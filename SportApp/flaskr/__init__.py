from flask import Flask
from celery import Celery

def make_celery(app):
    # Inicializa Celery y lo configura con la configuración de la aplicación Flask
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)

    # Crea una subclase de tarea para manejar el contexto de la aplicación
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    
    celery.Task = ContextTask
    return celery

def create_app(config_name):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SportApp.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configuración del broker de Celery (usa Redis, RabbitMQ, o lo que prefieras)
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    app.config['result_backend'] = 'redis://localhost:6379/0'

    # Inicializa Celery
    celery = make_celery(app)

  
    
    return app