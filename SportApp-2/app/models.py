from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(64), unique=True, index=True)
    correo = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    rol = db.Column(db.String(64))
    nombre = db.Column(db.String(64), nullable=True)
    numero_contacto = db.Column(db.String(64), nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_role(self, role):
        return self.rol == role

class TrainingSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    data = db.Column(db.JSON)
    user = db.relationship('User', backref='training_sessions')

class MedicalRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deportista_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    diagnosis = db.Column(db.String(255), nullable=True)
    treatment = db.Column(db.String(255), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    deportista = db.relationship('User', foreign_keys=[deportista_id], backref='medical_records')
    medico = db.relationship('User', foreign_keys=[medico_id])

class Instructor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    credentials = db.Column(db.String(255), nullable=True)
    specialties = db.Column(db.String(255), nullable=True)
    user = db.relationship('User', backref='instructor_profile')

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    type = db.Column(db.String(255), nullable=True)
    duration = db.Column(db.Integer, nullable=True)
    repetitions = db.Column(db.Integer, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'type': self.type,
            'duration': self.duration,
            'repetitions': self.repetitions
        }
    
class TrainingPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exercises = db.relationship('Exercise', secondary='training_plan_exercise', backref='training_plans')

    user = db.relationship('User', backref='training_plans')

class TrainingPlanExercise(db.Model):
    __tablename__ = 'training_plan_exercise'
    training_plan_id = db.Column(db.Integer, db.ForeignKey('training_plan.id'), primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), primary_key=True)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    user = db.relationship('User', backref='notifications')
    

