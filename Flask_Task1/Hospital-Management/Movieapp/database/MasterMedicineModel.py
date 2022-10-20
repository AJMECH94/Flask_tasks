# Imports
from . import db
from marshmallow import fields, Schema, validates, ValidationError
from marshmallow.validate import Length, Regexp


class MasterMedicineModel(db.Model):
    '''
    ORM to manage Master Medicines
    '''
    __tablename__="master_medicine"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    rate = db.Column(db.Integer, nullable=False)
    m = db.relationship('MedicineModel', backref='complete', cascade="all, delete", lazy=True)
    


    def __init__(self, data):
        self.name = data.get('name')
        self.quantity = data.get('quantity')
        self.rate = data.get('rate')
    
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
    def get_all_medicines_available():
        return MasterMedicineModel.query.all()

    @staticmethod
    def get_one_medicine(id):
        return MasterMedicineModel.query.get(id)
    
    @staticmethod
    def check_validity_and_update(data):
        medicine = data.get('medicine')
        quantity = data.get('quantity')
        q = MasterMedicineModel.query.get(medicine)
        quantity_available = q.quantity
        if(quantity<=quantity_available or quantity<=0):
            q.quantity = q.quantity - quantity
            db.session.commit()
            return True
        return False


# Schema for serilazitation and validation
class MasterMedicineSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=Regexp(regex=r'^[a-zA-Z ]+$', error='Please enter a valid name'))
    quantity = fields.Integer(required=True)
    rate = fields.Integer(required=True)