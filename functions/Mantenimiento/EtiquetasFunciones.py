from flask import jsonify, render_template, request, redirect, flash, session, url_for
from datetime import datetime
# MODELOS
from Models.Tables import MT_etiquetas, MT_funciones, MT_eti_fn
from Models.Tables import MT_areas
from Models.Tables import Configuraciones, UAR_accesos, Areas, Roles
from Models.Tables import db

consulta = bool


# PAGINAS
def List_EtiquetasFunciones():
    try:
        return render_template('Mantenimiento/EtiquetasFunciones/List.html')
    except Exception as e:
        db.session.rollback()
        flash('Error al mostrar página. ' + str(e), 'danger')
        return redirect(url_for('SW5pdA'))

def List_Etiquetas():
    try:
        # AREAS
        data1 = MT_etiquetas.query.filter_by().order_by(MT_etiquetas.MT_Enombre.asc())
        db.session.remove()
        return render_template('Mantenimiento/EtiquetasFunciones/Etiquetas.html', etiquetas=data1)
    except Exception as e:
        db.session.rollback()
        flash('Error al mostrar página. ' + str(e), 'danger')
        return redirect(url_for('SW5pdA'))


def List_Funciones():
    try:
        # AREAS
        data1 = MT_funciones.query.filter_by().order_by(MT_funciones.MT_Fnombre.asc())
        db.session.remove()
        return render_template('Mantenimiento/EtiquetasFunciones/Funciones.html', funciones=data1)
    except Exception as e:
        flash('Error al mostrar página. ' + str(e), 'danger')
        return redirect(url_for('SW5pdA'))


# ETIQUETAS
def Create_Etiqueta():
    now = datetime.now()
    fecha = now.strftime('%Y-%m-%d %H:%M:%S.000000')
    if request.method == 'POST':
        try:
            MT_Enombre = request.form['MT_Enombre']
            MT_Eestado = 1
            MT_Efech_crea = str(fecha)
            MT_Efech_mod = None
            new_insert = MT_etiquetas(MT_Enombre, MT_Eestado, MT_Efech_crea, MT_Efech_mod)
            db.session.add(new_insert)
            db.session.commit()
            flash('Etiqueta agregada: ' + MT_Enombre, 'success')
            db.session.remove()
            return redirect(url_for('TGlzdF9FdGlxdWV0YXM'))
        except Exception as e:
            flash('Error al insertar etiqueta: ' + str(e), 'danger')
            return redirect(url_for('TGlzdF9FdGlxdWV0YXM'))


def Get_etiqueta(id):
    data = MT_etiquetas.query.filter_by(MT_Eid=id).first()
    # Estado
    data2 = Configuraciones.get_estados(self=1)
    db.session.remove()
    return render_template('Mantenimiento/EtiquetasFunciones/Editar_Etiqueta.html', etiqueta=data, estados=data2)


#
def Update_Etiqueta(id):
    now = datetime.now()
    fecha = now.strftime('%Y-%m-%d %H:%M:%S')
    if request.method == 'POST':
        try:
            sga = MT_etiquetas.query.filter_by(MT_Eid=id).first()
            sga.MT_Enombre = request.form['MT_Enombre']
            sga.MT_Eestado = request.form['estado']
            sga.MT_Efech_mod = str(fecha)
            db.session.commit()
            flash('Etiqueta actualizada', 'success')
            db.session.remove()
            return redirect(url_for('TGlzdF9FdGlxdWV0YXM'))
        except Exception as e:
            flash('Error al actualizar etiqueta: ' + str(e), 'danger')
            return redirect(url_for('TGlzdF9FdGlxdWV0YXM'))


# FUNCIONES
def Create_Funciones():
    now = datetime.now()
    fecha = now.strftime('%Y-%m-%d %H:%M:%S.000000')
    if request.method == 'POST':
        try:
            MT_Fnombre = request.form['MT_Fnombre']
            MT_Festado = 1
            MT_Ffech_crea = str(fecha)
            MT_Ffech_mod = None
            new_insert = MT_funciones(MT_Fnombre, MT_Festado, MT_Ffech_crea, MT_Ffech_mod)
            print(new_insert)
            db.session.add(new_insert)
            db.session.commit()
            flash('Etiqueta agregada: ' + MT_Fnombre, 'success')
            db.session.remove()
            return redirect(url_for('TGlzdF9GdW5jaW9uZXM'))
        except Exception as e:
            print(e)
            flash('Error al insertar etiqueta: ' + str(e), 'danger')
            return redirect(url_for('TGlzdF9GdW5jaW9uZXM'))


def Get_funcion(id):
    data = MT_funciones.query.filter_by(MT_Fid=id).first()
    # Estado
    data2 = Configuraciones.get_estados(self=1)
    db.session.remove()
    return render_template('Mantenimiento/EtiquetasFunciones/Editar_Funciones.html', funcion=data, estados=data2)


#
def Update_Funcion(id):
    now = datetime.now()
    fecha = now.strftime('%Y-%m-%d %H:%M:%S')
    if request.method == 'POST':
        try:
            sga = MT_funciones.query.filter_by(MT_Fid=id).first()
            sga.MT_Fnombre = request.form['MT_Fnombre']
            sga.MT_Festado = request.form['estado']
            sga.MT_Ffech_mod = str(fecha)
            db.session.commit()
            flash('Etiqueta modificada: ' + sga.MT_Fnombre, 'success')
            db.session.remove()
            return redirect(url_for('TGlzdF9GdW5jaW9uZXM'))
        except Exception as e:
            flash('Error al actualizar función: ' + str(e), 'danger')
            return redirect(url_for('TGlzdF9GdW5jaW9uZXM'))


# ASIGNACION

def Get_FuncionesxEtiqueta(id):
    consulta = ''
    dato2 = MT_eti_fn.query.join(MT_etiquetas, MT_etiquetas.MT_Eid == MT_eti_fn.MT_Eid) \
        .join(MT_funciones, MT_funciones.MT_Fid == MT_eti_fn.MT_Fid) \
        .add_columns(MT_funciones.MT_Fid, MT_eti_fn.MT_EFid, MT_funciones.MT_Fnombre, MT_eti_fn.MT_EFfech_crea, MT_eti_fn.MT_EFestado) \
        .filter(MT_etiquetas.MT_Eid == id, MT_funciones.MT_Festado ==1, MT_eti_fn.MT_EFestado == 1)\
        .order_by(MT_funciones.MT_Fnombre.asc()).all()
    dato3 = MT_funciones.query.filter(MT_funciones.MT_Festado == 1,
                                      ~MT_eti_fn.query.filter(MT_eti_fn.MT_Fid == MT_funciones.MT_Fid,
                                                              MT_eti_fn.MT_Eid == id, MT_eti_fn.MT_EFestado == 1).exists()).order_by(MT_funciones.MT_Fnombre.asc()).all()
    return render_template('Mantenimiento/EtiquetasFunciones/AsigEF_busqueda.html', asignados=dato2, funciones=dato3,
                           id=id)

def delete_FuncionesxEtiqueta(id, eid):
    try:
        consulta = MT_eti_fn.query.filter_by(MT_EFid=id).first()
        if consulta.MT_EFestado == 1:
            consulta.MT_EFestado = 2
            flash('Asignacion deshabilitado con éxito', 'success')
        else:
            consulta.MT_EFestado = 1
            flash('Asignacion Habilitado con éxito', 'success')
        # db.session.delete(consulta)
        db.session.commit()
        db.session.remove()
        return redirect(url_for('R2V0X0Z1bmNpb25lc3hFdGlxdWV0YQ', id=eid))
    except Exception as e:
        flash('Error al tratar de eliminar: ' + str(e), 'danger')
        return redirect(url_for('R2V0X0Z1bmNpb25lc3hFdGlxdWV0YQ', id=id))


def Create_Asignacion(id, fid):
    now = datetime.now()
    fecha = now.strftime('%Y-%m-%d %H:%M:%S.000000')
    try:
        b = MT_eti_fn.query.filter_by(MT_Eid=id, MT_Fid=fid).first()
        if b is not None:
            b.MT_EFestado = 1
        else:
            etiqueta = id
            funcion = fid
            estado = 1
            fecha_crea = str(fecha)
            fech_mod = None
            new_insert = MT_eti_fn(etiqueta, funcion, estado, fecha_crea, fech_mod)
            db.session.add(new_insert)
        db.session.commit()
        flash('Asignacion completa', 'success')
        db.session.remove()
        return redirect(url_for('R2V0X0Z1bmNpb25lc3hFdGlxdWV0YQ', id=id))
    except Exception as e:
        flash('Error al agregar funcion: ' + str(e), 'danger')
        return redirect(url_for('R2V0X0Z1bmNpb25lc3hFdGlxdWV0YQ', id=id))
