from flask import jsonify, render_template, request, redirect, flash, session, url_for
from datetime import datetime
# MODELOS
from Models.Tables import MT_ambientes, MT_eti_fn, MT_funciones, MT_etiquetas, MT_asig_et_fn
from Models.Tables import MT_areas
from Models.Tables import Configuraciones, UAR_accesos, Areas, Roles
from Models.Tables import db
import pytz
def List_Ambientes():
    try:
        # AMBIENTES
        now = datetime.now(pytz.timezone('America/Lima'))
        fecha = now.strftime('%Y-%m-%d %H:%M:%S.000000')
        all = MT_ambientes.get_ambientes(self=1)
        # AREAS
        consulta = MT_areas.get_areas_a(self=1)
        db.session.remove()
        return render_template('Mantenimiento/Ambientes/List.html', ambientes=all, areas=consulta)
    except Exception as e:
        flash('Error al mostrar página. ' + str(e), 'danger')
        return redirect(url_for('SW5pdA'))

def Create_Ambiente():
    now = datetime.now(pytz.timezone('America/Lima'))
    fecha = now.strftime('%Y-%m-%d %H:%M:%S')
    if request.method == 'POST':
        try:
            MT_Aid = request.form['MT_Aid']
            MT_ABnombre = request.form['MT_ABnombre']
            MT_ABfech_crea = str(fecha)
            MT_ABestado = 1

            new_insert = MT_ambientes(MT_Aid, MT_ABnombre, MT_ABestado, MT_ABfech_crea)
            db.session.add(new_insert)
            db.session.commit()
            flash('Area agregada: ' + MT_ABnombre, 'success')
            db.session.remove()
            return redirect(url_for('TGlzdF9BbWJpZW50ZXM'))
        except Exception as e:
            flash('Error al registrar ambiente: el ambiente ya existe'+ str(e), 'danger')
            return redirect(url_for('TGlzdF9BbWJpZW50ZXM'))
#
def Get_ambiente(id):
    data = MT_ambientes.query.filter_by(MT_Abcodigo=id).first()
    # Estado
    data2 = Configuraciones.get_estados(self=1)
    # AREA
    data3 = MT_areas.get_areas_a(self=1)
    db.session.remove()
    return render_template('Mantenimiento/Ambientes/Edit.html', ambiente=data, estados=data2, areas=data3)
#
def Update_MT_ambiente(id):
    now = datetime.now(pytz.timezone('America/Lima'))
    fecha = now.strftime('%Y-%m-%d %H:%M:%S')
    if request.method == 'POST':
        try:
            sga = MT_ambientes.query.filter_by(MT_Abcodigo=id).first()
            sga.MT_Aid = request.form['empresa']
            sga.MT_ABnombre = request.form['MT_ABnombre']
            sga.MT_ABestado = request.form['estado']
            sga.MT_ABfech_mod = str(fecha)
            db.session.commit()
            flash('Ambiente actualizado', 'success')
            db.session.remove()
            return redirect(url_for('TGlzdF9BbWJpZW50ZXM'))
        except Exception as e:
            flash('Error al actualizar ambiente: ' + str(e), 'danger')
            return redirect(url_for('TGlzdF9BbWJpZW50ZXM'))
# -------------------------- VINCULACION DE ETIQUETAS------------------------------
def Get_ambiente_V(id):

    data1 = MT_etiquetas.query.filter(MT_etiquetas.MT_Eestado ==1,
                              ~MT_asig_et_fn.query.filter(MT_asig_et_fn.MT_Eid == MT_etiquetas.MT_Eid,
                                                          MT_asig_et_fn.MT_AEFestado == 1, MT_asig_et_fn.MT_Abcodigo == id).exists())\
        .order_by(MT_etiquetas.MT_Enombre.asc()).all()

    data2 = MT_asig_et_fn.query.filter(MT_etiquetas.MT_Eid == MT_asig_et_fn.MT_Eid)\
        .filter(MT_asig_et_fn.MT_AEFestado ==1, MT_etiquetas.MT_Eestado ==1, MT_asig_et_fn.MT_Abcodigo == id)\
        .add_columns(MT_asig_et_fn.MT_AEFid, MT_etiquetas.MT_Eid ,MT_etiquetas.MT_Enombre, MT_asig_et_fn.MT_AEFfech_crea)\
        .order_by(MT_etiquetas.MT_Enombre.asc()).all()
    db.session.remove()
    return render_template('Mantenimiento/Ambientes/Vinculacion.html', pendientes=data1, vinculados=data2, id=id)

def Create_Vincular(id, eid):
    now = datetime.now(pytz.timezone('America/Lima'))
    fecha = now.strftime('%Y-%m-%d %H:%M:%S.000000')
    try:
        b = MT_asig_et_fn.query.filter_by(MT_Abcodigo =id, MT_Eid =eid).first()
        if b is not None:
            b.MT_AEFestado = 1
        else:
            ambiente = id
            etiqueta = int(eid)
            estado = 1
            fecha_crea = str(fecha)
            fech_mod = None
            new_insert = MT_asig_et_fn(MT_Abcodigo=ambiente, MT_Eid=etiqueta, MT_AEFestado=estado, MT_AEFfech_crea=fecha_crea, MT_AEFfech_mod=fech_mod)
            db.session.add(new_insert)
        db.session.commit()
        flash('Vinculación completa', 'success')
        db.session.remove()
        return redirect(url_for('R2V0X2FtYmllbnRlX1Y', id=id))
    except Exception as e:
        flash('Error al vincular: ' + str(e), 'danger')
        return redirect(url_for('R2V0X2FtYmllbnRlX1Y', id=id))

def delete_Desvincular(id, eid):
    try:
        consulta = MT_asig_et_fn.query.filter_by(MT_AEFid=eid).first()
        consulta.MT_AEFestado = 2
        db.session.commit()
        flash('Asignación eliminado con éxito', 'success')
        db.session.remove()
        return redirect(url_for('R2V0X2FtYmllbnRlX1Y', id=id))
    except Exception as e:
        flash('Error al tratar de eliminar: ' + str(e), 'danger')
        return redirect(url_for('R2V0X2FtYmllbnRlX1Y', id=id))