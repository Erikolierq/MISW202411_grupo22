from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app
import logging
import jwt
from app.models import User
from app import db, app
import ssl
from app.models import User, TrainingSession, MedicalRecord


ROLES = {
    'deportista': ['deportista'],
    'instructor': ['instructor'],
    'medico_deportologo': ['medico_deportologo'],
    'administrador': ['administrador']
}

def authenticate_user(usuario, password):
    user = User.query.filter_by(usuario=usuario).first()
    if not user:
        current_app.logger.warning(f"Authentication failed for non-existent user: {usuario}")
        return None
    if not user.check_password(password):
        current_app.logger.warning(f"Authentication failed for user: {usuario}")
        return None
    current_app.logger.info(f"User {usuario} authenticated successfully")
    
    return user

def convert_token_string_to_bytes(token_str):
    try:
        token_bytes = token_str.encode('utf-8')  # Convertir el token de string a bytes
        return token_bytes
    except Exception as e:
        print(f"Error converting token string to bytes: {e}")
        return None

def generate_jwt_token(user):
    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow(),
            'sub': user.id,
            'rol': user.rol
        }
        secret_key = current_app.config.get('SECRET_KEY')  # Obtener la llave secreta de la configuración
        token_str = jwt.encode(
            payload,
            secret_key,
            algorithm='HS256'
        )
        print(f"Token bytes type: {type(token_str)}")  # Debug: Imprimir el tipo de token_str
        token_bytes = convert_token_string_to_bytes(token_str)  # Convertir el token a bytes
        if not isinstance(token_bytes, bytes):
            raise ValueError("Token conversion to bytes failed.")
        
        # Convertir el token de bytes a string antes de devolverlo
        token_str_final = token_bytes.decode('utf-8')
        
        current_app.logger.info(f"JWT token generated for user ID: {user.id}")
        return token_str_final  # Devolver el token como string
    except Exception as e:
        current_app.logger.error(f"Error generating JWT token for user ID: {user.id} - {e}")
        return None
    
def verify_certificate(cert_str):
    """
    Verifica la validez de un certificado de seguridad recibido como string.
    Retorna True si es válido, False en caso contrario.
    """
    try:
        cert_bytes = cert_str.encode()
        cert = ssl.PEM_cert_to_DER_cert(cert_bytes)
        current_app.logger.info("Security certificate verified successfully")
        return True
    except Exception as e:
        current_app.logger.error(f"Error verifying the certificate: {e}")
        return False

def token_required(expected_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = None
            cert_str = request.headers.get('X-Client-Cert')  

            if not cert_str or not verify_certificate(cert_str):
                return jsonify({'message': 'Missing or invalid security certificate'}), 401

            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].split()[1]

            if not token or not verify_certificate(token):
                return {'message': 'Token is missing or invalid'}, 403

            try:
                data = jwt.decode(token, app.config['SECRET_KEY'])
                current_user = User.query.filter_by(public_id=data['public_id']).first()
            except:
                return jsonify({'message': 'Token is invalid'}), 403
            if not current_user:
                return jsonify({'message': 'User not found'}), 403
            if ROLES[current_user.rol] < ROLES[expected_role]:
                return jsonify({'message': 'Unauthorized access'}), 403
            return f(current_user, *args, **kwargs)

        return decorated_function
    return decorator


@app.route('/protected-route-deportista', methods=['GET', 'POST'])
@token_required('deportista')
def protected_route_deportista(current_user):
    current_app.logger.info(f"Acceso concedido a la ruta protegida de deportista para el usuario: {current_user.usuario}")

    if request.method == 'GET':
        # Obtener todas las sesiones de entrenamiento del deportista
        training_sessions = TrainingSession.query.filter_by(deportista_id=current_user.id).all()
        return jsonify([session.to_dict() for session in training_sessions])

    if request.method == 'POST':
        # Registrar una nueva sesión de entrenamiento para el deportista
        data = request.get_json()
        new_session = TrainingSession(
            name=data.get('name'),
            date=data.get('date'),
            duration=data.get('duration'),
            deportista_id=current_user.id
        )
        db.session.add(new_session)
        db.session.commit()
        return jsonify({'message': 'Training session registered successfully'}), 201

    return jsonify({'message': 'Invalid request method'}), 405

@app.route('/protected-route-instructor', methods=['GET', 'POST'])
@token_required('instructor')
def protected_route_instructor(current_user):
    current_app.logger.info(f"Acceso concedido a la ruta protegida de instructor para el usuario: {current_user.usuario}")

    if request.method == 'GET':
        # Obtener todas las sesiones de entrenamiento gestionadas por este instructor
        training_sessions = TrainingSession.query.filter_by(instructor_id=current_user.id).all()
        return jsonify([session.to_dict() for session in training_sessions])

    if request.method == 'POST':
        # Crear una nueva sesión de entrenamiento
        data = request.get_json()
        new_session = TrainingSession(
            name=data.get('name'),
            date=data.get('date'),
            duration=data.get('duration'),
            instructor_id=current_user.id
        )
        db.session.add(new_session)
        db.session.commit()
        return jsonify({'message': 'Training session created successfully'}), 201

    return jsonify({'message': 'Invalid request method'}), 405

@app.route('/protected-route-medico', methods=['GET', 'POST'])
@token_required('medico_deportologo')
def protected_route_medico_deportologo(current_user):
    current_app.logger.info(f"Acceso concedido a la ruta protegida de médico deportólogo para el usuario: {current_user.usuario}")

    if request.method == 'GET':
        # Obtener todos los registros médicos gestionados por este médico deportólogo
        medical_records = MedicalRecord.query.filter_by(medico_id=current_user.id).all()
        return jsonify([record.to_dict() for record in medical_records])

    if request.method == 'POST':
        # Crear un nuevo registro médico
        data = request.get_json()
        new_record = MedicalRecord(
            deportista_id=data.get('deportista_id'),
            medico_id=current_user.id,
            diagnosis=data.get('diagnosis'),
            treatment=data.get('treatment'),
            notes=data.get('notes')
        )
        db.session.add(new_record)
        db.session.commit()
        return jsonify({'message': 'Medical record created successfully'}), 201

    return jsonify({'message': 'Invalid request method'}), 405

@app.route('/protected-route-administrador', methods=['GET', 'POST'])
@token_required('administrador')
def protected_route_administrador(current_user):
    current_app.logger.info(f"Acceso concedido a la ruta protegida de administrador para el usuario: {current_user.usuario}")

    if request.method == 'GET':
        # Obtener todos los usuarios registrados en la plataforma
        users = User.query.all()
        return jsonify([{
            'id': user.id,
            'usuario': user.usuario,
            'correo': user.correo,
            'rol': user.rol,
            'nombre': user.nombre,
            'numero_contacto': user.numero_contacto
        } for user in users])

    if request.method == 'POST':
        # Crear un nuevo usuario
        data = request.get_json()
        new_user = User(
            usuario=data.get('usuario'),
            correo=data.get('correo'),
            rol=data.get('rol'),
            nombre=data.get('nombre', None),
            numero_contacto=data.get('numero_contacto', None)
        )
        new_user.set_password(data.get('contrasena'))
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201

    return jsonify({'message': 'Invalid request method'}), 405