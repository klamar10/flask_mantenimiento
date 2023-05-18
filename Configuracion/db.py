from app import app
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
mysql = MySQL()

app.config['MYSQL_HOST'] = '159.89.48.159'
app.config['MYSQL_USER'] = 'adrian'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'adminbd_college'
mysql.init_app(app)


