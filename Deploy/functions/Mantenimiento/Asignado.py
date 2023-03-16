from flask import jsonify, render_template, request, redirect, flash, session, url_for
from datetime import datetime
# MODELOS
from Models.Tables import MT_asig_funciones, MT_areas, MT_ambientes, MT_asig_et_fn, MT_eti_fn, MT_funciones, \
    MT_funcion_resp, MT_etiquetas
from Models.Tables import db


def List_Asignaciones():
    trabajador = session['Uid']
    select = MT_areas.query.filter(MT_areas.MT_Aestado ==1, MT_asig_et_fn.query.join(MT_asig_funciones, MT_asig_funciones.MT_AEFid == MT_asig_et_fn.MT_AEFid).join(
        MT_ambientes, MT_ambientes.MT_Abcodigo == MT_asig_et_fn.MT_Abcodigo).join(MT_areas,
                                                                                  MT_areas.MT_Aid == MT_ambientes.MT_Aid).exists()).order_by(MT_areas.MT_Anombre.asc()).all()

    if request.method == 'POST':
        area = request.form['area']
        data = MT_asig_et_fn.query.join(MT_asig_funciones, MT_asig_funciones.MT_AEFid == MT_asig_et_fn.MT_AEFid).join(
            MT_ambientes, MT_ambientes.MT_Abcodigo == MT_asig_et_fn.MT_Abcodigo).join(MT_areas,
                                                                                      MT_areas.MT_Aid == MT_ambientes.MT_Aid).join(MT_etiquetas, MT_etiquetas.MT_Eid == MT_asig_et_fn.MT_Eid) \
            .add_columns(MT_asig_funciones.MT_ASFid, MT_ambientes.MT_ABnombre, MT_asig_funciones.MT_ASFcontador, MT_etiquetas.MT_Enombre)\
            .filter(MT_areas.MT_Aestado == 1,
                                                                      MT_ambientes.MT_ABestado == 1,
                                                                      MT_asig_funciones.MT_ASFestado == 1,
                                                                      MT_asig_funciones.Uid == trabajador,
                                                                      MT_ambientes.MT_Aid == area) \
            .order_by(MT_areas.MT_Anombre.asc()).all()
        db.session.remove()
        return render_template('Mantenimiento/Trabajo/List.html', select=select, ambientes=data)

    db.session.remove()
    return render_template('Mantenimiento/Trabajo/List.html', select=select)


def asignado_id(id):
    now = datetime.now()
    fecha = now.strftime('%Y-%m-%d %H:%M:%S')
    try:
        if request.method == 'POST':
            try:
                # INSERTAR
                MT_ASFid = id
                MT_FRRespuesta = request.form['MT_FRRespuesta']
                MT_FRcomentario = request.form['MT_FRcomentario']
                MT_ASFfech_crea = str(fecha)
                new_insert = MT_funcion_resp(MT_ASFid, MT_FRRespuesta, MT_FRcomentario, MT_ASFfech_crea)
                db.session.add(new_insert)

                # ACTUALIZAR
                asig_funciones = MT_asig_funciones.query.filter_by(MT_ASFid=id).first()
                asig_funciones.MT_ASFcontador = int(asig_funciones.MT_ASFcontador) + 1

                db.session.commit()
                flash('Tarea Registrada', 'success')
                db.session.remove()
                return redirect(url_for('TGlzdF9Bc2lnbmFjaW9uZXM'))
            except Exception as e:
                flash('Error al registrar. ' + str(e), 'danger')
                return render_template('Mantenimiento/Trabajo/List.html')

        data = MT_funciones.query.join(MT_eti_fn, MT_eti_fn.MT_Fid == MT_funciones.MT_Fid) \
            .join(MT_asig_et_fn, MT_asig_et_fn.MT_Eid == MT_eti_fn.MT_Eid).join(MT_asig_funciones,
                                                                                MT_asig_funciones.MT_AEFid == MT_asig_et_fn.MT_AEFid) \
            .filter(MT_funciones.MT_Festado == 1, MT_eti_fn.MT_EFestado == 1, MT_asig_et_fn.MT_AEFestado == 1,
                    MT_asig_funciones.MT_ASFestado == 1, MT_asig_funciones.MT_ASFid == id).all()
        db.session.remove()

        return render_template('Mantenimiento/Trabajo/Respuesta.html', funciones=data, id=id)
    except Exception as e:
        flash('Error al mostrar página. ' + str(e), 'danger')
        return redirect(url_for('SW5pdA'))
