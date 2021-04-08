from Configuracion.db import mysql
from flask import flash, render_template, request, redirect, flash, session, url_for
from datetime import datetime
def List_Empresas():
    acces = session.permanent
    rol = session['rol']
    if acces is True:
        if rol == 1:
            #  USUARIOS
            cur1 = mysql.connection.cursor()
            cur1.execute("SELECT * FROM `empresas`")
            data1 = cur1.fetchall()
            # Estado
            cur2 = mysql.connection.cursor()
            cur2.execute("sELECT Cdescripcion, Corden from configuraciones WHERE Ccategoria = 'Estado' and Cvalor1 = 1")
            data2 = cur2.fetchall()

            return render_template('Empresas/List.html', empresas=data1, roles=data2)
        else:
            flash('Usuario No autorizado', 'primary')
            return render_template('Layouts/Inicio.html')
    else:
        flash('Debe iniciar sesión', 'danger')
        return render_template('Login/List.html')

def create_Empresas():
    if request.method == 'POST':
        try:
            Eruc =request.form['Eruc']
            Enombre =request.form['Enombre']
            Edepartamento =request.form['Edepartamento']
            Eestado = 1
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO `empresas`(`Eruc`, `Enombre`, `Edepartamento`, `Eestado`) VALUES (%s, %s, %s, %s)",
            (Eruc, Enombre, Edepartamento, Eestado,))

            mysql.connection.commit()
            flash('Empresa agregada: ' + Enombre, 'success')

            return redirect(url_for('TGlzdF9FbXByZXNhcw'))

        except:
            flash('Error al insertar empresa: '+Enombre, 'danger')
            return redirect(url_for('TGlzdF9FbXByZXNhcw'))

def get_usuario(id):
    cur = mysql.connection.cursor()
    cur.execute('select * from usuarios where Uid = %s',(id, ))
    data = cur.fetchall()
    # ROLES
    cur2 = mysql.connection.cursor()
    cur2.execute("SELECT Cdescripcion, Corden from configuraciones WHERE Ccategoria = 'Rol' and Cvalor1 = 1")
    data2 = cur2.fetchall()
    # Estado
    cur3 = mysql.connection.cursor()
    cur3.execute("sELECT Cdescripcion, Corden from configuraciones WHERE Ccategoria = 'Estado' and Cvalor1 = 1")
    data3 = cur3.fetchall()
    return render_template('Usuarios/Editar.html', contact=data[0], roles=data2, estados=data3)

def update(id):
    now = datetime.now()
    fecha = now.strftime('%Y-%m-%d %H:%M:%S')
    if request.method == 'POST':
        _nombre =request.form['nombre']
        _apellido =request.form['apellido']
        _correo =request.form['correo']
        _password =request.form['password']
        _rol = request.form['rol']
        _fecha = str(fecha)
        _estado = request.form['estado']
        cur = mysql.connection.cursor()
        cur.execute("""
            update usuarios
            set Unombre = %s,
                Uapellido = %s,
                Ucorreo = %s,
                Upassword = %s,
                Urol = %s,
                Ufecha_modificacion= %s,
                Uestado = %s
            where Uid = %s
        """, (_nombre, _apellido, _correo, _password, _rol, _fecha, _estado, id))
        mysql.connection.commit()
        flash('Usuario Actualizado', 'success')
        return redirect(url_for('VXN1YXJpb3M'))

def delete(id):
    cur = mysql.connection.cursor()
    cur.execute('delete from usuarios where Uid = {0}'.format(id, ))
    # cur2 = mysql.connection.cursor()
    # cur2.execute('ALTER TABLE usuarios AUTO_INCREMENT = {0}'.format(id, ))

    mysql.connection.commit()
    flash('Usuario Eliminado', 'success')
    return redirect(url_for('VXN1YXJpb3M'))
