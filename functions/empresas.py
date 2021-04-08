from Configuracion.db import mysql
from Models.Tables import Empresas, empre_scs
from Models.Tables import Configuraciones
from flask import flash, render_template, request, redirect, flash, session, url_for
from Models.Tables import db

def List_Empresas():
    #  configuraciones
    all = Empresas.query.all()
    data1 = empre_scs.dump(all)
    db.session.remove()
    return render_template('Empresas/List.html', empresas=data1)

def create_Empresas():
    if request.method == 'POST':
        try:
            Eruc = request.form['Eruc']
            Enombre = request.form['Enombre']
            Edepartamento = request.form['Edepartamento']
            Eestado = 1
            new_insert = Empresas(Eruc, Enombre, Edepartamento, Eestado)
            db.session.add(new_insert)
            db.session.commit()
            flash('Empresa añadida correctamente', 'success')
            db.session.remove()
            return redirect(url_for('TGlzdF9FbXByZXNhcw'))
        except Exception as e:
            print(e)
            flash('Error al insertar empresa, error: ' + str(e), 'danger')
            return redirect(url_for('TGlzdF9FbXByZXNhcw'))


def get_empresa(id):
    data = Empresas.get_id(id)
    data2 = Configuraciones.get_estados(self=1)
    db.session.remove()
    return render_template('Empresas/Editar.html', empresa=data, estados=data2)


def update_empresa(id):
    if request.method == 'POST':
        try:
            empresa = Empresas.query.filter_by(Eid=id).first()
            empresa.Eruc = request.form['Eruc']
            empresa.Enombre = request.form['Enombre']
            empresa.Edepartamento = request.form['Edepartamento']
            empresa.Eestado = request.form['estado']
            db.session.commit()
            flash('Empresa Actualizada', 'success')
            db.session.remove()
            return redirect(url_for('TGlzdF9FbXByZXNhcw'))
        except Exception as e:
            flash('Error al registrar Empresa. ' + str(e), 'danger')
            return redirect(url_for('TGlzdF9Db25maQ'))