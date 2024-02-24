from flask_restful import Resource
from ..modelos import db, Situacion, SituacionSchema, Alerta, AlertaSchema, Ejercicio, EjercicioSchema
from flask import request
from sqlalchemy.exc import IntegrityError

ejercicio_schema = EjercicioSchema()
situacion_schema = SituacionSchema()
alerta_schema = AlertaSchema()

class VistaEjercicios(Resource):
    def post(self):
        nuevo_ejercicio = Ejercicio(nombre=request.json["nombre"],duracion = request.json["duracion"])
        db.session.add(nuevo_ejercicio)
        db.session.commit()
        return ejercicio_schema.dump(nuevo_ejercicio)
    
    def get(self):
        return [ejercicio_schema.dump(ejercicio) for ejercicio in Ejercicio.query.all()]

class VistaEjercicio(Resource):
    def get(self, id_ejercicio):
        return ejercicio_schema.dump(Ejercicio.query.get_or_404(id_ejercicio))

    def put(self, id_ejercicio):
        ejercicio = Ejercicio.query.get_or_404(id_ejercicio)
        ejercicio.nombre = request.json.get("nombre",ejercicio.nombre)
        ejercicio.duracion = request.json.get("duracion",ejercicio.duracion)
        db.session.commit()
        return ejercicio_schema.dump(ejercicio)

    def delete(self, id_ejercicio):
        ejercicio = Ejercicio.query.get_or_404(id_ejercicio)
        db.session.delete(ejercicio)
        db.session.commit()
        return '',204


class VistaSituacion(Resource):
    def get(self, id_situacion):
        return situacion_schema.dump(Situacion.query.get_or_404(id_situacion))
    
    def put(self, id_situacion):
        situacion = Situacion.query.get_or_404(id_situacion)
        situacion.nombre_riesgo = request.json.get("nombre riesgo", situacion.nombre_riesgo)
        situacion.riesgo = request.json.get("riesgo", situacion.riesgo)
        db.session.commit()
        return situacion_schema.dump(situacion)
    
    def delete(self, id_situacion):
        situacion = Situacion.query.get_or_404(id_situacion)
        db.session.delete(situacion)
        db.session.commit()
        return '',204



class VistaAlertas(Resource):

    def get(self):
        return [alerta_schema.dump(alerta) for alerta in Alerta.query.all()]
    
    def post(self):
        nueva_alerta = Alerta(nombre_alerta = request.json['nombre riesgo'],\
                                    generar= request.json['generar'])
        db.session.add(nueva_alerta)
        db.session.commit()
        return alerta_schema.dump(nueva_alerta)
    
class VistaAlerta(Resource):

    def get(self, id_alerta):
        return alerta_schema.dump(Alerta.query.get_or_404(id_alerta))
    
    def put(self, id_alerta):
        alerta=Alerta.query.get_or_404(id_alerta)
        alerta.nombre_alerta = request.json.get('nombre alerta', alerta.nombre_alerta)
        alerta.generar = request.json.get('generar', alerta.generar)
        db.session.commit()
        return alerta_schema.dump(alerta)
    
    def delete(self, id_alerta):
        alerta=Alerta.query.get_or_404(id_alerta)
        db.session.delete(alerta)
        db.session.commit()
        return 'Operacion exitosa', 204
    
class VistaSituacionAlerta(Resource):
     def post(self, id_alerta):
        nueva_situacion = Situacion(nombre_riesgo=request.json["nombre riesgo"], riesgo=request.json["riesgo"])
        alerta = Alerta.query.get_or_404(id_alerta)
        alerta.situacion.append(nueva_situacion)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'La alerta ya tiene una situacion con dicho nombre',409

        return situacion_schema.dump(nueva_situacion)

     def get(self, id_alerta):
        alerta = Alerta.query.get_or_404(id_alerta)
        return [alerta_schema.dump(al) for al in alerta.situaciones]

class VistaEjerciciosSituaciones(Resource):

    def post(self, id_situacion):
        situacion = Situacion.query.get_or_404(id_situacion)
        
        if "id_ejercicio" in request.json.keys():
            
            nuevo_ejercicio = Ejercicio.query.get(request.json["id_ejercicio"])
            if nuevo_ejercicio is not None:
                situacion.canciones.append(nuevo_ejercicio)
                db.session.commit()
            else:
                return 'Ejercicio erróneo',404
        else: 
            nuevo_ejercicio = Ejercicio(nombre=request.json["nombre"], duracion=request.json["duracion"])
            situacion.ejercicios.append(nuevo_ejercicio)
        db.session.commit()
        return ejercicio_schema.dump(nuevo_ejercicio)
       
    def get(self, id_situacion):
        situacion = Situacion.query.get_or_404(id_situacion)
        return [ejercicio_schema.dump(ej) for ej in situacion.ejercicios]