from Models.Tables import Configuraciones, config_scs
from flask import Flask, render_template, request, redirect, flash, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from Models.Tables import db


def List_Configuracion():
    #  configuraciones
    all = Configuraciones.query.all()
    data1 = config_scs.dump(all)
    db.session.remove()
    return render_template('Layouts/Configuracion.html', configuraciones=data1)


def Create_Configuracion():
    if request.method == 'POST':
        _Ccategoria = request.form['Ccategoria']
        _Corden = request.form['Corden']
        _Cdescripcion = request.form['Cdescripcion']
        _Cvalor1 = request.form['Cvalor1']
        new_insert = Configuraciones(_Ccategoria, _Corden, _Cdescripcion, _Cvalor1)
        try:
            db.session.add(new_insert)
            db.session.commit()
            flash('Configuracion añadida correctamente', 'success')
            db.session.remove()
            return redirect(url_for('TGlzdF9Db25maQ'))
        except:
            db.session.remove()
            flash('Error al registrar configuracion', 'danger')
            return redirect(url_for('TGlzdF9Db25maQ'))


def Get_Configuracion(id):
    data = Configuraciones.get_id(id)
    db.session.remove()
    return render_template('Layouts/Editar_Configuracion.html', config=data)


def Update_Configuracion(id):
    if request.method == 'POST':
        try:
            config = Configuraciones.query.filter_by(Cid=id).first()
            config.Ccategoria = request.form['Ccategoria']
            config.Corden = request.form['Corden']
            config.Cdescripcion = request.form['Cdescripcion']
            config.Cvalor1 = request.form['Cvalor1']
            db.session.commit()
            flash('Configuracion Actualizada', 'success')
            db.session.remove()
            return redirect(url_for('TGlzdF9Db25maQ'))
        except:
            flash('Error al registrar configuracion', 'danger')
            return redirect(url_for('TGlzdF9Db25maQ'))
        # try:
        #     config.Ccategoria = Ccategoria
        #     config.Corden = Corden
        #     config.Cdescripcion = Cdescripcion
        #     config.Cvalor1 = Cvalor1
        #
        #
        #
        # except:
        #     flash('Error al registrar configuracion', 'danger')
        #     return redirect(url_for('TGlzdF9Db25maQ'))
