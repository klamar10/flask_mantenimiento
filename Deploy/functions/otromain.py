from app import app
from Configuracion.db import mysql
from flask import Flask, jsonify, render_template, request, flash, session, redirect, url_for
from flask import flash, jsonify, request, redirect, flash, session, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_mail import Mail

mail = Mail()
from Models import Tables
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/SAPPJIMENEZ'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

@app.route('/')


def Init():
    if session.permanent is True:

        return render_template('Layouts/Inicio.html')
    else:
        all = Tables.Roles.query.filter(Tables.Roles.Restado.in_([1]))
        return render_template('Login/List.html', area=all)


if __name__ == "__main__":
    mail.init_app(app)
    app.run(port=4000, debug=True)
