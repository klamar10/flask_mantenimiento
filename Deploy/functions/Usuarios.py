from app import app
from Configuracion.db import mysql
from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash, render_template, request, redirect, flash, session, url_for
from datetime import datetime
# MODELOS
from Models.Tables import Usuarios, usuarios_scs
from Models.Tables import Empresas
from Models.Tables import Configuraciones, UAR_accesos, Areas, Roles
from Models.Tables import db


def Lis_Usuarios():
    try:
        # USUARIOS
        data1 = Usuarios.query.all()
        # EMPRESAS
        consulta = Empresas.get_empresas_a(self=1)
        db.session.remove()
        return render_template('Usuarios/List.html', contacts=data1, empresas=consulta)
    except Exception as e:
        flash('Error al mostrar página. ' + str(e), 'danger')
        return redirect(url_for('SW5pdA'))


def create():
    now = datetime.now()
    fecha = now.strftime('%Y-%m-%d %H:%M:%S')
    if request.method == 'POST':
        try:
            _nombre = request.form['nombre']
            _apellido = request.form['apellido']
            _correo = request.form['correo']
            _password = request.form['password']
            _fecha = str(fecha)
            _estado = 1
            _empresa = request.form['empresa']
            _fecha_modificacion = ''

            new_insert = Usuarios(_nombre, _apellido, _correo, _password, _estado, _empresa, _fecha, _fecha_modificacion)
            db.session.add(new_insert)
            db.session.commit()
            flash('Usuario Agregado: ' + _nombre + ' ' + _apellido, 'success')
            db.session.remove()
            return redirect(url_for('VXN1YXJpb3M'))
        except Exception as e:
            flash('Error al insertar usuario: ' + _nombre + ' ' + _apellido + '. Pueda que ya exista.', 'danger')
            return redirect(url_for('VXN1YXJpb3M'))


def get_usuario(id):
    data = Usuarios.query.filter_by(Uid=id).first()
    # Estado
    data2 = Configuraciones.get_estados(self=1)
    # EMPRESAS
    data3 = Empresas.get_empresas_a(self=1)
    db.session.remove()
    return render_template('Usuarios/Editar.html', contact=data, estados=data2, empresas=data3)


def update(id):
    now = datetime.now()
    fecha = now.strftime('%Y-%m-%d %H:%M:%S')
    if request.method == 'POST':
        try:
            usuario = Usuarios.query.filter_by(Uid=id).first()
            usuario.Unombre = request.form['nombre']
            usuario.Uapellido = request.form['apellido']
            usuario.Ucorreo = request.form['correo']
            usuario.Upassword = request.form['password']
            usuario.Ufecha_modificacion = str(fecha)
            usuario.Uestado = request.form['estado']
            usuario.Eid = request.form['empresa']
            db.session.commit()
            flash('Usuario Actualizado', 'success')
            db.session.remove()
            return redirect(url_for('VXN1YXJpb3M'))
        except Exception as e:
            flash('Error al actualizar usuario: ' + usuario.Unombre + ' ' + usuario.Uapellido + ' ' + str(e), 'danger')
            return redirect(url_for('VXN1YXJpb3M'))

def delete(id):
    cur = mysql.connection.cursor()
    cur.execute('delete from usuarios where Uid = {0}'.format(id, ))
    # cur2 = mysql.connection.cursor()
    # cur2.execute('ALTER TABLE usuarios AUTO_INCREMENT = {0}'.format(id, ))

    mysql.connection.commit()
    flash('Usuario Eliminado', 'success')
    db.session.remove()
    return redirect(url_for('VXN1YXJpb3M'))


def accesos(id):
    #  accesos
    # cur1 = mysql.connection.cursor()
    # cur1.execute("""
    #            SELECT a.uid, a.Aid, a.rid, c.Adescripcion, d.Rdescripcion FROM `uar_accesos` a
    #            INNER JOIN usuarios b on a.Uid = b.Uid
    #            INNER JOIN area c on a.Aid =c.Aid
    #            INNER JOIN roles d on a.Rid = d.Rid where b.uid = %s""", (id,))
    # data1 = cur1.fetchall()
    data1 = Usuarios.get_roles(id)
    #  USUARIO
    data2 = Usuarios.get_Detalle_id(id)
    #  AREA
    data3 = Areas.get_area_a(self=1)
    #  Rol
    data4 = Roles.get_roles_a(self=1)
    db.session.remove()
    return render_template('Usuarios/Accesos.html', accesos=data1, usuario=data2, areas=data3, roles=data4)


def create_accesos(id):
    if request.method == 'POST':
        try:
            _id = id
            area = request.form['area']
            rol = request.form['rol']
            new_insert = UAR_accesos(_id, area, rol)
            db.session.add(new_insert)
            db.session.commit()
            flash('Acceso Agregado', 'success')
            db.session.remove()
            return redirect(url_for('YWNjZXNvcw', id=id))

        except Exception as e:
            flash('Error al crear acceso, pueda que ya exista el registro. ' + str(e), 'danger')
            return redirect(url_for('YWNjZXNvcw', id=id))


def delete_accesos(id, aid, rid):
    try:
        consulta = UAR_accesos.UAR_id_all(id, aid, rid)
        db.session.delete(consulta)
        db.session.commit()
        flash('Acceso eliminado con éxito', 'success')
        db.session.remove()
        return redirect(url_for('YWNjZXNvcw', id=id))
    except  Exception as e:
        flash('Error al tratar de eliminar: ' + str(e), 'danger')
        return redirect(url_for('YWNjZXNvcw', id=id))