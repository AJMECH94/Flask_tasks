# Imports
from ..models.MasterMedicineModel import MasterMedicineModel, MasterMedicineSchema
from  flask import Response, json, Blueprint, request
from marshmallow import ValidationError
from ..shared.auth import Auth

master_medicine_api = Blueprint('master_medicine_api', __name__)
master_medicine_schema = MasterMedicineSchema()

# Endpoint for creation
@master_medicine_api.route('/', methods=['POST'])
def create():
    req_data = request.get_json()
    try:
        data = master_medicine_schema.load(req_data)
    except ValidationError as err:
        return custom_response(err.messages, 400)
    master_medicine = MasterMedicineModel(data)
    master_medicine.save()
    res_data = master_medicine_schema.dump(master_medicine)
    return custom_response(res_data, 200)

# Endpoint for retrival
@master_medicine_api.route('/', methods=['GET'])
def get_medicine():
    data = MasterMedicineModel.get_all_medicines_available()
    res_data = master_medicine_schema.dump(data, many=True)
    return custom_response(res_data, 200)

# Endpoint for deletion 
@master_medicine_api.route('/<int:id>', methods=['DELETE'])
def delete(id):
    data = MasterMedicineModel.get_one_medicine(id)
    
    if not data:
        return custom_response({'error': 'No such medicine'}, 404)
    
    data.delete()
    return custom_response({'message': 'Deletion sucessfull'}, 204)


# Custom response
def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )


