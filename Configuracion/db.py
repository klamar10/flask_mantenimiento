from app import app
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
mysql = MySQL()

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'adrian'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'adminbd_college'
mysql.init_app(app)


