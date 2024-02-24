from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
import enum

db = SQLAlchemy()

situaciones_ejercicio = db.Table('situacion_ejercicio',
    db.Column('situacion_id', db.Integer, db.ForeignKey('situacion.id'), primary_key = True),
    db.Column('ejercicio_id', db.Integer, db.ForeignKey('ejercicio.id'), primary_key = True))

class Ejercicio(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(128))
    duracion = db.Column(db.Integer)
    situaciones = db.relationship('Situacion', secondary = 'situacion_ejercicio', back_populates="ejercicios")

    
class Riesgo(enum.Enum):
    Existe = 1
    No = 2

class Situacion(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre_riesgo = db.Column(db.String(128))
    riesgo = db.Column(db.Enum(Riesgo))
    alerta = db.Column(db.Integer, db.ForeignKey('alerta.id'))
    ejercicios = db.relationship('Ejercicio', secondary = 'situacion_ejercicio', back_populates = "situaciones")



class Alerta(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre_alerta = db.Column(db.String(128))
    generar = db.Column(db.String(2))
    situaciones = db.relationship('Situacion', cascade = 'all, delete, delete-orphan')
    #situacion = db.Column(db.Integer, db.ForeignKey('situacion.id'))
    #__table_args__= (db.UniqueConstraint('situacion', 'nombre', name='nombre_unico_situacion'),)


class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {'llave':value.name, 'valor':value.value}

class EjercicioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Ejercicio
        include_relationships = True
        load_instance = True

class SituacionSchema(SQLAlchemyAutoSchema):
    riesgo = EnumADiccionario(attribute=('riesgo'))
    class meta:
        model = Situacion
        include_relationships = True
        load_instance = True


class AlertaSchema(SQLAlchemyAutoSchema):
    class meta:
        model = Alerta
        include_relationships = True
        load_instance = True