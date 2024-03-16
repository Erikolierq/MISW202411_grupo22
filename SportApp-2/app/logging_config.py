import logging
from logging.handlers import RotatingFileHandler

def configure_logging(app):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')

    file_handler = RotatingFileHandler('instance/sportapp.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
    file_handler.setLevel(logging.INFO)

    app.logger.addHandler(file_handler)