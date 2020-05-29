#!flask/bin/python
from flask import Flask, request, render_template
from flaskext.mysql import MySQL
from datetime import datetime
import settings_gitignore

app = Flask(__name__)

# alarmActivated = True when user activated the alarm in the UI
# alarmActivated = False at start of app, or when user de-activated the alarm in the UI
alarmActivated = False

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


###############
### routing ###
###############

@app.route('/', methods=['GET'])
def main():

    return render_template('index.html')


@app.route('/ping/<device>', methods=['POST'])
def ping(device):

    _device = device
    _date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _status = alarmActivated
    cursor = mysql.get_db().cursor()
    sql = "INSERT INTO ping (device, date, status) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE device=%s, date=%s, status=%s"
    val = (_device, _date, _status, _device, _date, _status)
    cursor.execute(sql, val)
    mysql.get_db().commit()

    if alarmActivated == True:
        textArmed = "Armed"
    else:
        textArmed = "Disarmed"

    return {'message': textArmed}


@app.route('/status', methods=['GET'])
def status():

    if alarmActivated == True:
        return "armed"
    else:
        return "disarmed"


@app.route('/action/<action>/<device>/<rfid>', methods=['POST'])
def action(action,device,rfid):

    global alarmActivated
    now = datetime.now()

    if(checkRfid(settings_gitignore.rfidAllowedList, rfid)): 
        print("RFID: OK!")

        if action == "disable":
            alarmActivated = False
        elif action == "enable":
            alarmActivated = True
        elif action == "switch":
            alarmActivated = not alarmActivated

    else: 
        print("RFID",rfid,": NOT allowed")
        return {'message': "NotAllowed"}, 403
    
    if alarmActivated == True:
        textArmed = "Armed"
    else:
        textArmed = "Disarmed"

    _device = device
    _event = action
    _date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor = mysql.get_db().cursor()
    sql = "INSERT INTO events (device, event, date) VALUES (%s, %s, %s)"
    val = (_device, _event, _date)
    cursor.execute(sql, val)
    mysql.get_db().commit()

    print("status: ",action.strip(),"; alarmActivated: ",alarmActivated,"; device: ",device,"; rfid: ",rfid)

    return {'message': textArmed}


@app.route('/event', methods=['POST'])
def event():

    #print("request.is_json: ",request.is_json)
    content = request.get_json()

    _device = content['device']
    _event = content['event']
    _date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor = mysql.get_db().cursor()
    sql = "INSERT INTO events (device, event, date) VALUES (%s, %s, %s)"
    val = (_device, _event, _date)
    cursor.execute(sql, val)
    mysql.get_db().commit()

    output = "{} record inserted.".format(cursor.rowcount)
    print(output, ' - date: ', _date,'; device: ', _device,'; event: ', _event)
    return  output

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)
