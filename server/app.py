#!flask/bin/python
from flask import Flask, request, render_template
from flaskext.mysql import MySQL
from flask_basicauth import BasicAuth
from datetime import datetime
import os.path
import time
import atexit
import threading

app = Flask(__name__)


# alarmStatus = Home, is when you are Home, aka the system shouldn't be armed at all
# alarmStatus = Upstairs, is when you go to bed for example, aka the system should be armed for your devices of "downstairs"
# alarmStatus = Away, is when you are gone, aka the system should be armed for all your devices
#
#    default should be "Away", as it's the safest one in case of a reboot/restart
#
alarmStatus = "Home"
intrusionDetected = False
intrusionDelayOngoing = False

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


##################
### schedulers ###
##################

#
### INTRUSION BASED ON /event AND /intrusion, NO SCHEDULER NEEDED FOR INTRUSION
#
#from apscheduler.schedulers.background import BackgroundScheduler
#
#def intrusion_detection():
#    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
#
#scheduler = BackgroundScheduler()
#scheduler.add_job(func=intrusion_detection, trigger="interval", seconds=1)
#scheduler.start()
#
## Shut down the scheduler when exiting the app
#atexit.register(lambda: scheduler.shutdown())


#################
### functions ###
#################

# check if rfid is inside the rfidAlledList
def checkRfid(rfid): 
    # Check if the given RFID token is in the database as approved token, or not

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
    # Add to the database what happens with a lightbo.lt sensor

    cursor = mysql.get_db().cursor()
    sql = "INSERT INTO events (device, event, date, status) VALUES (%s, %s, %s, %s)"
    val = (_device, _event, _date, _status)
    cursor.execute(sql, val)
    mysql.get_db().commit()

    return format(cursor.rowcount)

def insertPing(_device, _date, _status):
    # Devices Ping every X seconds, saying "hey, I'm still alive, not broken (on purpose), etc"

    cursor = mysql.get_db().cursor()
    sql = "INSERT INTO ping (device, date, status) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE device=%s, date=%s, status=%s"
    val = (_device, _date, _status, _device, _date, _status)
    cursor.execute(sql, val)
    mysql.get_db().commit()

    return format(cursor.rowcount)

def intrusionDelay():
    # When intrusionDelayOngonig == True, there shoul dbe no intrusionDetected activated
    # Happens when you've put the alarm in Upstairs or Away, but don't want to detect yourself of course
    
    global intrusionDelayOngoing
    print("Start intrusionDelay - intrusionDelayOngoing:",intrusionDelayOngoing)
    intrusionDelayOngoing = True
    print(" => Ongoing intrusionDelay - intrusionDelayOngoing:",intrusionDelayOngoing)
    time.sleep(10)
    intrusionDelayOngoing = False
    print("End intrusionDelay - intrusionDelayOngoing:",intrusionDelayOngoing)

    return True

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
    global intrusionDetected

    _date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    insertEvent(device, action, _date, alarmStatus)
    print("status: ",action.strip(),"; alarmStatus: ",alarmStatus,"; device: ",device,"; rfid: ",rfid,"; intrusionDetected: ",intrusionDetected)

    # IF RFID check confirms good RFID token, do the action
    #    Also start the intrusionDetection process
    # IF bad RFID token, exit

    if(checkRfid(rfid)): 
        #print("RFID: OK!")
        intrusionDetected = False

        if action == "home":
            alarmStatus = "Home"
        elif action == "upstairs":
            alarmStatus = "Upstairs"
            threading.Thread(target=intrusionDelay)
        elif action == "away":
            alarmStatus = "Away"
            threading.Thread(target=intrusionDelay)
        elif action == "switch":
            if alarmStatus == "Home":
                alarmStatus = "Away"
                threading.Thread(target=intrusionDelay)
            else:
                alarmStatus = "Home"

        print(" => alarmStatus: ",alarmStatus,"; device: ",device,"; intrusionDetected: ",intrusionDetected)
        
    else: 
        print("RFID ",rfid,": NOT allowed")
        return {'message': "NotAllowed"}, 403

    return alarmStatus, 201


@app.route('/event', methods=['POST'])
def event():

    #print("request.is_json: ",request.is_json)
    content = request.get_json()

    _date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output = "{} record inserted.".format(insertEvent(content['device'], content['event'], _date, alarmStatus))

    if alarmStatus != "Home" and intrusionDelayOngoing == False:
        intrusionDetected = True
    else:
        intrusionDetected = False

    print(output, ' - date: ', _date,'; device: ', content['device'],'; event: ', content['event'],'; intrusionDetected:',intrusionDetected,'(intrusionDelayOngoing:',intrusionDelayOngoing,')')
    return  output, 201


@app.route('/intrusion', methods=['GET'])
def intrusion():

    print('intrusion - intrusionDetected:',intrusionDetected)
    if intrusionDetected == False:
        return "False", 200
    else:
        return "True", 201

############
### main ###
############

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)

