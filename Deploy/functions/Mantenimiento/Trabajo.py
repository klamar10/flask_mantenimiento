from flask import jsonify, render_template, request, redirect, flash, session, url_for
from datetime import datetime
# MODELOS
from Models.Tables import Usuarios, MT_asig_et_fn, MT_asig_funciones, MT_ambientes
from Models.Tables import MT_areas
from Models.Tables import Configuraciones, UAR_accesos, Areas, Roles
from Models.Tables import db

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
        .join(MT_ambientes, MT_ambientes.MT_Abcodigo == MT_asig_et_fn.MT_Abcodigo) \
        .filter(MT_asig_funciones.MT_ASFestado == 1, MT_asig_funciones.Uid == id, MT_ambientes.MT_ABestado==1) \
        .add_columns(MT_asig_funciones.MT_ASFid,MT_ambientes.MT_Abcodigo, MT_ambientes.MT_ABnombre, MT_ambientes.MT_ABfech_crea) \
        .order_by(MT_ambientes.MT_ABnombre.asc()).all()
    # //data2 = MT_asig_funciones.query.join(MT_asig_et_fn, MT_asig_et_fn.MT_AEFid == MT_asig_funciones.MT_AEFid)

    if request.method == 'POST':
       try:
           area = request.form['area']
           pendientes = MT_ambientes.query.join(MT_asig_et_fn, MT_asig_et_fn.MT_Abcodigo == MT_ambientes.MT_Abcodigo).filter(MT_ambientes.MT_ABestado == 1, MT_ambientes.MT_Aid==area,MT_asig_et_fn.MT_AEFestado==1,
                                                  ~MT_asig_funciones.query.filter(
                                                      MT_asig_funciones.MT_AEFid == MT_asig_et_fn.MT_AEFid,
                                                      MT_asig_funciones.MT_ASFestado == 1,
                                                      MT_asig_funciones.Uid == id).exists()) \
               .add_columns(MT_ambientes.MT_Abcodigo, MT_ambientes.MT_ABnombre, MT_asig_et_fn.MT_AEFid).order_by(MT_ambientes.MT_ABnombre.asc()).all()
           db.session.remove()
           return render_template('Mantenimiento/Asig_Trabajo/Asignacion.html', asignados=data2, id=id,
                                  areas=data1,  pendientes=pendientes)
       except Exception as e:
           flash('Error al buscar funciones: ' + str(e), 'danger')
           return redirect(url_for('R2V0X2FzaWduYWRvX3RyYWJham8', id=id))
    db.session.remove()
    return render_template('Mantenimiento/Asig_Trabajo/Asignacion.html',  asignados=data2, id=id, areas=data1)

def Create_asignado_trabajo(id, aid):
    now = datetime.now()
    fecha = now.strftime('%Y-%m-%d %H:%M:%S.000000')
    try:
        b = MT_asig_funciones.query.filter_by(Uid =id, MT_AEFid =aid).first()
        if b is not None:
            b.MT_ASFestado = 1
        else:
            usuario = id
            ambiente = int(aid)
            estado = 1
            fecha_crea = str(fecha)
            fech_mod = None
            contador = 0
            new_insert = MT_asig_funciones(usuario, ambiente, estado, fecha_crea, fech_mod, contador)
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