# Imports
from ..models.MasterDiagnosticsModel import MasterDiagnosticsModel, MasterDiagnosticsSchema
from  flask import Response, json, Blueprint, request
from marshmallow import ValidationError
from ..auth.auth import Auth

master_diagnostics_api = Blueprint('master_diagnostics_api', __name__)
master_diagnostics_schema = MasterDiagnosticsSchema()

# Endpoint for creation
@master_diagnostics_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    req_data = request.get_json()
    try:
        data = master_diagnostics_schema.load(req_data)
    except ValidationError as err:
        return custom_response(err.messages, 400)
    master_diagnostics = MasterDiagnosticsModel(data)
    master_diagnostics.save()
    res_data = master_diagnostics_schema.dump(master_diagnostics)
    return custom_response(res_data, 201)

# Endpoint for retrival 
@master_diagnostics_api.route('/', methods=['GET'])
@Auth.auth_required
def get_diagnostics():
    data = MasterDiagnosticsModel.get_all_diagnostics_available()
    res_data = master_diagnostics_schema.dump(data, many=True)
    return custom_response(res_data, 200)

# Endpoint for deletion
@master_diagnostics_api.route('/<int:id>', methods=['DELETE'])
@Auth.auth_required
def delete(id):
    data = MasterDiagnosticsModel.get_one_diagnostics(id)
    
    if not data:
        return custom_response({'error': 'No such diagnostics'}, 404)
    
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


