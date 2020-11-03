#!flask/bin/python
from flask import Flask, request, render_template
from flaskext.mysql import MySQL
from datetime import datetime
import settings_gitignore

app = Flask(__name__)

# alarmActivated = Home, is when you are Home, aka the system shouldn't be armed at all
# alarmActivated = Upstairs, is when you go to bed for example, aka the system should be armed for your devices of "downstairs"
# alarmActivated = Away, is when you are gone, aka the system should be armed for all your devices
#
#    default should be "Away", as it's the safest one in case of a reboot/restart
#
alarmActivated = "Away"

mysql = MySQL() 
app.config['MYSQL_DATABASE_USER'] = 'homereset'
app.config['MYSQL_DATABASE_PASSWORD'] = settings_gitignore.MYSQL_DATABASE_PASSWORD
app.config['MYSQL_DATABASE_DB'] = 'homerest'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
conn = mysql.connect()

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
def main():

    return render_template('index.html')


@app.route('/ping/<device>', methods=['POST'])
def ping(device):

    _date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    insertPing(device, _date, alarmActivated)

    return alarmActivated


@app.route('/status', methods=['GET'])
def status():

    return alarmActivated
    #return "alarmActivated, 200


@app.route('/action/<action>/<device>/<rfid>', methods=['POST'])
def action(action,device,rfid):
    # action == home|upstairs|away

    global alarmActivated
    
    if(checkRfid(settings_gitignore.rfidAllowedList, rfid)): 
        print("RFID: OK!")

        if action == "home":
            alarmActivated = "Home"
        elif action == "upstairs":
            alarmActivated = "Upstairs"
        elif action == "away":
            alarmActivated = "Away"

    else: 
        print("RFID",rfid,": NOT allowed")
        return {'message': "NotAllowed"}, 403
    
    _date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    insertEvent(device, action, _date, alarmActivated)

    print("status: ",action.strip(),"; alarmActivated: ",alarmActivated,"; device: ",device,"; rfid: ",rfid)

    return alarmActivated


@app.route('/event', methods=['POST'])
def event():

    #print("request.is_json: ",request.is_json)
    content = request.get_json()

    _date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output = "{} record inserted.".format(insertEvent(content['device'], content['event'], _date, alarmActivated))

    print(output, ' - date: ', _date,'; device: ', content['device'],'; event: ', content['event'])
    return  output

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)
