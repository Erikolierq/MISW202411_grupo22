from celery import Celery
from flask_mail import Message
from app import app, mail

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task
def send_message(subject, recipient, body):
    msg = Message(subject, recipients=[recipient], body=body)
    mail.send(msg)

@celery.task
def send_security_alert(user_email):
    subject = "Alerta de Seguridad de SportApp"
    body = "Se ha detectado una actividad sospechosa en tu cuenta. Por favor, revisa tu actividad reciente."
    send_message.delay(subject, user_email, body)

@celery.task
def send_training_confirmation(user_email, training_details):
    subject = "Confirmación de Sesión de Entrenamiento"
    body = f"Tu sesión de entrenamiento ha sido registrada con éxito: {training_details}"
    send_message.delay(subject, user_email, body)

@celery.task
def send_verification_email(user_email, verification_link):
    subject = "Verificación de Cuenta de SportApp"
    body = f"Por favor, haz clic en el siguiente enlace para verificar tu cuenta: {verification_link}"
    send_message.delay(subject, user_email, body)

@celery.task
def send_password_reset_email(user_email, reset_link):
    subject = "Restablecimiento de Contraseña de SportApp"
    body = f"Para restablecer tu contraseña, por favor sigue este enlace: {reset_link}"
    send_message.delay(subject, user_email, body)