#!flask/bin/python
from flask import Flask, request, render_template
from flaskext.mysql import MySQL
from flask_basicauth import BasicAuth
from datetime import datetime
import settings_gitignore
import os.path

app = Flask(__name__)

# alarmStatus = Home, is when you are Home, aka the system shouldn't be armed at all
# alarmStatus = Upstairs, is when you go to bed for example, aka the system should be armed for your devices of "downstairs"
# alarmStatus = Away, is when you are gone, aka the system should be armed for all your devices
#
#    default should be "Away", as it's the safest one in case of a reboot/restart
#
alarmStatus = "Away"

mysql = MySQL() 
app.config['MYSQL_DATABASE_PASSWORD'] = settings_gitignore.MYSQL_DATABASE_PASSWORD
app.config['MYSQL_DATABASE_DB'] = 'homerest'
if os.path.isfile('/.dockerenv'):
    print ("Running in container!")
    app.config['MYSQL_DATABASE_HOST'] = 'lightbo.lt-mariadb'
    app.config['MYSQL_DATABASE_PORT'] = 13306
    app.config['MYSQL_DATABASE_USER'] = 'homereset'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'quertyhomerest'
else: # Not running in container
    print ("NOT running in container!")
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    app.config['MYSQL_DATABASE_USER'] = 'homereset'
mysql.init_app(app)
conn = mysql.connect()

app.config['BASIC_AUTH_USERNAME'] = ''
app.config['BASIC_AUTH_PASSWORD'] = 'matrix'
basic_auth = BasicAuth(app)


#################
### functions ###
#################

# check if rfid is inside the rfidAlledList
def checkRfid(list1, val): 
      
    print(val,list1)
    if val in list1: 
            return True 
    return False

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

    return alarmStatus


@app.route('/action/<action>/<device>/<rfid>', methods=['POST'])
def action(action,device,rfid):
    # action == home|upstairs|away

    global alarmStatus
    
    if(checkRfid(settings_gitignore.rfidAllowedList, rfid)): 
        print("RFID: OK!")

        if action == "home":
            alarmStatus = "Home"
        elif action == "upstairs":
            alarmStatus = "Upstairs"
        elif action == "away":
            alarmStatus = "Away"

    else: 
        print("RFID",rfid,": NOT allowed")
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
