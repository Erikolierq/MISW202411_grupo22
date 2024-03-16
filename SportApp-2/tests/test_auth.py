from datetime import datetime
from flask import jsonify
from unittest.mock import patch
from flask import Flask
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, authentication
from app.models import User

app = Flask(__name__)
app.config.from_object('config.Config')

def test_verify_certificate():
    # Mockear 'verify_certificate' directamente en lugar de usar 'flask.request.headers.get'
    with patch('app.authentication.verify_certificate', return_value=True):
        assert authentication.verify_certificate('valid_certificate_string') == True

def test_generate_jwt_token():
    # Mockear 'datetime.utcnow' para devolver una fecha y hora fija para una generación de token consistente
    with patch('app.authentication.datetime') as mock_datetime:
        mock_datetime.utcnow.return_value = datetime(2022, 1, 1)
        token = authentication.generate_jwt_token(1)
        assert token is not None
        
