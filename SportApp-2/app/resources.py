from flask import request, jsonify
from flask_restful import Resource
from app.models import User, TrainingSession, MedicalRecord, Instructor, Notification, Exercise, TrainingPlan, TrainingPlanExercise
from app.tasks import send_message, send_verification_email, send_password_reset_email
from app import db
from app.authentication import authenticate_user, generate_jwt_token, authenticate_user, token_required
from flask_jwt_extended import jwt_required, JWTManager



# User resource remains the same
class UserResource(Resource):
    @token_required
    def get(self, current_user, user_id):
        """
        Retrieve user information.
        """
        if current_user.id != user_id and current_user.rol != 'administrador':
            return {'message': 'Unauthorized access'}, 403

        user = User.query.get_or_404(user_id)
        return user.to_dict()

class TrainingSessionResource(Resource):
    @token_required
    def get(self, current_user, session_id):
        """
        Retrieve training session information.
        """
        session = TrainingSession.query.get_or_404(session_id)

        # Verificar si el usuario actual tiene permiso para acceder a la sesión de entrenamiento
        if current_user.id != session.user_id and current_user.rol != 'administrador':
            return {'message': 'Unauthorized access'}, 403

        return session.to_dict()

# MedicalRecordResource: Maneja las operaciones relacionadas con los registros médicos
class MedicalRecordResource(Resource):
    def get(self, record_id):
        record = MedicalRecord.query.get_or_404(record_id)
        return {
            'id': record.id,
            'deportista_id': record.deportista_id,
            'medico_id': record.medico_id,
            'diagnosis': record.diagnosis,
            'treatment': record.treatment,
            'notes': record.notes
        }

# InstructorResource: Maneja las operaciones relacionadas con los instructores
class InstructorResource(Resource):
    def get(self, instructor_id):
        instructor = Instructor.query.get_or_404(instructor_id)
        return {
            'id': instructor.id,
            'user_id': instructor.user_id,
            'credentials': instructor.credentials,
            'specialties': instructor.specialties
        }


# ExerciseResource: Maneja las operaciones relacionadas con los ejercicios
class ExerciseResource(Resource):
    def get(self, exercise_id):
        exercise = Exercise.query.get_or_404(exercise_id)
        return exercise.to_dict()

# TrainingPlanResource: Maneja las operaciones relacionadas con los planes de entrenamiento
class TrainingPlanResource(Resource):
    def get(self, plan_id):
        plan = TrainingPlan.query.get_or_404(plan_id)
        return {
            'id': plan.id,
            'name': plan.name,
            'description': plan.description,
            'user_id': plan.user_id,
            'exercises': [exercise.to_dict() for exercise in plan.exercises]
        }
    
# NotificationResource: Maneja las operaciones relacionadas con las notificaciones
class NotificationResource(Resource):
    def get(self, notification_id):
        notification = Notification.query.get_or_404(notification_id)
        return {
            'id': notification.id,
            'user_id': notification.user_id,
            'message': notification.message,
            'timestamp': notification.timestamp
        }


# New resource for testing message sending with Celery
class SendMessageResource(Resource):
    def post(self):
        subject = request.json.get('subject', 'Test Subject')
        recipient = request.json.get('recipient', 'your-email@example.com')
        body = request.json.get('body', 'Test message body')
        send_message.delay(subject, recipient, body)
        return {'message': 'Message sent successfully'}, 200


# Resource for user registration
class UserRegistrationResource(Resource):
    def post(self):
        data = request.get_json()
        user = User(
            usuario=data['usuario'],
            correo=data['correo'],
            rol=data['rol'],
            nombre=data.get('nombre', None),
            numero_contacto=data.get('numeroContacto', None)
        )
        user.set_password(data['contrasena'])  # Encripta la contraseña
        db.session.add(user)
        db.session.commit()
        send_verification_email(user.correo, 'verification_link')
        return {'message': 'User registered successfully'}, 201

# Resource for email verification
class EmailVerificationResource(Resource):
    def post(self):
        # Add logic to verify email
        return {'message': 'Email verified successfully'}, 200

# Resource for password reset request
class PasswordResetRequestResource(Resource):
    def post(self):
        email = request.json.get('email')
        # Add logic to send password reset email
        send_password_reset_email.delay(email, 'reset_link')
        return {'message': 'Password reset email sent'}, 200

# Resource for password reset
class PasswordResetResource(Resource):
    def post(self):
        # Add logic to reset password
        return {'message': 'Password reset successfully'}, 200


class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        user = authenticate_user(data.get('usuario'), data.get('contrasena'))
        if user:
            token = generate_jwt_token(user)
            return {'token': token}, 200
        else:
            return {'message': 'Invalid credentials'}, 401

class CrearEjerciciosResource(Resource):
    @jwt_required()
    def post(self):
        ejercicios_nuevos = request.json.get('ejercicios', [])  
        try:
            ejercicios_creados = []
            for ejercicio in ejercicios_nuevos:
                nuevo_ejercicio = Exercise(
                    name=ejercicio['name'],
                    description=ejercicio['description'],
                    type=ejercicio['type'],
                    duration=ejercicio['duration'],
                    repetitions=ejercicio['repetitions']
                )
                db.session.add(nuevo_ejercicio)
                ejercicios_creados.append(nuevo_ejercicio.to_dict())

            db.session.commit()
            return {'message': 'Ejercicios creados correctamente', 'ejercicios': ejercicios_creados}, 201
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500
        
class ListarEjerciciosResource(Resource):
    @jwt_required()
    def get(self):
        try:
            ejercicios = Exercise.query.all()
            ejercicios_list = [ejercicio.to_dict() for ejercicio in ejercicios]
            return {'ejercicios': ejercicios_list}, 200  # Return a dictionary
        except Exception as e:
            # Handle the exception and return a dictionary with error details
            return {'error encontrao': str(e)}, 500


        
class ActualizarEjercicioResource(Resource):
    @jwt_required()
    def put(self, ejercicio_id):
        try:
            ejercicio = Exercise.query.get(ejercicio_id)
            if not ejercicio:
                return {'message': 'Ejercicio no encontrado'}, 404
            
            # Actualizar los campos del ejercicio
            data = request.json
            ejercicio.name = data.get('name', ejercicio.name)
            ejercicio.description = data.get('description', ejercicio.description)
            ejercicio.type = data.get('type', ejercicio.type)
            ejercicio.duration = data.get('duration', ejercicio.duration)
            ejercicio.repetitions = data.get('repetitions', ejercicio.repetitions)
            
            db.session.commit()
            return {'message': 'Ejercicio actualizado correctamente'}, 200
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

class EliminarEjercicioResource(Resource):
    @jwt_required()
    def delete(self, ejercicio_id):
        try:
            ejercicio = Exercise.query.get(ejercicio_id)
            if not ejercicio:
                return {'message': 'Ejercicio no encontrado'}, 404
            
            db.session.delete(ejercicio)
            db.session.commit()
            return {'message': 'Ejercicio eliminado correctamente'}, 200
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500
        
# Nueva función para configurar 'api' y evitar importaciones cíclicas
def configure_api(api):
    api.add_resource(UserResource, '/users/<int:user_id>')
    api.add_resource(LoginResource, "/login")
    api.add_resource(TrainingSessionResource, '/training_sessions/<int:session_id>')
    api.add_resource(SendMessageResource, '/send_message')
    api.add_resource(UserRegistrationResource, '/registro')
    api.add_resource(EmailVerificationResource, '/verify_email')
    api.add_resource(PasswordResetRequestResource, '/password_reset_request')
    api.add_resource(PasswordResetResource, '/password_reset')
    api.add_resource(MedicalRecordResource, '/medical_records/<int:record_id>')
    api.add_resource(InstructorResource, '/instructors/<int:instructor_id>')
    api.add_resource(ExerciseResource, '/exercises/<int:exercise_id>')
    api.add_resource(TrainingPlanResource, '/training_plans/<int:plan_id>')
    api.add_resource(NotificationResource, '/notifications/<int:notification_id>')
    api.add_resource(CrearEjerciciosResource, '/crear_ejercicios')
    api.add_resource(ListarEjerciciosResource, '/ejercicios')
    api.add_resource(ActualizarEjercicioResource, '/actualizar_ejercicio/<int:ejercicio_id>')
    api.add_resource(EliminarEjercicioResource, '/eliminar_ejercicio/<int:ejercicio_id>')