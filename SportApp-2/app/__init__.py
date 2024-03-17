from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_migrate import Migrate
from flask_mail import Mail
from flask_cors import CORS
from app.logging_config import configure_logging
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required

# Crear la instancia de la aplicación Flask
app = Flask(__name__)

# Cargar la configuración de la aplicación desde el objeto de configuración
app.config.from_object('config.Config')
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
# Configurar el logging para la aplicación
configure_logging(app)



jwt = JWTManager(app)

@jwt.unauthorized_loader
def unauthorized_callback(jwt_header, jwt_payload):
    return jsonify({'message': 'You are not authorized to access this resource'}), 403

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'status': 401,
        'sub_status': 1,
        'msg': 'You must provide a valid JWT token'
    }), 401

# Inicializar las extensiones de Flask
db = SQLAlchemy(app)  # Base de datos
api = Api(app)  # API RESTful
migrate = Migrate(app, db)  # Migraciones de la base de datos
mail = Mail(app)  # Correo electrónico
CORS(app)  # Control de Acceso de Origen Cruzado



# Importar los modelos, recursos y tareas de la aplicación
from app import models, resources, tasks



# Configurar la API RESTful con los recursos definidos
resources.configure_api(api)

# Importar e inicializar las rutas de la aplicación Flask
from app.routes import init_routes
init_routes(app)

# Crear todas las tablas en la base de datos (si no existen)
with app.app_context():
    db.create_all()

# Ejecutar la aplicación en modo de depuración (debug)
if __name__ == '__main__':
    app.run(debug=True)
