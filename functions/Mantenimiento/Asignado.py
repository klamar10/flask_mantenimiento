from flask import jsonify, render_template, request, redirect, flash, session, url_for
from datetime import datetime
from Configuracion.db import mysql
# MODELOS
from Models.Tables import MT_asig_funciones, MT_areas, MT_ambientes, MT_asig_et_fn, MT_eti_fn, MT_funciones, \
    MT_funcion_resp, MT_etiquetas
from Models.Tables import db
from sqlalchemy import func
from sqlalchemy import distinct
def List_Asignaciones():
    trabajador = session['Uid']
    now = datetime.now()
    fecha = now.strftime('%Y%m%d')
    cur = mysql.connection.cursor()
    cur.callproc("usp_listarAreas_asig", [trabajador, fecha])
    select = list(cur.fetchall())
    cur.close()
    if request.method == 'POST':
        print(request.form['area'])
        try:
            area = request.form['area']
            cur = mysql.connection.cursor()
            cur.callproc("usp_listarAsignaciones", [area, fecha, trabajador])
            print(area, fecha, trabajador)
            data = list(cur.fetchall())
            cur.close()
            return render_template('Mantenimiento/Trabajo/List.html', select=select, ambientes=data)
        except Exception as e:
            flash('Error ' + str(e), 'danger')
            return render_template('Mantenimiento/Trabajo/List.html')
    return render_template('Mantenimiento/Trabajo/List.html', select=select)


def asignado_id(id):
    now = datetime.now()
    fecha = now.strftime('%Y-%m-%d %H:%M:%S')
    fecha2 = now.strftime('%Y%m%d')
    try:
        if request.method == 'POST':
            try:
                # INSERTAR
                MT_ASFid = id
                MT_FRRespuesta = 'Si'
                MT_FRcomentario = 'Se realizó todas las funciones'
                MT_ASFfech_crea = str(fecha)

                new_insert = MT_funcion_resp(MT_ASFid, MT_FRRespuesta, MT_FRcomentario, MT_ASFfech_crea)
                print(new_insert)
                db.session.add(new_insert)
                db.session.commit()
                flash('Tarea Registrada', 'success')
                db.session.remove()
                db.session.close_all()
                return redirect(url_for('TGlzdF9Bc2lnbmFjaW9uZXM'))
            except Exception as e:
                print(e)
                flash('Error al registrar. ' + str(e), 'danger')
                return render_template('Mantenimiento/Trabajo/List.html')
                # ACTUALIZAR
                # asig_funciones = MT_asig_funciones.query.filter_by(MT_ASFid=id).first()
                # asig_funciones.MT_ASFcontador = int(asig_funciones.MT_ASFcontador) + 1


            # except Exception as e:
            #     flash('Error al registrar. ' + str(e), 'danger')
            #     return render_template('Mantenimiento/Trabajo/List.html')

        data = MT_funciones.query.join(MT_eti_fn, MT_eti_fn.MT_Fid == MT_funciones.MT_Fid) \
            .join(MT_asig_et_fn, MT_asig_et_fn.MT_Eid == MT_eti_fn.MT_Eid).join(MT_asig_funciones,
                                                                                MT_asig_funciones.MT_AEFid == MT_asig_et_fn.MT_AEFid) \
            .filter(MT_funciones.MT_Festado == 1, MT_eti_fn.MT_EFestado == 1, MT_asig_et_fn.MT_AEFestado == 1,
                    MT_asig_funciones.MT_ASFestado == 1, MT_asig_funciones.MT_ASFid == id).all()

        query = db.session.query(func.count(MT_funcion_resp.MT_ASFid)).filter(MT_funcion_resp.MT_ASFid==id, MT_funcion_resp.MT_ASFfech_crea>=fecha2).scalar()
        print(query)
        contador=query
        db.session.remove()

        return render_template('Mantenimiento/Trabajo/Respuesta.html', funciones=data, id=id, contador=contador)
    except Exception as e:
        flash('Error al mostrar página. ' + str(e), 'danger')
        return redirect(url_for('SW5pdA'))
