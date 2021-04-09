from flask import Flask
app = Flask(__name__)
class Config():
    # Configuración del email

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'lm98adrian@gmail.com'
    app.config['MAIL_PASSWORD'] = 'adrianmorales1098'