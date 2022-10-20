# Imports
from . import db
from marshmallow import fields, Schema, validates, ValidationError
from marshmallow.validate import Length, Regexp


class MasterDiagnosticsModel(db.Model):
    '''
    ORM to manage Master Diagnostics
    '''
    __tablename__="master_diagnostics"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    rate = db.Column(db.Integer, nullable=False)
    d = db.relationship('DiagnosticsModel', backref='complete', cascade="all, delete", lazy=True)

    def __init__(self, data):
        self.name = data.get('name')
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
    def get_all_diagnostics_available():
        return MasterDiagnosticsModel.query.all()

    @staticmethod
    def get_one_diagnostics(id):
        return MasterDiagnosticsModel.query.get(id)


# Schema for serilazitation and validation
class MasterDiagnosticsSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=Regexp(regex=r'^[a-zA-Z ]+$', error='Please enter a valid name'))
    rate = fields.Integer(required=True)