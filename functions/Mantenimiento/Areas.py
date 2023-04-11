from flask import flash, render_template, request, redirect, flash, session, url_for
from datetime import datetime
# MODELOS
from Models.Tables import MT_areas, MT_areas_scs
from Models.Tables import Empresas
from Models.Tables import Configuraciones, UAR_accesos, Areas, Roles
from Models.Tables import db
import pytz
def List_Areas():
    try:
        # AREAS
        data1 = MT_areas.query.add_columns(MT_areas.MT_Aid, MT_areas.MT_Anombre, MT_areas.MT_Aestado, MT_areas.MT_Afech_crea, MT_areas.MT_Afech_mod).order_by(MT_areas.MT_Anombre.asc())
        # EMPRESAS
        consulta = Empresas.get_empresas_a(self=1)
        db.session.remove()
        return render_template('Mantenimiento/Areas/List.html', areas=data1, empresas=consulta)
    except Exception as e:
        flash('Error al mostrar página. ' + str(e), 'danger')
        return redirect(url_for('SW5pdA'))

def Create_Area():
    now = datetime.now(pytz.timezone('America/Lima'))
    fecha = now.strftime('%Y-%m-%d %H:%M:%S.000000')
    if request.method == 'POST':
        try:
            empresa = request.form['empresa']
            MT_Anombre = request.form['MT_Anombre']
            MT_fecha = str(fecha)
            MT_estado = 1
            new_insert = MT_areas(empresa, MT_Anombre, MT_estado, MT_fecha)
            db.session.add(new_insert)
            db.session.commit()
            flash('Area agregada: ' + MT_Anombre, 'success')
            db.session.remove()
            return redirect(url_for('TGlzdF9BcmVhcw'))
        except Exception as e:
            flash('Error al insertar area: el área ya existe'+ str(e), 'danger')
            return redirect(url_for('TGlzdF9BcmVhcw'))

def get_area(id):
    data = MT_areas.query.filter_by(MT_Aid=id).first()
    # Estado
    data2 = Configuraciones.get_estados(self=1)
    # EMPRESAS
    data3 = Empresas.get_empresas_a(self=1)
    db.session.remove()
    return render_template('Mantenimiento/Areas/Editar.html', area=data, estados=data2, empresas=data3)

def update_MT_area(id):
    now = datetime.now(pytz.timezone('America/Lima'))
    fecha = now.strftime('%Y-%m-%d %H:%M:%S')
    if request.method == 'POST':
        try:
            MT_area = MT_areas.query.filter_by(MT_Aid=id).first()
            MT_area.MT_Anombre = request.form['MT_Anombre']
            MT_area.MT_Afech_mod = str(fecha)
            MT_area.MT_Aestado = request.form['estado']
            MT_area.Eid = request.form['empresa']
            db.session.commit()
            flash('Area actualizada', 'success')
            db.session.remove()
            return redirect(url_for('TGlzdF9BcmVhcw'))
        except Exception as e:
            flash('Error al actualizar area: ' + str(e), 'danger')
            return redirect(url_for('TGlzdF9BcmVhcw'))

