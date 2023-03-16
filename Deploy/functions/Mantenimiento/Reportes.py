from Models.Tables import Usuarios, MT_asig_funciones, MT_ambientes, MT_areas, MT_asig_et_fn, MT_eti_fn, MT_funciones, \
    MT_funcion_resp, MT_etiquetas
from flask import url_for, render_template, request, redirect, flash, session, Response
from Models.Tables import db
import io
import xlwt


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
            .join(MT_funciones, MT_funciones.MT_Fid == MT_eti_fn.MT_EFid) \
            .join(MT_ambientes, MT_ambientes.MT_Abcodigo == MT_asig_et_fn.MT_Abcodigo) \
            .join(MT_areas, MT_areas.MT_Aid == MT_ambientes.MT_Aid) \
            .filter(MT_funcion_resp.MT_ASFfech_crea >= inicio, MT_funcion_resp.MT_ASFfech_crea <= fin,
                    MT_asig_funciones.Uid == trabajador) \
            .add_columns(MT_areas.MT_Anombre, MT_ambientes.MT_ABnombre, MT_funciones.MT_Fnombre,
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
            .join(MT_funciones, MT_funciones.MT_Fid == MT_eti_fn.MT_EFid) \
            .join(MT_ambientes, MT_ambientes.MT_Abcodigo == MT_asig_et_fn.MT_Abcodigo) \
            .join(MT_areas, MT_areas.MT_Aid == MT_ambientes.MT_Aid) \
            .filter(MT_funcion_resp.MT_ASFfech_crea >= inicio, MT_funcion_resp.MT_ASFfech_crea <= fin,
                    MT_asig_funciones.Uid == trabajador) \
            .add_columns(MT_areas.MT_Anombre, MT_ambientes.MT_ABnombre, MT_funciones.MT_Fnombre,
                         MT_funcion_resp.MT_ASFfech_crea, MT_funcion_resp.MT_FRRespuesta,
                         MT_funcion_resp.MT_FRcomentario).order_by(MT_funcion_resp.MT_ASFfech_crea.asc()).all()
        db.session.remove()

        output = io.BytesIO()
        wk = xlwt.Workbook()
        sh = wk.add_sheet('Reporte de trabajo')

        sh.write(0, 0, 'Area')
        sh.write(0, 1, 'Ambiente')
        sh.write(0, 2, 'Funcion')
        sh.write(0, 3, 'Fecha de registro')
        sh.write(0, 4, 'Respuesta')
        sh.write(0, 5, 'Comentario')

        idx = 0

        for row in consulta:
            sh.write(idx + 1, 0, str(row['MT_Anombre']))
            sh.write(idx + 1, 1, str(row['MT_ABnombre']))
            sh.write(idx + 1, 2, str(row['MT_Fnombre']))
            sh.write(idx + 1, 3, str(row['MT_ASFfech_crea']))
            sh.write(idx + 1, 4, str(row['MT_FRRespuesta']))
            sh.write(idx + 1, 5, str(row['MT_FRcomentario']))

            idx += 1
        wk.save(output)
        output.seek(0)
        return Response(output, mimetype="application/ms-excel",
                        headers={"Content-Disposition": "attchment;filename=Reporte_Trabajador.xls"})

    except:
        flash('Realizar una consulta para poder exportar', 'danger')
        return redirect(url_for('TGlzdF9SZXBvcnRl'))


#

def List_Reporte2():
    data1 = MT_areas.query.filter_by(MT_Aestado=1).all()
    if request.method == 'POST':
        area = request.form['area']
        inicio = request.form['inicio']
        fin = request.form['fin']

        session['rparea'] = area
        session['rpinicio'] = inicio
        session['rpfin'] = fin

        consulta = MT_areas.query.join(MT_ambientes, MT_ambientes.MT_Aid == MT_areas.MT_Aid)\
            .join(MT_asig_et_fn, MT_asig_et_fn.MT_Abcodigo == MT_ambientes.MT_Abcodigo)\
            .add_columns(MT_ambientes.MT_ABnombre, MT_ambientes.MT_Abcodigo) \
            .filter(MT_areas.MT_Aid == area).order_by(MT_ambientes.MT_ABnombre.desc()).all()
        db.session.remove()
        return render_template('Reportes/Mantenimiento/RptaxArea.html', areas=data1, consulta=consulta)
    db.session.remove()
    return render_template('Reportes/Mantenimiento/RptaxArea.html', areas=data1)


def Detaller_Reporte2(id):
    try:
        inicio = session['rpinicio']
        fin = session['rpfin']
        consulta = MT_ambientes.query.join(MT_asig_et_fn, MT_asig_et_fn.MT_Abcodigo == MT_ambientes.MT_Abcodigo) \
            .join(MT_asig_funciones, MT_asig_funciones.MT_AEFid == MT_asig_et_fn.MT_AEFid) \
            .join(Usuarios, Usuarios.Uid == MT_asig_funciones.Uid) \
            .join(MT_eti_fn, MT_eti_fn.MT_Eid == MT_asig_et_fn.MT_Eid) \
            .join(MT_etiquetas, MT_etiquetas.MT_Eid == MT_eti_fn.MT_Eid) \
            .join(MT_funcion_resp, MT_funcion_resp.MT_ASFid == MT_asig_funciones.MT_ASFid) \
            .filter(MT_ambientes.MT_Abcodigo == id, MT_funcion_resp.MT_ASFfech_crea >= inicio,
                    MT_funcion_resp.MT_ASFfech_crea <= fin) \
            .add_columns(MT_ambientes.MT_ABnombre, Usuarios.Unombre, Usuarios.Uapellido, MT_etiquetas.MT_Enombre,
                         MT_funcion_resp.MT_FRRespuesta, MT_funcion_resp.MT_FRcomentario, MT_funcion_resp.MT_ASFfech_crea) \
            .all()

        output = io.BytesIO()
        wk = xlwt.Workbook()
        sh = wk.add_sheet('Detalle de trabajo realizado')

        sh.write(0, 0, 'Ambiente')
        sh.write(0, 1, 'Nombre')
        sh.write(0, 2, 'Apellido')
        sh.write(0, 3, 'Etiqueta')
        sh.write(0, 4, 'Fecha de registro')
        sh.write(0, 5, 'Respuesta')
        sh.write(0, 6, 'Comentario')

        idx = 0

        for row in consulta:
            sh.write(idx + 1, 0, str(row['MT_ABnombre']))
            sh.write(idx + 1, 1, str(row['Unombre']))
            sh.write(idx + 1, 2, str(row['Uapellido']))
            sh.write(idx + 1, 3, str(row['MT_Enombre']))
            sh.write(idx + 1, 4, str(row['MT_ASFfech_crea']))
            sh.write(idx + 1, 5, str(row['MT_FRRespuesta']))
            sh.write(idx + 1, 6, str(row['MT_FRcomentario']))

            idx += 1
        wk.save(output)
        output.seek(0)

        db.session.remove()
        return Response(output, mimetype="application/ms-excel",
                        headers={"Content-Disposition": "attchment;filename=Reporte_Areas.xls"})

    except:
        flash('Realizar una consulta para poder exportar', 'danger')
        return redirect(url_for('TGlzdF9SZXBvcnRlMg'))
