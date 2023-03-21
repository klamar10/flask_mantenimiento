from app import app
from flask_mail import Mail
from functions.Login import Init, Login, Logout, check_habilitado, check_token, check_admin

from flask import Flask

# app = Flask(__name__)

from functions.Usuarios import Lis_Usuarios, create, get_usuario, update, accesos, create_accesos, delete_accesos
from functions.config import List_Configuracion, Create_Configuracion, Get_Configuracion, Update_Configuracion
from functions.empresas import List_Empresas, create_Empresas, get_empresa, update_empresa

# MANTENIMIENTO
from functions.Mantenimiento.Areas import List_Areas, Create_Area, get_area, update_MT_area
from functions.Mantenimiento.Ambientes import List_Ambientes, Create_Ambiente, Get_ambiente, Update_MT_ambiente, Get_ambiente_V, Create_Vincular, delete_Desvincular
from functions.Mantenimiento.EtiquetasFunciones import List_EtiquetasFunciones, List_Etiquetas, List_Funciones, \
    Create_Etiqueta, Get_etiqueta, Update_Etiqueta, Create_Funciones, Get_funcion, Update_Funcion, \
    Create_Asignacion, Get_FuncionesxEtiqueta, delete_FuncionesxEtiqueta
from functions.Mantenimiento.Trabajo import List_Asignados, Get_asignado_trabajo, Create_asignado_trabajo, delete_eliminar_asignado
from functions.Mantenimiento.Asignado import List_Asignaciones,asignado_id
from functions.Mantenimiento.Reportes import List_Reporte, List_Reporte2, List_Reporte3, Detaller_Reporte2,reporte_excel_RxT,Detaller_Reporte3,ReporteTotal3

# from functions.Mantenimiento.Asignado import List_Asignaciones, asignado_id

# REPORTE
# from functions.Mantenimiento.Reportes import List_Reporte, reporte_excel_RxT, List_Reporte2, Detaller_Reporte2, List_Reporte3, Detaller_Reporte3, ReporteTotal3
# CONEXION
from Models.Tables import db
mail = Mail()

# # CONFIGURACIONES
@app.route('/Configuracion')
@check_token
@check_admin
def TGlzdF9Db25maQ():
    return List_Configuracion()


@app.route('/Registrar_configuracion', methods=['POST'])
@check_token
@check_habilitado
@check_admin
def Q3JlYXRlX0NvbmZp():
    return Create_Configuracion()


@app.route('/Editar_Configuracion/<string:id>')
@check_token
@check_admin
def R2V0X0NvbmZp(id):
    return Get_Configuracion(id)


@app.route('/Actualizar_Configuracion/<string:id>', methods=['GET', 'POST'])
@check_token
@check_habilitado
@check_admin
def VXBkYXRlX0NvbmZp(id):
    return Update_Configuracion(id)


# # LOGIN
@app.route('/')
def SW5pdA():
    return Init()


@app.route('/Login', methods=['GET', 'POST'])
def TG9naW4():
    return Login()


@app.route('/Logout')
def TG9nb3V0():
    return Logout()

#
# # EMPRESAS
@app.route('/Empresas')
@check_token
@check_admin
def TGlzdF9FbXByZXNhcw():
    return List_Empresas()


@app.route('/Registrar_Empresa', methods=['POST'])
@check_token
@check_habilitado
@check_admin
def Y3JlYXRlX0VtcHJlc2Fz():
    return create_Empresas()


@app.route('/Editar_Empresa/<string:id>')
@check_token
@check_admin
def Z2V0X2VtcHJlc2E(id):
    return get_empresa(id)


@app.route('/Update_Empresa/<string:id>', methods=['POST'])
@check_token
@check_habilitado
@check_admin
def dXBkYXRlX2VtcHJlc2E(id):
    return update_empresa(id)
#
#
# # USUARIOS
@app.route('/Usuarios')
@check_token
@check_admin
def VXN1YXJpb3M():
    return Lis_Usuarios()


@app.route('/Registrar_usuario', methods=['POST'])
@check_token
@check_habilitado
@check_admin
def Y3JlYXRl():
    return create()


@app.route('/Editar_Usuario/<string:id>')
@check_token
@check_habilitado
@check_admin
def Z2V0X3VzdWFyaW8(id):
    return get_usuario(id)


@app.route('/Update_Usuario/<id>', methods=['POST'])
@check_token
@check_habilitado
@check_admin
def dXBkYXRl(id):
    return update(id)


#
# @app.route('/Eliminar_usuario/<string:id>')
# @check_token
# @check_rol
# @check_rol_admin
# def ZGVsZXRl(id):
#     return delete(id)
#
@app.route('/Accesos_Usuario/<string:id>')
@check_token
@check_admin
def YWNjZXNvcw(id):
    return accesos(id)


#
@app.route('/Asignar_Acceso/<id>', methods=['POST'])
@check_token
@check_habilitado
@check_admin
def Y3JlYXRlX2FjY2Vzb3M(id):
    return create_accesos(id)


@app.route('/Eliminar_Acceso/<string:id>/<string:aid>/<string:rid>')
@check_token
@check_habilitado
@check_admin
def ZGVsZXRlX2FjY2Vzb3M(id, aid, rid):
    return delete_accesos(id, aid, rid)

#
#
# # -------------------------------ETIQUETAS**------------------------------*
@app.route('/Etiquetas-funciones')
@check_token
@check_habilitado
@check_admin
def TGlzdF9FdGlxdWV0YXNGdW5jaW9uZXM():
    return List_EtiquetasFunciones()


@app.route('/Etiquetas-funciones/Etiquetas')
@check_token
@check_habilitado
@check_admin
def TGlzdF9FdGlxdWV0YXM():
    return List_Etiquetas()


@app.route('/Etiquetas-funciones/Funciones')
@check_token
@check_habilitado
@check_admin
def TGlzdF9GdW5jaW9uZXM():
    return List_Funciones()
#
#
# # ETIQUETA
@app.route('/Registrar-etiqueta', methods=['POST'])
@check_token
@check_habilitado
@check_admin
def Q3JlYXRlX0V0aXF1ZXRh():
    return Create_Etiqueta()


@app.route('/Etiquetas-funciones/Editar_etiqueta/<string:id>')
@check_token
@check_admin
def R2V0X2V0aXF1ZXRh(id):
    return Get_etiqueta(id)


@app.route('/Etiquetas-funciones/Update_etiqueta/<id>', methods=['POST'])
@check_token
@check_habilitado
@check_admin
def VXBkYXRlX0V0aXF1ZXRh(id):
    return Update_Etiqueta(id)
#
#
# # FUNCION
@app.route('/Etiquetas-funciones/Registrar-funcion', methods=['POST'])
@check_token
@check_habilitado
@check_admin
def Q3JlYXRlX0Z1bmNpb25lcw():
    return Create_Funciones()


@app.route('/Etiquetas-funciones/Editar_funcion/<string:id>')
@check_token
@check_admin
def R2V0X2Z1bmNpb24(id):
    return Get_funcion(id)


@app.route('/Etiquetas-funciones/Update_funcion/<id>', methods=['POST'])
@check_token
@check_habilitado
@check_admin
def VXBkYXRlX0Z1bmNpb24(id):
    return Update_Funcion(id)

#
# # ASIGNACION
@app.route('/Etiquetas-funciones/Asignaciones/<string:id>')
@check_token
@check_admin
def R2V0X0Z1bmNpb25lc3hFdGlxdWV0YQ(id):
    return Get_FuncionesxEtiqueta(id)


@app.route('/Etiquetas-funciones/Eliminar_asignacion/<string:id>/<string:eid>')
@check_token
@check_habilitado
@check_admin
def ZGVsZXRlX0Z1bmNpb25lc3hFdGlxdWV0YQ(id, eid):
    return delete_FuncionesxEtiqueta(id, eid)


@app.route('/Etiquetas-funciones/Asignar-funcion/<string:id>/<string:fid>')
@check_token
@check_habilitado
@check_admin
def Q3JlYXRlX0FzaWduYWNpb24(id, fid):
    return Create_Asignacion(id, fid)
# # ------------------------------************------------------------------*
# # ------------------------------************------------------------------*
# # ------------------------------************------------------------------*
# # ------------------------------************------------------------------*
# # ------------------------------MANTENIMIENTO-----------------------------*
#
#
@app.route('/Mantenimiento/Areas')
@check_token
@check_admin
def TGlzdF9BcmVhcw():
    return List_Areas()


@app.route('/Mantenimiento/Registrar_MT_area', methods=['POST'])
@check_token
@check_habilitado
@check_admin
def Q3JlYXRlX0FyZWE():
    return Create_Area()


@app.route('/Mantenimiento/Editar_MT_area/<string:id>')
@check_token
@check_admin
def Z2V0X2FyZWE(id):
    return get_area(id)


@app.route('/Mantenimiento/Update_MT_area/<id>', methods=['POST'])
@check_token
@check_habilitado
@check_admin
def dXBkYXRlX1NnX2FyZWE(id):
    return update_MT_area(id)
#
# # -------AMBIENTES----------
#
@app.route('/Mantenimiento/Ambientes')
@check_token
@check_admin
def TGlzdF9BbWJpZW50ZXM():
    return List_Ambientes()


@app.route('/Mantenimiento/Registrar_MT_Ambiente', methods=['POST'])
@check_token
@check_habilitado
@check_admin
def Q3JlYXRlX0FtYmllbnRl():
    return Create_Ambiente()


@app.route('/Mantenimiento/Editar_MT_Ambiente/<string:id>')
@check_token
@check_admin
def R2V0X2FtYmllbnRl(id):
    return Get_ambiente(id)


@app.route('/Mantenimiento/Update_MT_Ambiente/<id>', methods=['POST'])
@check_token
@check_habilitado
@check_admin
def VXBkYXRlX1NnX2FtYmllbnRl(id):
    return Update_MT_ambiente(id)

@app.route('/Mantenimiento/Asignaciones/<string:id>')
@check_token
@check_admin
def R2V0X2FtYmllbnRlX1Y(id):
    return Get_ambiente_V(id)

@app.route('/Mantenimiento/Asignaciones/Vincular/<string:id>/<string:eid>' )
@check_token
@check_habilitado
@check_admin
def Q3JlYXRlX1ZpbmN1bGFy(id,eid):
    return Create_Vincular(id,eid)
@app.route('/Mantenimiento/Asignaciones/Desvincular/<string:id>/<string:eid>')
@check_token
@check_habilitado
@check_admin
def ZGVsZXRlX0Rlc3ZpbmN1bGFy(id, eid):
    return delete_Desvincular(id, eid)
#
# # -------TRABAJO----------
#
@app.route('/Mantenimiento/Asignados_Trabajo')
@check_token
@check_admin
def TGlzdF9Bc2lnbmFkb3M():
    return List_Asignados()

@app.route('/Mantenimiento/Asignados_Trabajo/Asignaciones/<string:id>', methods=['GET', 'POST'])
@check_token
@check_admin
def R2V0X2FzaWduYWRvX3RyYWJham8(id):
    return Get_asignado_trabajo(id)

@app.route('/Mantenimiento/Asignados_Trabajo/Asignar/<string:id>/<string:aid>', methods=[ 'POST'])
@check_token
@check_habilitado
@check_admin
def UjJWMFgyRnphV2R1WVdSdlgzUnlZV0poYW04(id, aid):
    return Create_asignado_trabajo(id,aid)

@app.route('/Mantenimiento/Asignados_Trabajo/Eliminar/<string:id>/<string:eid>')
@check_token
@check_habilitado
@check_admin
def ZGVsZXRlX2VsaW1pbmFyX2FzaWduYWRv(id, eid):
    return delete_eliminar_asignado(id, eid)
#
# # -------TRABAJO ASIGNADO----------
#
@app.route('/Mantenimiento/Asignaciones', methods=['GET', 'POST'])
@check_token
@check_habilitado
def TGlzdF9Bc2lnbmFjaW9uZXM():
    return List_Asignaciones()

@app.route('/Mantenimiento/Asignaciones/Respuesta/<string:id>', methods=['GET', 'POST'])
@check_token
@check_habilitado
def YXNpZ25hZG9faWQ(id):
    return asignado_id(id)

# ------------------------------************------------------------------*
# ------------------------------************------------------------------*
# ------------------------------************------------------------------*
# ------------------------------************------------------------------*
# ---------------------------------REPORTE--------------------------------*

@app.route('/Mantenimiento/Reportes/Reporte_Trabajador', methods=['GET', 'POST'])
@check_token
@check_admin
def TGlzdF9SZXBvcnRl():
    return List_Reporte()

@app.route('/Mantenimiento/Reportes/Reporte_Trabajador/Excel')
@check_token
@check_admin
def reporte_excel_RxTs():
    return reporte_excel_RxT()

@app.route('/Mantenimiento/Reportes/Reporte_Ambientes', methods=['GET', 'POST'])
@check_token
@check_admin
def TGlzdF9SZXBvcnRlMg():
    return List_Reporte2()

@app.route('/Mantenimiento/Asignaciones/Reporte_Ambientes/<string:id>', methods=['GET', 'POST'])
@check_token
@check_admin
def RGV0YWxsZXJfUmVwb3J0ZTMy(id):
    return Detaller_Reporte2(id)

@app.route('/Mantenimiento/Reportes/Reporte_Indicadores', methods=['GET', 'POST'])
@check_token
@check_admin
def ReporteIndicadores():
    return List_Reporte3()
@app.route('/Mantenimiento/Reportes/Reporte_Indicadores/Export', methods=['GET', 'POST'])
@check_token
@check_admin
def Detaller_Reporte3s():
    return Detaller_Reporte3()
@app.route('/Mantenimiento/Reportes/Reporte_Indicadores/Indicadores', methods=['GET', 'POST'])
@check_token
@check_admin
def ReporteTotal3s():
    return ReporteTotal3()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()