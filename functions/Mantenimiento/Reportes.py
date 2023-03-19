from Models.Tables import Usuarios, MT_asig_funciones, MT_ambientes, MT_areas, MT_asig_et_fn, MT_eti_fn, MT_funciones, \
    MT_funcion_resp, MT_etiquetas
from flask import url_for, render_template, request, redirect, flash, session, Response
from Models.Tables import db
import io
import xlwt
from Configuracion.db import mysql


def List_Reporte():
    data1 = Usuarios.query.filter_by(Uestado=1).all()
    if request.method == 'POST':
        trabajador = request.form['trabajador']
        inicio = request.form['inicio']
        fin = request.form['fin']
        session['rptrabajador'] = trabajador
        session['rpinicio'] = inicio
        session['rpfin'] = fin
        consulta = MT_funcion_resp.query.join(MT_asig_funciones, MT_asig_funciones.MT_ASFid == MT_funcion_resp.MT_ASFid) \
            .join(MT_asig_et_fn, MT_asig_et_fn.MT_AEFid == MT_asig_funciones.MT_AEFid) \
            .join(MT_eti_fn, MT_eti_fn.MT_Eid == MT_asig_et_fn.MT_Eid) \
            .join(MT_etiquetas, MT_etiquetas.MT_Eid == MT_eti_fn.MT_Eid) \
            .join(MT_ambientes, MT_ambientes.MT_Abcodigo == MT_asig_et_fn.MT_Abcodigo) \
            .join(MT_areas, MT_areas.MT_Aid == MT_ambientes.MT_Aid) \
            .filter(MT_funcion_resp.MT_ASFfech_crea >= inicio, MT_funcion_resp.MT_ASFfech_crea <= fin,
                    MT_asig_funciones.Uid == trabajador) \
            .add_columns(MT_areas.MT_Anombre, MT_ambientes.MT_ABnombre, MT_etiquetas.MT_Enombre,
                         MT_funcion_resp.MT_ASFfech_crea, MT_funcion_resp.MT_FRRespuesta,
                         MT_funcion_resp.MT_FRcomentario).order_by(MT_funcion_resp.MT_ASFfech_crea.asc()).all()
        db.session.remove()
        return render_template('Reportes/Mantenimiento/RptxTrabajador.html', usuarios=data1, reporte=consulta)
    db.session.remove()
    return render_template('Reportes/Mantenimiento/RptxTrabajador.html', usuarios=data1)


def reporte_excel_RxT():
    try:
        trabajador = session['rptrabajador']
        inicio = session['rpinicio']
        fin = session['rpfin']
        consulta = MT_funcion_resp.query.join(MT_asig_funciones, MT_asig_funciones.MT_ASFid == MT_funcion_resp.MT_ASFid) \
            .join(MT_asig_et_fn, MT_asig_et_fn.MT_AEFid == MT_asig_funciones.MT_AEFid) \
            .join(MT_eti_fn, MT_eti_fn.MT_Eid == MT_asig_et_fn.MT_Eid) \
            .join(MT_etiquetas, MT_etiquetas.MT_Eid == MT_eti_fn.MT_Eid) \
            .join(MT_ambientes, MT_ambientes.MT_Abcodigo == MT_asig_et_fn.MT_Abcodigo) \
            .join(MT_areas, MT_areas.MT_Aid == MT_ambientes.MT_Aid) \
            .filter(MT_funcion_resp.MT_ASFfech_crea >= inicio, MT_funcion_resp.MT_ASFfech_crea <= fin,
                    MT_asig_funciones.Uid == trabajador) \
            .add_columns(MT_areas.MT_Anombre, MT_ambientes.MT_ABnombre, MT_etiquetas.MT_Enombre,
                         MT_funcion_resp.MT_ASFfech_crea, MT_funcion_resp.MT_FRRespuesta,
                         MT_funcion_resp.MT_FRcomentario).order_by(MT_funcion_resp.MT_ASFfech_crea.asc()).all()
        db.session.remove()

        output = io.BytesIO()
        wk = xlwt.Workbook()
        sh = wk.add_sheet('Reporte de trabajo')

        sh.write(0, 0, 'Area')
        sh.write(0, 1, 'Ambiente')
        sh.write(0, 2, 'Etiqueta')
        sh.write(0, 3, 'Fecha de registro')
        sh.write(0, 4, 'Respuesta')
        sh.write(0, 5, 'Comentario')

        idx = 0

        for row in consulta:
            print(str(row[4]))
            sh.write(idx +1, 0, row[1])
            sh.write(idx +1, 1, row[2])
            sh.write(idx +1, 2, row[3])
            sh.write(idx +1, 3, str(row[4]))
            sh.write(idx +1, 4, row[5])
            sh.write(idx +1, 5, row[6])
            idx += 1
        print(idx)
        wk.save(output)

        output.seek(0)
        return Response(output, mimetype="application/ms-excel",
                        headers={"Content-Disposition": "attchment;filename=Reporte_Trabajador.xls"})

    except Exception as e:
        print(e)
        flash('Realizar una consulta para poder exportar', 'danger')
        return redirect(url_for('TGlzdF9SZXBvcnRl'))


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////

def List_Reporte2():
    data1 = MT_areas.query.filter_by(MT_Aestado=1).all()
    if request.method == 'POST':
        area = request.form['area']
        inicio = request.form['inicio']
        fin = request.form['fin']

        session['rparea'] = area
        session['rpinicio'] = inicio
        session['rpfin'] = fin

        # consulta = MT_areas.query.join(MT_ambientes, MT_ambientes.MT_Aid == MT_areas.MT_Aid)\
        #     .join(MT_asig_et_fn, MT_asig_et_fn.MT_Abcodigo == MT_ambientes.MT_Abcodigo) \
        #     .filter(MT_areas.MT_Aid == area,
        #             MT_asig_et_fn.query.join(MT_asig_funciones, MT_asig_funciones.MT_AEFid == MT_asig_et_fn.MT_AEFid)
        #             .join(MT_funcion_resp, MT_funcion_resp.MT_ASFid == MT_asig_funciones.MT_ASFid))\
        #     .add_columns(MT_ambientes.MT_ABnombre, MT_ambientes.MT_Abcodigo).all()
        consulta = MT_areas.query.filter(MT_areas.MT_Aid == area,
                                         MT_asig_et_fn.query.join(MT_asig_funciones,
                                                                  MT_asig_funciones.MT_AEFid == MT_asig_et_fn.MT_AEFid)
                                         .join(MT_funcion_resp, MT_funcion_resp.MT_ASFid == MT_asig_funciones.MT_ASFid)
                                         .filter(
                                                 MT_funcion_resp.MT_ASFfech_crea >= inicio,
                                                 MT_funcion_resp.MT_ASFfech_crea <= fin).exists()) \
            .join(MT_ambientes, MT_ambientes.MT_Aid == MT_areas.MT_Aid) \
            .add_columns(MT_ambientes.MT_ABnombre, MT_ambientes.MT_Abcodigo).all()

        if consulta == []:
            flash('No se encontraton registros', 'warning')
        else:
            pass
        db.session.remove()
        return render_template('Reportes/Mantenimiento/RptaxArea.html', areas=data1, consulta=consulta)
    db.session.remove()
    return render_template('Reportes/Mantenimiento/RptaxArea.html', areas=data1)


def Detaller_Reporte2(id):
    try:
        inicio = session['rpinicio']
        fin = session['rpfin']
        print(id)
        consulta = MT_ambientes.query.join(MT_asig_et_fn, MT_asig_et_fn.MT_Abcodigo == MT_ambientes.MT_Abcodigo) \
            .join(MT_asig_funciones, MT_asig_funciones.MT_AEFid == MT_asig_et_fn.MT_AEFid) \
            .join(Usuarios, Usuarios.Uid == MT_asig_funciones.Uid) \
            .join(MT_eti_fn, MT_eti_fn.MT_Eid == MT_asig_et_fn.MT_Eid) \
            .join(MT_etiquetas, MT_etiquetas.MT_Eid == MT_eti_fn.MT_Eid) \
            .join(MT_funcion_resp, MT_funcion_resp.MT_ASFid == MT_asig_funciones.MT_ASFid) \
            .filter(MT_ambientes.MT_Abcodigo==id, MT_funcion_resp.MT_ASFfech_crea >= inicio,
                    MT_funcion_resp.MT_ASFfech_crea <= fin ) \
            .add_columns( MT_ambientes.MT_ABnombre, Usuarios.Unombre, Usuarios.Uapellido, MT_etiquetas.MT_Enombre,
                         MT_funcion_resp.MT_FRRespuesta, MT_funcion_resp.MT_FRcomentario,
                         MT_funcion_resp.MT_ASFfech_crea) \
            .all()
        print(consulta)
        if consulta == []:
            db.session.remove()
            flash('No se encontraton registros para exportar', 'warning')
            return redirect(url_for('TGlzdF9SZXBvcnRlMg'))
        else:
            pass
        output = io.BytesIO()
        wk = xlwt.Workbook()
        sh = wk.add_sheet('Detalle de trabajo realizado')

        sh.write(0, 0, 'Ambiente')
        sh.write(0, 1, 'Nombre')
        sh.write(0, 2, 'Apellido')
        sh.write(0, 3, 'Etiqueta')
        sh.write(0, 4, 'Respuesta')
        sh.write(0, 5, 'Comentario')
        sh.write(0, 6, 'Fecha de registro')

        idx = 0

        for row in consulta:
            sh.write(idx + 1, 0, str(row[1]))
            sh.write(idx + 1, 1, str(row[2]))
            sh.write(idx + 1, 2, str(row[3]))
            sh.write(idx + 1, 3, str(row[4]))
            sh.write(idx + 1, 4, str(row[5]))
            sh.write(idx + 1, 5, str(row[6]))
            sh.write(idx + 1, 6, str(row[7]))

            idx += 1
        wk.save(output)
        output.seek(0)

        db.session.remove()
        return Response(output, mimetype="application/ms-excel",
                        headers={"Content-Disposition": "attchment;filename=Reporte_Areas.xls"})

    except:
        flash('Realizar una consulta para poder exportar', 'danger')
        return redirect(url_for('TGlzdF9SZXBvcnRlMg'))


def List_Reporte3():
    if request.method == 'POST':
        fini = request.form['inicio']
        ffin = request.form['fin']
        session['rpinicio'] = fini
        session['rpfin'] = ffin
        # consulta = MT_funcion_resp.query\
        #     .join(MT_asig_funciones, MT_asig_funciones.MT_ASFid == MT_funcion_resp.MT_ASFid)\
        #     .join(Usuarios, Usuarios.Uid == MT_asig_funciones.Uid)\
        #     .join(MT_asig_et_fn, MT_asig_et_fn.MT_AEFid == MT_asig_funciones.MT_AEFid)\
        #     .join(MT_ambientes, MT_ambientes.MT_Abcodigo == MT_asig_et_fn.MT_Abcodigo)\
        #     .join(MT_areas, MT_areas.MT_Aid == MT_ambientes.MT_Aid).filter(MT_asig_funciones.MT_ASFfech_asigdesde >= fini, MT_asig_funciones.MT_ASFfech_asighasta <= ffin)\
        #         .add_columns(MT_areas.MT_Anombre, MT_ambientes.MT_ABnombre, Usuarios.Unombre, Usuarios.Uapellido, MT_funcion_resp.MT_FRRespuesta, MT_funcion_resp.MT_ASFfech_crea)\
        #     .order_by(MT_ambientes.MT_ABnombre.asc()).all()
        #
        # consulta2 = db.session.query(MT_asig_funciones).join(MT_funcion_resp, isouter=True)\
        #     .join(MT_asig_et_fn, MT_asig_et_fn.MT_AEFid == MT_asig_funciones.MT_AEFid)\
        #     .join(MT_ambientes, MT_ambientes.MT_Abcodigo == MT_asig_et_fn.MT_Abcodigo)\
        #     .add_columns(MT_ambientes.MT_ABnombre, MT_funcion_resp.MT_ASFid)\
        #     .filter(MT_funcion_resp.MT_ASFid == None)
        # print(consulta2)
        # db.session.remove()
        cur = mysql.connection.cursor()

        cur.execute('''
                SELECT x.MT_Anombre, a.MT_ABnombre,f.MT_Enombre, c.MT_ASFfech_asigdesde ,c.MT_ASFfech_asighasta,
                 case when d.MT_ASFfech_crea is NULL then 'Sin atender' ELSE  d.MT_ASFfech_crea
                END,
                 CONCAT(e.Unombre , ' ' , e.Uapellido) as 'Trabajador', 
                case WHEN d.MT_FRRespuesta is Null THEN 'P' WHEN d.MT_FRRespuesta = 'NO' THEN 'OBSERVADO' WHEN d.MT_FRRespuesta = 'Si' THEN "E" END as Estado 
                FROM mt_areas x inner join mt_ambientes a on a.MT_Aid = x.MT_Aid inner join mt_asig_et_fn b on a.MT_Abcodigo = b.MT_Abcodigo 
                inner join mt_asig_funciones c on c.MT_AEFid = b.MT_AEFid 
                left join mt_funcion_resp d on d.MT_ASFid = c.MT_ASFid 
                inner join usuarios e on e.Uid = c.Uid 
                inner join mt_etiquetas f on f.MT_Eid = b.MT_Eid
                WHERE date(c.MT_ASFfech_asigdesde) >= %s and date(c.MT_ASFfech_asighasta) <= %s 
                and a.MT_ABestado = 1 and b.MT_AEFestado = 1 and f.MT_Eestado = 1
                ORDER BY c.MT_ASFfech_asighasta desc''', (fini, ffin))
        data = cur.fetchall()
        cur.close()
        return render_template('Reportes/Mantenimiento/RptaxIndicadores.html', consulta=data)
    return render_template('Reportes/Mantenimiento/RptaxIndicadores.html')


def Detaller_Reporte3():
    fini = session['rpinicio']
    ffin = session['rpfin']
    cur = mysql.connection.cursor()
    cur.execute('''
                SELECT x.MT_Anombre, a.MT_ABnombre,f.MT_Enombre, c.MT_ASFfech_asigdesde ,c.MT_ASFfech_asighasta,
                 case when d.MT_ASFfech_crea is NULL then 'Sin atender' ELSE  d.MT_ASFfech_crea
                END,
                 CONCAT(e.Unombre , ' ' , e.Uapellido) as 'Trabajador', 
                case WHEN d.MT_FRRespuesta is Null THEN 'P' WHEN d.MT_FRRespuesta = 'NO' THEN 'OBSERVADO' WHEN d.MT_FRRespuesta = 'Si' THEN "E" END as Estado 
                FROM mt_areas x inner join mt_ambientes a on a.MT_Aid = x.MT_Aid inner join mt_asig_et_fn b on a.MT_Abcodigo = b.MT_Abcodigo 
                inner join mt_asig_funciones c on c.MT_AEFid = b.MT_AEFid 
                left join mt_funcion_resp d on d.MT_ASFid = c.MT_ASFid 
                inner join usuarios e on e.Uid = c.Uid 
                inner join mt_etiquetas f on f.MT_Eid = b.MT_Eid
                WHERE date(c.MT_ASFfech_asigdesde) >= %s and date(c.MT_ASFfech_asighasta) <= %s 
                and a.MT_ABestado = 1 and b.MT_AEFestado = 1 and f.MT_Eestado = 1
                ORDER BY c.MT_ASFfech_asighasta desc''', (fini, ffin))
    consulta = cur.fetchall()
    cur.close()
    if consulta == []:
        db.session.remove()
        flash('No se encontraton registros para exportar', 'warning')
        return redirect(url_for('TGlzdF9SZXBvcnRlMg'))
    else:
        pass
    output = io.BytesIO()
    wk = xlwt.Workbook()
    sh = wk.add_sheet('Reporte de indicadores')

    sh.write(0, 0, 'Área')
    sh.write(0, 1, 'Ambiente')
    sh.write(0, 2, 'Etiqueta')
    sh.write(0, 3, 'Fecha de registro')
    sh.write(0, 4, 'Fecha de asignacion inicio')
    sh.write(0, 5, 'Fecha de asignacion fin')
    sh.write(0, 6, 'Asignado')
    sh.write(0, 7, 'Estado')

    idx = 0

    for row in consulta:
        sh.write(idx + 1, 0, str(row[0]))
        sh.write(idx + 1, 1, str(row[1]))
        sh.write(idx + 1, 2, str(row[2]))
        sh.write(idx + 1, 3, str(row[3]))
        sh.write(idx + 1, 4, str(row[4]))
        sh.write(idx + 1, 5, str(row[5]))
        sh.write(idx + 1, 6, str(row[6]))
        sh.write(idx + 1, 7, str(row[7]))

        idx += 1
    wk.save(output)
    output.seek(0)

    db.session.remove()
    return Response(output, mimetype="application/ms-excel",
                    headers={"Content-Disposition": "attchment;filename=Reporte_detalle.xls"})
def ReporteTotal3():
    fini = session['rpinicio']
    ffin = session['rpfin']
    cur = mysql.connection.cursor()
    cur.callproc("usp_reporteIndicador", [fini, ffin])
    consulta = list(cur.fetchall())
    cur.close()

    if consulta == []:
        db.session.remove()
        flash('No se encontraton registros para exportar', 'warning')
        return redirect(url_for('TGlzdF9SZXBvcnRlMg'))
    else:
        pass
    output = io.BytesIO()
    wk = xlwt.Workbook()
    sh = wk.add_sheet('Reporte de indicadores')
    # fila / columna
    sh.write(0, 0, 'Área')
    sh.write(0, 1, 'Ambiente')
    sh.write(0, 2, 'Estado de trabajo')
    sh.write(0, 3, 'Porcentaje de avance')

    sh.write(2, 8, 'Realizar un conteo del reporte de indicadores')
    sh.write(3, 7, 'Programado')
    sh.write(4, 7, 'Ejecutado')
    sh.write(5, 7, 'Avance %')

    # FORMULA
    sh.write(3, 8, '=CONTAR.SI($c$2:$c$5000;"P")')
    sh.write(4, 8, '=CONTAR.SI($c$2:$c$5000;"E")')
    sh.write(5, 8, '=($I$5/CONTAR.si(d2:d5000;"<>"))*100%')
    idx = 0

    for row in consulta:
        sh.write(idx + 1, 0, str(row[5]))
        sh.write(idx + 1, 1, str(row[4]))
        sh.write(idx + 1, 2, str(row[1]))
        sh.write(idx + 1, 3, str(row[0]))

        idx += 1
    wk.save(output)
    output.seek(0)

    db.session.remove()
    return Response(output, mimetype="application/ms-excel",
                    headers={"Content-Disposition": "attchment;filename=Reporte_Indicadores.xls"})