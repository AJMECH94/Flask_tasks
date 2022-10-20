# Imports
from marshmallow import fields, Schema, validates, ValidationError
import datetime
from . import db
from marshmallow.validate import Length, Regexp
from sqlalchemy import or_, Sequence
from .MedicineModel import MedicineSchema
from .DiagnosticsModel import DiagnosticsSchema


class PatientModel(db.Model):
    '''
    ORM to manage Patients
    '''
    
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    ssn = db.Column(db.Integer, nullable=False, unique=True)
    name = db.Column(db.String(128), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    admited_on = db.Column(db.DateTime)
    type_of_bed = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(1000), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    discharged = db.Column(db.Boolean, default=False)
    medicines = db.relationship('MedicineModel', backref='patients', cascade="all, delete", lazy=True)
    diagnostics = db.relationship('DiagnosticsModel', backref='patients', cascade="all, delete", lazy=True)


    def __init__(self, data):
        self.ssn = data.get('ssn')
        self.name = data.get('name')
        self.age = data.get('age')
        self.admited_on = datetime.datetime.utcnow() if not data.get('admited_on') else data.get('admited_on')
        self.type_of_bed = data.get('type_of_bed')
        self.address = data.get('address')
        self.state = data.get('state')
        self.city = data.get('city')
        self.discharged = data.get('discharged')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()

    @staticmethod
    def get_one_patient(id):
        return PatientModel.query.get(id)
    
    @staticmethod
    def get_all_patients():
        return PatientModel.query.all()

    @staticmethod
    def search(param):
        search = "%{}%".format(param)
        return PatientModel.query.filter(
            or_(
            PatientModel.name.like(search),
            PatientModel.id.like(search))).all()
    
    @staticmethod
    def get_patient_by_ssn(value):
        return PatientModel.query.filter_by(ssn=value).first()


def age(age):
    if (age < 1 or age > 999):
        raise ValidationError('Please enter a valid age')

def ssn(ssn):
    if(len(str(ssn)) != 9):
        raise ValidationError('Enter a valid ssn')

# Schema for serilazitation and validation
class PatientSchema(Schema):
    id = fields.Integer(dump_only=True)
    ssn = fields.Integer(required=True, validate=ssn, load_only=True)
    name = fields.String(required=True, validate=Regexp(regex=r'^[a-zA-Z ]+$', error="Name must conatin only alphabets"))
    age = fields.Integer(required=True, validate=age)
    admited_on = fields.DateTime()
    type_of_bed = fields.String(required=True)
    address = fields.String(required=True)
    state = fields.String(required=True, validate=Regexp(regex=r'^[a-zA-Z ]+$', error="State must conatin only alphabets"))
    city = fields.String(required=True, validate=Regexp(regex=r'^[a-zA-Z ]+$', error="City must conatin only alphabets"))
    discharged = fields.Boolean()
    medicines = fields.Nested(MedicineSchema, many=True)
    diagnostics = fields.Nested(DiagnosticsSchema, many=True)

    
