from .modelos import db, Ejercicio, Situacion, Alerta, Riesgo
from .modelos import SituacionSchema
from flask_restful import Api
from .vistas import VistaAlertas, VistaAlerta, VistaEjercicio, VistaEjercicios, VistaEjerciciosSituaciones, VistaSituacion, VistaSituacionAlerta
from flaskr import create_app
from flaskr.modelos import db
from flaskr.vistas import (
    VistaAlertas, VistaAlerta, VistaEjercicio, VistaEjercicios,
    VistaEjerciciosSituaciones, VistaSituacion, VistaSituacionAlerta
)
from flask_restful import Api

# Crea una instancia de la aplicación Flask utilizando la configuración predeterminada
app = create_app('default')

# Crea el contexto de la aplicación y lo activa
app_context = app.app_context()
app_context.push()

# Inicializa la API de Flask-RESTful y registra los recursos/endpoints
api = Api(app)
api.add_resource(VistaEjercicios, '/ejercicios')
api.add_resource(VistaEjercicio, '/ejercicio/<int:id_ejercicio>')
api.add_resource(VistaAlertas, '/alertas')
api.add_resource(VistaAlerta, '/alerta/<int:id_alerta>')
api.add_resource(VistaSituacionAlerta, '/alerta/<int:id_alerta>/situaciones')
api.add_resource(VistaSituacion, '/situacion/<int:id_situacion>')
api.add_resource(VistaEjerciciosSituaciones, '/situacion/<int:id_situacion>/ejercicios')

# Asegura que el contexto de la aplicación esté activo y configura la base de datos
with app.app_context():
    db.init_app(app)  # Esta línea es redundante ya que app_context ya está activo
    db.create_all()   # Crea todas las tablas definidas en tus modelos (si no existen)

# Ejecuta la aplicación si este script es ejecutado directamente
if __name__ == '__main__':
    app.run(debug=True)

#PRUEBA
#with app.app_context():
 #   e = Ejercicio(nombre='Sentadilla', duracion=2)
  #  db.session.add(e)
   # s = Situacion(nombre_riesgo='Corazon',riesgo=Riesgo.Existe)
    #e.riesgos.append(s)
    #db.session.add(s)
    #db.session.commit()
    #print(Ejercicio.query.all())
    #print(Ejercicio.query.all()[0].riesgos)

