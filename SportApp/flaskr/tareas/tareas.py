from celery import Celery
from flaskr import create_app
from flaskr.modelos import db, Situacion, SituacionSchema, Alerta, AlertaSchema, Ejercicio, EjercicioSchema

from sqlalchemy.exc import IntegrityError

celery_app = Celery(__name__, broker='redis://localhost:6379/0')

# Define tus tareas de Celery aquí
@celery_app.task
def crear_ejercicio(nombre, duracion):
    
    try:
        nuevo_ejercicio = Ejercicio(nombre=nombre, duracion=duracion)
        print(nuevo_ejercicio)
        db.session.add(nuevo_ejercicio)
        db.session.commit()
        
        return True
    
    except IntegrityError:
        db.session.rollback()
        return False

@celery_app.task
def crear_alerta(nombre_alerta, generar):
    try:
        nueva_alerta = Alerta(nombre_alerta=nombre_alerta, generar=generar)
        db.session.add(nueva_alerta)
        db.session.commit()
        return True
    except IntegrityError:
        db.session.rollback()
        return False

@celery_app.task
def actualizar_situacion(id_situacion, nombre_riesgo, riesgo):
    try:
        situacion = Situacion.query.get_or_404(id_situacion)
        situacion.nombre_riesgo = nombre_riesgo
        situacion.riesgo = riesgo
        db.session.commit()
        return True
    except IntegrityError:
        db.session.rollback()
        return False