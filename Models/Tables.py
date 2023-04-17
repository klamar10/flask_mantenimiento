from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from app import app
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://adrian:password@159.89.48.159/adminbd_college'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@localhost:3306/adminbd_college'

# app.config["SQLALCHEMY_DATABASE_URI"] = "mssql+pyodbc://usuario1:123@127.0.0.1/farmaco_bd?driver=SQL+Server"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://b4ba93774ba5cd:8d85ef45@us-cdbr-east-03.cleardb.com/heroku_a2320043afa4b7d'
app.config['SQLALCHEMY_POOL_RECYCLE'] = 60
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 864000
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Configuraciones(db.Model):
    Cid = db.Column(db.Integer, primary_key=True)
    Ccategoria = db.Column(db.String(30), nullable=False)
    Corden = db.Column(db.Integer, nullable=False)
    Cdescripcion = db.Column(db.String(80), nullable=False)
    Cvalor1 = db.Column(db.Integer, nullable=False)

    def __init__(self, Ccategoria, Corden, Cdescripcion, Cvalor1):
        self.Ccategoria = Ccategoria
        self.Corden = Corden
        self.Cdescripcion = Cdescripcion
        self.Cvalor1 = Cvalor1

    # OBTENER Configuracion
    def get_id(id):
        consulta = Configuraciones.query.filter_by(Cid=id).first()
        return consulta

    # OBTENER Configuracion
    def get_estados(self):
        consulta = Configuraciones.query.filter_by(Ccategoria='Estado', Cvalor1=1).all()
        return consulta


class ConfiguracionesSchema(ma.Schema):
    class Meta:
        fields = ('Cid', 'Ccategoria', 'Corden', 'Cdescripcion', 'Cvalor1')


config_sc = ConfiguracionesSchema()
config_scs = ConfiguracionesSchema(many=True)


# ------------------------------************------------------------------*
class Empresas(db.Model):
    Eid = db.Column(db.Integer, primary_key=True)
    Eruc = db.Column(db.Integer, nullable=False)
    Enombre = db.Column(db.String(100), nullable=False)
    Edepartamento = db.Column(db.String(50), nullable=False)
    Eestado = db.Column(db.Integer, nullable=False)

    def __init__(self, Eruc, Enombre, Edepartamento, Eestado):
        self.Eruc = Eruc
        self.Enombre = Enombre
        self.Edepartamento = Edepartamento
        self.Eestado = Eestado

    # OBTENER Configuracion
    def get_id(id):
        consulta = Empresas.query.filter_by(Eid=id).first()
        return consulta

    # OBTENER EMPRESAS ACTIVAS
    def get_empresas_a(self):
        consulta = Empresas.query.filter_by(Eestado=1).order_by(Empresas.Enombre.asc())
        return consulta


class Empresas_Schema(ma.Schema):
    class Meta:
        fields = ('Eid', 'Eruc', 'Enombre', 'Edepartamento', 'Eestado')


empre_sc = Empresas_Schema()
empre_scs = Empresas_Schema(many=True)


# ------------------------------************------------------------------*

class Roles(db.Model):
    Rid = db.Column(db.Integer, primary_key=True)
    Rdescripcion = db.Column(db.String(100), nullable=False)
    Restado = db.Column(db.Integer, nullable=False)

    def __init__(self, Rid, Rdescripcion, Restado):
        self.Rid = Rid
        self.Rdescripcion = Rdescripcion
        self.Restado = Restado

    # OBTENER NOMBRE DE ROL
    def get_id_rol(uid, aid):
        countries = []
        consulta = Roles.query.join(UAR_accesos, UAR_accesos.Rid == Roles.Rid) \
            .join(Usuarios, Usuarios.Uid == UAR_accesos.Uid) \
            .filter(Usuarios.Uid == uid, UAR_accesos.Aid == aid).all()
        for c in consulta:
            return c

    # OBTENER ROLES ACTIVAS
    def get_roles_a(self):
        consulta = Roles.query.filter_by(Restado=1).all()
        return consulta


class Roles_Schema(ma.Schema):
    class Meta:
        fields = ('Rid', 'Rdescripcion', 'Restado')


rol_sc = Roles_Schema()
roles_scs = Roles_Schema(many=True)


# ------------------------------************------------------------------*

class Areas(db.Model):
    Aid = db.Column(db.Integer, primary_key=True)
    Adescripcion = db.Column(db.String(60), nullable=False)
    Aestado = db.Column(db.Integer, nullable=False)

    def __init__(self, Aid, Adescripcion, Aestado):
        self.Aid = Aid
        self.Adescripcion = Adescripcion
        self.Aestado = Aestado

    # OBTENER NOMBRE DE AREA
    def get_id(id):
        consulta = Areas.query.filter_by(Aid=id).first()
        return consulta.__dict__.get('Adescripcion')

    # OBTENER AREAS ACTIVAS
    def get_area_a(self):
        consulta = Areas.query.filter_by(Aestado=1).all()
        return consulta


class Areas_Schema(ma.Schema):
    class Meta:
        fields = ('Aid', 'Adescripcion', 'Aestado')


area_sc = Areas_Schema()
areas_scs = Areas_Schema(many=True)


# ------------------------------************------------------------------*

class Usuarios(db.Model):
    Uid = db.Column(db.Integer, primary_key=True)
    Unombre = db.Column(db.String(200), nullable=False)
    Uapellido = db.Column(db.String(200), nullable=False)
    Ucorreo = db.Column(db.String(200), nullable=False, unique=True)
    Upassword = db.Column(db.String(200), nullable=False)
    Uestado = db.Column(db.Integer, nullable=False)
    Eid = db.Column(db.Integer, nullable=False)
    Ufecha_creacion = db.Column(db.DateTime, nullable=False)
    Ufecha_modificacion = db.Column(db.DateTime)

    def __init__(self, Unombre, Uapellido, Ucorreo, Upassword, Uestado, Eid, Ufecha_creacion, Ufecha_modificacion):
        self.Unombre = Unombre
        self.Uapellido = Uapellido
        self.Ucorreo = Ucorreo
        self.Upassword = Upassword
        self.Uestado = Uestado
        self.Eid = Eid
        self.Ufecha_creacion = Ufecha_creacion
        self.Ufecha_modificacion = Ufecha_modificacion

    # OBTENER CORREO ACTIVO
    def get_id(email):
        consulta = Usuarios.query.filter_by(Ucorreo=email, Uestado=1).first()
        return consulta.__dict__.get('Uid')

    # LOGIN
    def get_by_email(Ucorreo, Upassword):
        return Usuarios.query.filter_by(Ucorreo=Ucorreo, Upassword=Upassword, Uestado=1).first()

    # MUESTRA CONSULTA DE USUARIO POR ID
    def get_Detalle_id(id):
        consulta = Usuarios.query.filter_by(Uid=id, Uestado=1).first()
        return consulta

    # VALIDAR ESTADO HABILITADO
    def get_Estado(id):
        consulta = Usuarios.query.filter_by(Uid=id, Uestado=1).first()
        return consulta

    # OBTENER ROL
    def get_roles(uid):
        consulta = Usuarios.query.join(UAR_accesos, UAR_accesos.Uid == Usuarios.Uid) \
            .join(Areas, Areas.Aid == UAR_accesos.Aid).join(Roles, Roles.Rid == UAR_accesos.Rid) \
            .add_columns(Areas.Aid, Areas.Adescripcion, Roles.Rid, Roles.Rdescripcion, Usuarios.Uid) \
            .filter(UAR_accesos.Uid == uid)
        return consulta
        # for c in consulta:
        #     return c


class Usuarios_Schema(ma.Schema):
    class Meta:
        fields = ('Uid', 'Unombre', 'Uapellido', 'Ucorreo', 'Upassword', 'Uestado', 'Eid', 'Ufecha_creacion',
                  'Ufecha_modificacion')


usuario_sc = Usuarios_Schema()
usuarios_scs = Usuarios_Schema(many=True)


# ------------------------------************------------------------------*
class UAR_accesos(db.Model):
    Uid = db.Column(db.Integer, primary_key=True)
    Aid = db.Column(db.Integer, primary_key=True)
    Rid = db.Column(db.Integer, nullable=False)

    def __init__(self, Uid, Aid, Rid):
        self.Uid = Uid
        self.Aid = Aid
        self.Rid = Rid

    def UAR_id(aid, id):
        return UAR_accesos.query.filter_by(Aid=aid, Uid=id).first()
    def UAR_id_all(uid, aid, rid):
        return UAR_accesos.query.filter_by(Uid=uid,Aid=aid, Rid=rid).first()

class UAR_accesos_Schema(ma.Schema):
    class Meta:
        fields = ('Uid',)

UAR_acceso_sc = UAR_accesos_Schema()
UAR_accesos_scs = UAR_accesos_Schema(many=True)
# ------------------------------************------------------------------*
# ------------------------------************------------------------------*
# ------------------------------************------------------------------*
# ------------------------------************------------------------------*
# --------------------------------SEGURIDAD-------------------------------*

class MT_areas(db.Model):
    MT_Aid = db.Column(db.Integer, primary_key=True)
    Eid = db.Column(db.Integer, nullable=False)
    MT_Anombre = db.Column(db.String(200), nullable=False)
    MT_Aestado = db.Column(db.Integer, nullable=False)
    MT_Afech_crea = db.Column(db.DateTime, nullable=False)
    MT_Afech_mod = db.Column(db.DateTime, nullable=True)
    MT_ambientes = db.relationship('MT_ambientes', backref='MT_areas', lazy=True)

    def __init__(self, Eid, MT_Anombre, MT_Aestado, MT_Afech_crea):
        self.Eid = Eid
        self.MT_Anombre = MT_Anombre
        self.MT_Aestado = MT_Aestado
        self.MT_Afech_crea = MT_Afech_crea
    def get_areas_a(self):
        return MT_areas.query.filter_by(MT_Aestado=1)\
            .add_columns(MT_areas.MT_Aid, MT_areas.MT_Anombre, MT_areas.MT_Aestado, MT_areas.MT_Afech_crea, MT_areas.MT_Afech_mod)\
            .order_by(MT_areas.MT_Anombre.asc())

class MT_areas_Schema(ma.Schema):
    class Meta:
        fields = ('MT_Aid', 'Eid', 'MT_Anombre', 'MT_Aestado', 'MT_Afech_crea', 'MT_Afech_mod')

MT_areas_sc = MT_areas_Schema()
MT_areas_scs = MT_areas_Schema(many=True)

# ##################################################
class MT_ambientes(db.Model):
    MT_Abcodigo = db.Column(db.Integer, primary_key=True)
    MT_Aid = db.Column(db.Integer, db.ForeignKey('mt_areas.MT_Aid'), nullable=False)
    MT_ABnombre = db.Column(db.String(200), nullable=False)
    MT_ABestado = db.Column(db.Integer, nullable=False)
    MT_ABfech_crea = db.Column(db.DateTime, nullable=False)
    MT_ABfech_mod = db.Column(db.DateTime)
    MT_asig_et_fn = db.relationship('MT_asig_et_fn', backref='MT_ambientes', lazy=True)



    def __init__(self, MT_Aid, MT_ABnombre, MT_ABestado, MT_ABfech_crea):
        self.MT_Aid = MT_Aid
        self.MT_ABnombre = MT_ABnombre
        self.MT_ABestado = MT_ABestado
        self.MT_ABfech_crea = MT_ABfech_crea

     # OBTENER AREAS ACTI
    def get_ambientes(self):
        consulta = MT_ambientes.query.join(MT_areas, MT_ambientes.MT_Aid == MT_areas.MT_Aid) \
            .add_columns(MT_ambientes.MT_Abcodigo, MT_areas.MT_Anombre, MT_ambientes.MT_ABnombre,
                         MT_ambientes.MT_ABestado, MT_ambientes.MT_ABfech_crea, MT_ambientes.MT_ABfech_mod)\
            .filter(MT_areas.MT_Aestado == 1).order_by(MT_ambientes.MT_ABnombre.asc())
        return consulta

class MT_ambientes_Schema(ma.Schema):
    class Meta:
        fields = ('MT_Abcodigo', 'MT_Aid', 'MT_ABnombre', 'MT_ABestado', 'MT_ABfech_crea', 'MT_ABfech_mod')

MT_ambientes_sc = MT_ambientes_Schema()
MT_ambientes_scs = MT_ambientes_Schema(many=True)

# ##################################################
class MT_etiquetas(db.Model):
    MT_Eid = db.Column(db.Integer, primary_key=True)
    MT_Enombre = db.Column(db.String(200), nullable=False)
    MT_Eestado = db.Column(db.Integer, nullable=False)
    MT_Efech_crea = db.Column(db.DateTime, nullable=False)
    MT_Efech_mod = db.Column(db.DateTime)
    MT_eti_fn = db.relationship('MT_eti_fn', backref='MT_etiquetas', lazy=True)
    MT_asig_et_fn = db.relationship('MT_asig_et_fn', backref='MT_etiquetas', lazy=True)
    def __init__(self, MT_Enombre, MT_Eestado, MT_Efech_crea, MT_Efech_mod):
        self.MT_Enombre = MT_Enombre
        self.MT_Eestado = MT_Eestado
        self.MT_Efech_crea = MT_Efech_crea
        self.MT_Efech_mod = MT_Efech_mod

class MT_etiquetas_Schema(ma.Schema):
    class Meta:
        fields = ('MT_Enombre', 'MT_Eestado', 'MT_Efech_crea', 'MT_Efech_mod')

MT_etiquetas_sc = MT_etiquetas_Schema()
MT_etiquetas_scs = MT_etiquetas_Schema(many=True)

# ##################################################
class MT_funciones(db.Model):
    MT_Fid = db.Column(db.Integer, primary_key=True)
    MT_Fnombre = db.Column(db.String(200), nullable=False)
    MT_Festado = db.Column(db.Integer, nullable=False)
    MT_Ffech_crea = db.Column(db.DateTime, nullable=False)
    MT_Ffech_mod = db.Column(db.DateTime)
    MT_eti_fn = db.relationship('MT_eti_fn', backref='MT_funciones', lazy=True)

    def __init__(self, MT_Fnombre, MT_Festado, MT_Ffech_crea, MT_Ffech_mod):
        self.MT_Fnombre = MT_Fnombre
        self.MT_Festado = MT_Festado
        self.MT_Ffech_crea = MT_Ffech_crea
        self.MT_Ffech_mod = MT_Ffech_mod

class MT_funciones_Schema(ma.Schema):
    class Meta:
        fields = ('MT_Fnombre', 'MT_Festado', 'MT_Ffech_crea', 'MT_Ffech_mod')

MT_funciones_sc = MT_funciones_Schema()
MT_funciones_scs = MT_funciones_Schema(many=True)

# ##################################################
class MT_eti_fn(db.Model):
    MT_EFid = db.Column(db.Integer, primary_key=True)
    MT_Eid = db.Column(db.Integer, db.ForeignKey('mt_etiquetas.MT_Eid'))
    MT_Fid = db.Column(db.Integer, db.ForeignKey('mt_funciones.MT_Fid'))
    MT_EFestado = db.Column(db.Integer, nullable=False)
    MT_EFfech_crea = db.Column(db.DateTime, nullable=False)
    MT_EFfech_mod = db.Column(db.DateTime)


    def __init__(self, MT_Eid, MT_Fid, MT_EFestado, MT_EFfech_crea, MT_EFfech_mod):
        self.MT_Eid = MT_Eid
        self.MT_Fid = MT_Fid
        self.MT_EFestado = MT_EFestado
        self.MT_EFfech_crea = MT_EFfech_crea
        self.MT_EFfech_mod = MT_EFfech_mod

class MT_eti_fn_Schema(ma.Schema):
    class Meta:
        fields = ('MT_Eid', 'MT_Fid', 'MT_EFestado', 'MT_EFfech_crea', 'MT_EFfech_mod')

MT_eti_fn_sc = MT_eti_fn_Schema()
MT_eti_fn_scs = MT_eti_fn_Schema(many=True)

# ##################################################
class MT_asig_et_fn(db.Model):
    MT_AEFid = db.Column(db.Integer, primary_key=True)
    MT_Abcodigo = db.Column(db.Integer, db.ForeignKey('mt_ambientes.MT_Abcodigo'))
    MT_Eid = db.Column(db.Integer, db.ForeignKey('mt_etiquetas.MT_Eid'))
    MT_AEFestado = db.Column(db.Integer, nullable=False)
    MT_AEFfech_crea = db.Column(db.DateTime, nullable=False)
    MT_AEFfech_mod = db.Column(db.DateTime)
    MT_asig_funciones = db.relationship('MT_asig_funciones', backref='MT_asig_et_fn', lazy=True)

    def __init__(self, MT_Abcodigo, MT_Eid, MT_AEFestado, MT_AEFfech_crea, MT_AEFfech_mod):
        self.MT_Abcodigo = MT_Abcodigo
        self.MT_Eid = MT_Eid
        self.MT_AEFestado = MT_AEFestado
        self.MT_AEFfech_crea = MT_AEFfech_crea
        self.MT_AEFfech_mod = MT_AEFfech_mod

class MT_asig_et_fn_Schema(ma.Schema):
    class Meta:
        fields = ('MT_Abcodigo', 'MT_Eid', 'MT_AEFestado', 'MT_AEFfech_crea', 'MT_AEFfech_mod')

MT_asig_et_fn_sc = MT_asig_et_fn_Schema()
MT_asig_et_fn_scs = MT_asig_et_fn_Schema(many=True)

# ##################################################
class MT_asig_funciones(db.Model):
    MT_ASFid = db.Column(db.Integer, primary_key=True)
    Uid = db.Column(db.Integer, nullable=False)
    MT_AEFid = db.Column(db.Integer, db.ForeignKey('mt_asig_et_fn.MT_AEFid'))
    MT_ASFestado = db.Column(db.Integer, nullable=False)
    MT_ASFfech_crea = db.Column(db.DateTime, nullable=False)
    MT_ASFfech_asigdesde = db.Column(db.Date)
    MT_ASFfech_asighasta = db.Column(db.Date)
    MT_ASFcontador = db.Column(db.Integer, nullable=False)
    MT_funcion_resp = db.relationship('MT_funcion_resp', backref='MT_asig_funciones', lazy=True)

    def __init__(self, Uid, MT_AEFid, MT_ASFestado, MT_ASFfech_crea, MT_ASFfech_asigdesde, MT_ASFfech_asighasta, MT_ASFcontador):
        self.Uid = Uid
        self.MT_AEFid = MT_AEFid
        self.MT_ASFestado = MT_ASFestado
        self.MT_ASFfech_crea = MT_ASFfech_crea
        self.MT_ASFfech_asigdesde = MT_ASFfech_asigdesde
        self.MT_ASFfech_asighasta = MT_ASFfech_asighasta
        self.MT_ASFcontador = MT_ASFcontador

class MT_asig_funciones_Schema(ma.Schema):
    class Meta:
        fields = ('Uid', 'MT_AEFid', 'MT_ASFestado', 'MT_ASFfech_crea', 'MT_ASFfech_asigdesde','MT_ASFfech_asighasta', 'MT_ASFcontador')

MT_asig_funciones_sc = MT_asig_funciones_Schema()
MT_asig_funciones_scs = MT_asig_funciones_Schema(many=True)

# ##################################################
class MT_funcion_resp(db.Model):
    MT_FRid = db.Column(db.Integer, primary_key=True)
    MT_ASFid = db.Column(db.Integer, db.ForeignKey('mt_asig_funciones.MT_ASFid'))
    MT_FRRespuesta= db.Column(db.String(10), nullable=False)
    MT_FRcomentario = db.Column(db.String(150), nullable=False)
    MT_ASFfech_crea = db.Column(db.DateTime, nullable=False)

    def __init__(self, MT_ASFid, MT_FRRespuesta, MT_FRcomentario, MT_ASFfech_crea):
        self.MT_ASFid = MT_ASFid
        self.MT_FRRespuesta = MT_FRRespuesta
        self.MT_FRcomentario = MT_FRcomentario
        self.MT_ASFfech_crea = MT_ASFfech_crea

class MT_funcion_resp_Schema(ma.Schema):
    class Meta:
        fields = ('MT_ASFid', 'MT_FRRespuesta', 'MT_FRcomentario', 'MT_ASFfech_crea')

MT_funcion_resp_sc = MT_funcion_resp_Schema()
MT_funcion_resp_scs = MT_funcion_resp_Schema(many=True)

# try:
#     db.create_all()
# except Exception as e:
#     print(e)

# @app.route('/', methods=['GET'])
# def get():
#     config = Configuraciones.query.filter_by(Cid=6).first()
#     config.Ccategoria = 'ok'
#     db.session.commit()
#     return config.Ccategoria
    # ok = UAR_accesos.query.all()
    # result = UAR_accesos_scs.dump(ok)
    # return jsonify(result[0])
#     con = Roles.query.all()
#     return 'ds'
# all = Roles.query.all()
# result = roles_scs.dump(all)
# print(all)
# print(result)
# return render_template('Login/List.html', area=result)

# class Task(db.Model):
#     Aid = db.Column(db.Integer, primary_key=True)
#     prueba = db.Column(db.String(70))
#
#     def __init__(self, prueba):
#         self.prueba = prueba
#
# db.create_all()
#
# class TaskSchema(ma.Schema):
#     class Meta:
#         fields = ( 'prueba',)
# task_sc = TaskSchema()
# task_scs = TaskSchema(many=True)
#
# @app.route('/task', methods = ['POST'])
# def create():
#     prueba = request.json['prueba']
#
#     new = Task(prueba)
#     db.session.add(new)
#     db.session.commit()
#     return task_sc.jsonify(new)
# @app.route('/', methods = ['GET'])
# def get():
#     all = Task.query.all()
#     result = task_scs.dump(all)
#     return jsonify(result)
# if __name__ ==   "__main__":
#     app.run(port=3000, debug=True)
