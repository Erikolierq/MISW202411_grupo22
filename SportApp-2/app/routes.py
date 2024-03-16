from flask import Flask, jsonify, request
from app.authentication import token_required, protected_route_deportista, protected_route_instructor, protected_route_medico_deportologo, protected_route_administrador

def init_routes(app):
    @app.route('/')
    def home():
        return 'Página de inicio'

    @app.route('/login', methods=['POST'])
    def login():
        # Lógica para el inicio de sesión
        return 'Inicio de sesión'

    @app.route('/register', methods=['POST'])
    def register():
        # Lógica para el registro
        return 'Registro'

    @app.route('/dashboard')
    def dashboard():
        return 'Panel de control'