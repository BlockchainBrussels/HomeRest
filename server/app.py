#!flask/bin/python
from flask import Flask, request, render_template
from flaskext.mysql import MySQL
from flask_basicauth import BasicAuth
from datetime import datetime
import os.path
import time
import atexit

app = Flask(__name__)


# alarmStatus = Home, is when you are Home, aka the system shouldn't be armed at all
# alarmStatus = Upstairs, is when you go to bed for example, aka the system should be armed for your devices of "downstairs"
# alarmStatus = Away, is when you are gone, aka the system should be armed for all your devices
#
#    default should be "Away", as it's the safest one in case of a reboot/restart
#
alarmStatus = "Home"

mysql = MySQL() 
app.config['MYSQL_DATABASE_DB'] = 'homerest'
if os.path.isfile('/.dockerenv'):
    print ("Running in container!")
    app.config['MYSQL_DATABASE_HOST'] = 'lightbo.lt-db'
    app.config['MYSQL_DATABASE_USER'] = 'homereset'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'quertyhomerest'
else: # Not running in container
    print ("NOT running in container!")
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    app.config['MYSQL_DATABASE_USER'] = 'homereset'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'ijdcIHQC8372ihc'
mysql.init_app(app)
conn = mysql.connect()

app.config['BASIC_AUTH_USERNAME'] = ''
app.config['BASIC_AUTH_PASSWORD'] = 'blahblahrfidkey'
basic_auth = BasicAuth(app)


#################
### schedulers ###
#################

from apscheduler.schedulers.background import BackgroundScheduler

def print_date_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

scheduler = BackgroundScheduler()
scheduler.add_job(func=print_date_time, trigger="interval", seconds=3)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


#################
### functions ###
#################

# check if rfid is inside the rfidAlledList
def checkRfid(rfid): 

    cursor = mysql.get_db().cursor()
    sql = "SELECT * FROM configuration WHERE variable ='rfid' AND value LIKE %s"
    val = ('%'+rfid+'%')
    cursor.execute(sql,val)
    cursor.fetchall()

    print("cursor.rowcount: ",cursor.rowcount)
    if cursor.rowcount == 0:
            return False 
    return True

def insertEvent(_device, _event, _date, _status):

    cursor = mysql.get_db().cursor()
    sql = "INSERT INTO events (device, event, date, status) VALUES (%s, %s, %s, %s)"
    val = (_device, _event, _date, _status)
    cursor.execute(sql, val)
    mysql.get_db().commit()

    return format(cursor.rowcount)

def insertPing(_device, _date, _status):

    cursor = mysql.get_db().cursor()
    sql = "INSERT INTO ping (device, date, status) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE device=%s, date=%s, status=%s"
    val = (_device, _date, _status, _device, _date, _status)
    cursor.execute(sql, val)
    mysql.get_db().commit()

    return format(cursor.rowcount)


###############
### routing ###
###############

@app.route('/', methods=['GET'])
@basic_auth.required
def main():

    return render_template('index.html')


@app.route('/ping/<device>', methods=['POST'])
def ping(device):

    _date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    insertPing(device, _date, alarmStatus)

    return alarmStatus


@app.route('/status', methods=['GET'])
def status():

    if alarmStatus == "Home":
        return alarmStatus, 200
    else:
        return alarmStatus, 201


@app.route('/action/<action>/<device>/<rfid>', methods=['POST'])
def action(action,device,rfid):
    # action == home|upstairs|away
    # action == switch == (home<->away)

    global alarmStatus
    
    if(checkRfid(rfid)): 
        #print("RFID: OK!")
        if action == "home":
            alarmStatus = "Home"
        elif action == "upstairs":
            alarmStatus = "Upstairs"
        elif action == "away":
            alarmStatus = "Away"
        elif action == "switch":
            if alarmStatus == "Home":
                alarmStatus = "Away"
            else:
                alarmStatus = "Home"

    else: 
        print("RFID ",rfid,": NOT allowed")
        return {'message': "NotAllowed"}, 403
    
    _date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    insertEvent(device, action, _date, alarmStatus)

    print("status: ",action.strip(),"; alarmStatus: ",alarmStatus,"; device: ",device,"; rfid: ",rfid)

    return alarmStatus, 201


@app.route('/event', methods=['POST'])
def event():

    #print("request.is_json: ",request.is_json)
    content = request.get_json()

    _date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output = "{} record inserted.".format(insertEvent(content['device'], content['event'], _date, alarmStatus))

    print(output, ' - date: ', _date,'; device: ', content['device'],'; event: ', content['event'])
    return  output, 201


############
### main ###
############

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)
