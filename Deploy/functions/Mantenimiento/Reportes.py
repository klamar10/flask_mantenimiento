from Models.Tables import Usuarios, MT_asig_funciones, MT_ambientes, MT_areas, MT_asig_et_fn, MT_eti_fn, MT_funciones, \
    MT_funcion_resp
from flask import jsonify, render_template, request, send_file, flash, session, url_for
from Models.Tables import db


def List_Reporte():
    data1 = Usuarios.query.filter_by(Uestado=1).all()
    if request.method == 'POST':
        trabajador = request.form['trabajador']
        inicio = request.form['inicio']
        fin = request.form['fin']
        session['rptrabajador'] =trabajador
        session['rpinicio'] =inicio
        session['rpfin'] =fin
        consulta = MT_funcion_resp.query.join(MT_asig_funciones, MT_asig_funciones.MT_ASFid == MT_funcion_resp.MT_ASFid) \
            .join(MT_asig_et_fn, MT_asig_et_fn.MT_AEFid == MT_asig_funciones.MT_AEFid) \
            .join(MT_eti_fn, MT_eti_fn.MT_Eid == MT_asig_et_fn.MT_Eid) \
            .join(MT_funciones, MT_funciones.MT_Fid == MT_eti_fn.MT_EFid) \
            .join(MT_ambientes, MT_ambientes.MT_Abcodigo == MT_asig_et_fn.MT_Abcodigo) \
            .join(MT_areas, MT_areas.MT_Aid == MT_ambientes.MT_Aid) \
            .filter(MT_funcion_resp.MT_ASFfech_crea >= inicio, MT_funcion_resp.MT_ASFfech_crea <= fin, MT_asig_funciones.Uid == trabajador) \
            .add_columns(MT_areas.MT_Anombre, MT_ambientes.MT_ABnombre, MT_funciones.MT_Fnombre,
                         MT_funcion_resp.MT_ASFfech_crea, MT_funcion_resp.MT_FRRespuesta,
                         MT_funcion_resp.MT_FRcomentario).order_by(MT_funcion_resp.MT_ASFfech_crea.asc()).all()
        db.session.remove()
        return render_template('Reportes/Mantenimiento/RptxTrabajador.html', usuarios=data1, reporte=consulta)
    db.session.remove()
    return render_template('Reportes/Mantenimiento/RptxTrabajador.html', usuarios=data1)

def reporte_excel_RxT():
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
    return 'ok'