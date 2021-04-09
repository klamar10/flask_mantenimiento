from flask import render_template, request, flash, session, redirect, url_for
from Models.Tables import Roles, Usuarios, Areas
from functools import wraps
from Models.Tables import db

# FUNCIONES

# valida token activo
def check_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.permanent is False:
            flash('Vuelve a iniciar sesión', 'warning')
            return redirect(url_for('SW5pdA'))
        else:
            pass
        return f(*args, **kwargs)

    return decorated

# valida usuario habilitado
def check_habilitado(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.permanent:
            Estado = Usuarios.get_Estado(session['Uid'])
            if Estado is None:
                session.clear()
                data1 = Areas.get_area_a(self=1)
                db.session.remove()
                return render_template('Login/List.html', area=data1)
            else:
                pass
                return f(*args, **kwargs)
        else:
            data1 = Areas.get_area_a(self=1)
            return render_template('Login/List.html', area=data1)
    return decorated

def Init():
    if session.permanent is True:
        try:
            Estado = Usuarios.get_Estado(session['Uid'])
            if Estado is None:
                session.clear()
                data1 = Areas.get_area_a(self=1)
                db.session.remove()
                return render_template('Login/List.html', area=data1)
            else:
                return render_template('Layouts/Inicio.html')
        except:
            db.session.remove()
            session.clear()
            data1 = Areas.get_area_a(self=1)
            db.session.remove()
            return render_template('Login/List.html', area=data1)
    else:
        #  USUARIOS
        # data1 = Areas.query.filter(Areas.Restado.in_([1]))
        data1 = Areas.get_area_a(self=1)
        db.session.remove()
        return render_template('Login/List.html', area=data1)


def Login():
    if request.method == 'POST':
        area = request.form['area']
        email = request.form['correo']
        password = request.form['password']
        consulta = Usuarios.get_by_email(email, password)
        if consulta is not None:
            uid = Usuarios.get_id(email)
            Area = Areas.get_id(area)
            Rol = Roles.get_id_rol(uid, area)
            if Rol is not None:
                session.permanent = True
                session['rol'] = Rol.Rdescripcion
                session['rolid'] = Rol.Rid
                session['Uid'] = uid
                session['Area'] = Area
                session['AreaID'] = area
                flash('Bienvenid@ a la plataforma en línea de administracion de trabajo. Ingresó al area de ' + session['Area'] + ' con el rol de ' + session['rol'], 'secondary')
                db.session.remove()
                return redirect(url_for('SW5pdA'))
            else:
                db.session.remove()
                flash('No tiene acceso', 'danger')
                return redirect(url_for('SW5pdA'))
        else:
            db.session.remove()
            flash('Credenciales erroneas', 'danger')
            return redirect(url_for('SW5pdA'))


def Logout():
    session.clear()
    return redirect(url_for('SW5pdA'))
