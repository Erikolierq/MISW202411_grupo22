from microservicio_riesgos import create_app
from flask_restful import Api, Resource
from flask import Flask, request
import requests
import json


app = create_app('default')
app_context = app.app_context()
app_context.push()

class VistaMonitoreoDeportivo(Resource):

    def post(self, id_ejercicio):
        content = requests.get('http://127.0.0.1:5000/ejercicio/{}'.format(id_ejercicio))

        if content.status_code == 404:
            return content.json(),404
        
        else:
            ejercicio = content.json()
            ejercicio['nivel_riesgo']= request.json['nivel_riesgo']
            args = (ejercicio,)
            return json.dumps(ejercicio)

api = Api(app)
api.add_resource(VistaMonitoreoDeportivo, '/ejercicio,<int:id_ejercicio>/nivel')