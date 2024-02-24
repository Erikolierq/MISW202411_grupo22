from flaskr import create_app
from .modelos import db, Ejercicio, Situacion, Alerta, Riesgo
from .modelos import SituacionSchema
from flask_restful import Api
from .vistas import VistaAlertas, VistaAlerta, VistaEjercicio, VistaEjercicios, VistaEjerciciosSituaciones, VistaSituacion, VistaSituacionAlerta


app = create_app('default')
app_context = app.app_context()
app_context.push()


db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(VistaEjercicios, '/ejercicios')
api.add_resource(VistaEjercicio, '/ejercicio/<int:id_ejercicio>')
api.add_resource(VistaAlertas, '/alertas')
api.add_resource(VistaAlerta, '/alerta/<int:id_alerta>')
api.add_resource(VistaSituacionAlerta, '/alerta/<int:id_alerta>/situaciones')
api.add_resource(VistaSituacion, '/situacion/<int:id_situacion>')
api.add_resource(VistaEjerciciosSituaciones, '/situacion/<int:id_situacion>/ejercicios')
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

