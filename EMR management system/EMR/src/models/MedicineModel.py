# Imports
from . import db
from marshmallow import fields, Schema, validates, ValidationError
from marshmallow.validate import Length, Regexp
from .MasterMedicineModel import MasterMedicineSchema

class MedicineModel(db.Model):
    '''
    ORM to manage Medicines
    '''
    __tablename__ = "medicines"

    id = db.Column(db.Integer, primary_key=True)
    medicine = db.Column(db.Integer, db.ForeignKey('master_medicine.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    patient = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    medicines = db.relationship('MasterMedicineModel', backref='med', lazy=True)

    def __init__(self, data):
        self.quantity = data.get('quantity')
        self.medicine = data.get('medicine')
        self.patient = data.get('patient')
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    @staticmethod
    def get_one_medicine(id):
        return MedicineModel.query.get(id)


# Schema for serilazitation and validation
class MedicineSchema(Schema):
    medicine = fields.Integer(required=True)
    id = fields.Integer(dump_only=True)
    quantity = fields.Integer(required=True)
    patient = fields.Integer(required=True)
    medicines = fields.Nested(MasterMedicineSchema)