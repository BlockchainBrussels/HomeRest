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

@app.route('/', methods=['GET'])
def main():

    return render_template('index.html')

@app.route('/action/<action>', methods=['POST'])
def action(action):

    now = datetime.now()

    _device = '0'
    _event = action
    _date = now.strftime("%Y-%m-%d %H:%M:%S")

    cursor = mysql.get_db().cursor()
    sql = "INSERT INTO events (device, event, date) VALUES (%s, %s, %s)"
    val = (_device, _event, _date)
    cursor.execute(sql, val)
    mysql.get_db().commit()

    if action == 'disable':
        alarmActivated = False
        textArmed = "Disarmed"
    elif action == "enable":
        alarmActivated = True
        textArmed = "Armed"
    print("action: ",action.strip(),"; alarmActivated: ",alarmActivated)
    
    return render_template('index.html', textArmed=textArmed)

@app.route('/event', methods=['POST'])
def event():

    now = datetime.now()

    print("request.is_json: ",request.is_json)
    content = request.get_json()

    _device = content['device']
    _event = content['event']
    _date = now.strftime("%Y-%m-%d %H:%M:%S")

    cursor = mysql.get_db().cursor()
    sql = "INSERT INTO events (device, event, date) VALUES (%s, %s, %s)"
    val = (_device, _event, _date)
    cursor.execute(sql, val)
    mysql.get_db().commit()

    output = "{} record inserted.".format(cursor.rowcount)
    print(output)
    print('date: ', _date,'; device: ', _device,'; event: ', _event)
    return  output

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)
