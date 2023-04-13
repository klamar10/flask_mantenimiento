from flask import jsonify, render_template, request, redirect, flash, session, url_for
from datetime import datetime
# MODELOS
from Models.Tables import Usuarios, MT_asig_et_fn, MT_asig_funciones, MT_ambientes
from Models.Tables import MT_areas
from Models.Tables import MT_etiquetas, UAR_accesos, Areas, Roles
from Models.Tables import db
import pytz
def List_Asignados():
    try:
        data1 = Usuarios.query.join(UAR_accesos, UAR_accesos.Uid == Usuarios.Uid)\
            .filter(Usuarios.Uestado == 1, UAR_accesos.Aid == 1, UAR_accesos.Rid == 2)\
            .add_columns(Usuarios.Uid, Usuarios.Uapellido, Usuarios.Unombre).all()
        db.session.remove()
        return render_template('Mantenimiento/Asig_Trabajo/List.html', usuarios=data1)
    except Exception as e:
        flash('Error al mostrar página. ' + str(e), 'danger')
        return redirect(url_for('SW5pdA'))


def Get_asignado_trabajo(id):
    data1 = MT_areas.query.filter_by(MT_Aestado=1).all()

    data2 = MT_asig_et_fn.query.join(MT_asig_funciones, MT_asig_funciones.MT_AEFid == MT_asig_et_fn.MT_AEFid)\
        .join(MT_ambientes, MT_ambientes.MT_Abcodigo == MT_asig_et_fn.MT_Abcodigo).join(MT_etiquetas,MT_etiquetas.MT_Eid == MT_asig_et_fn.MT_Eid) \
        .filter(MT_asig_funciones.MT_ASFestado == 1, MT_asig_funciones.Uid == id, MT_ambientes.MT_ABestado==1) \
        .add_columns(MT_asig_funciones.MT_ASFid,MT_etiquetas.MT_Enombre, MT_ambientes.MT_ABnombre, MT_asig_funciones.MT_ASFfech_asigdesde, MT_asig_funciones.MT_ASFfech_asighasta) \
        .order_by(MT_ambientes.MT_ABnombre.asc()).all()
    # //data2 = MT_asig_funciones.query.join(MT_asig_et_fn, MT_asig_et_fn.MT_AEFid == MT_asig_funciones.MT_AEFid)

    if request.method == 'POST':
       try:
           area = request.form['area']
           print(area)
           pendientes = MT_ambientes.query.join(MT_asig_et_fn, MT_asig_et_fn.MT_Abcodigo == MT_ambientes.MT_Abcodigo)\
               .join(MT_etiquetas, MT_etiquetas.MT_Eid == MT_asig_et_fn.MT_Eid)\
               .filter(MT_ambientes.MT_ABestado == 1, MT_ambientes.MT_Aid==area,MT_asig_et_fn.MT_AEFestado==1,
                                                  ~MT_asig_funciones.query.filter(
                                                      MT_asig_funciones.MT_AEFid == MT_asig_et_fn.MT_AEFid,
                                                      MT_asig_funciones.MT_ASFestado == 1,
                                                      MT_asig_funciones.Uid == id).exists()) \
               .add_columns(MT_etiquetas.MT_Enombre, MT_ambientes.MT_ABnombre, MT_asig_et_fn.MT_AEFid).order_by(MT_ambientes.MT_ABnombre.asc()).all()

           # pendientes = MT_ambientes.query.join(MT_asig_et_fn, MT_asig_et_fn.MT_Abcodigo == MT_ambientes.MT_Abcodigo)\
           #     .filter(MT_ambientes.MT_Aid==area)
           print(pendientes)
           db.session.remove()
           return render_template('Mantenimiento/Asig_Trabajo/Asignacion.html', asignados=data2, id=id,
                                  areas=data1,  pendientes=pendientes)
       except Exception as e:
           flash('Error al buscar funciones: ' + str(e), 'danger')
           return redirect(url_for('R2V0X2FzaWduYWRvX3RyYWJham8', id=id))
    db.session.remove()
    return render_template('Mantenimiento/Asig_Trabajo/Asignacion.html',  asignados=data2, id=id, areas=data1)

def Create_asignado_trabajo(id, aefid):
    now = datetime.now(pytz.timezone('America/Lima'))
    fecha = now.strftime('%Y-%m-%d %H:%M:%S.000000')
    try:
        b = MT_asig_funciones.query.filter_by(Uid =id, MT_AEFid =aefid).first()
        if b is not None:
            b.MT_ASFestado = 1
            b.MT_ASFfech_crea = str(fecha)
            b.MT_ASFfech_asigdesde = request.form['desde']
            b.MT_ASFfech_asighasta = request.form['hasta']
        else:
            usuario = id
            ambiente = int(aefid)
            estado = 1
            fecha_crea = str(fecha)
            desde = request.form['desde']
            hasta = request.form['hasta']
            contador = 0
            new_insert = MT_asig_funciones(usuario, ambiente, estado, fecha_crea, desde, hasta, contador)
            db.session.add(new_insert)
        db.session.commit()
        flash('Asignado completamente', 'success')
        db.session.remove()
        return redirect(url_for('R2V0X2FzaWduYWRvX3RyYWJham8', id=id))
    except Exception as e:
        flash('Error al vincular: ' + str(e), 'danger')
        return redirect(url_for('R2V0X2FzaWduYWRvX3RyYWJham8', id=id))

def delete_eliminar_asignado(id, aid):
    try:
        consulta = MT_asig_funciones.query.filter_by(MT_ASFid=aid).first()
        consulta.MT_ASFestado = 2
        db.session.commit()
        flash('Asignacion eliminado con éxito', 'success')
        db.session.remove()
        return redirect(url_for('R2V0X2FzaWduYWRvX3RyYWJham8', id=id))
    except Exception as e:
        flash('Error al tratar de eliminar: ' + str(e), 'danger')
        return redirect(url_for('R2V0X2FzaWduYWRvX3RyYWJham8', id=id))