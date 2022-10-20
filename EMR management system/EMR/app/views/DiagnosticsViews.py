# Imports
from flask import json, Response, Blueprint, request
from ..models.DiagnosticsModel import DiagnosticsModel, DiagnosticsSchema
from ..auth.auth import Auth
from marshmallow import ValidationError

diagnostics_api = Blueprint('diagnostics_api', __name__)
diagnostics_schema = DiagnosticsSchema()

# Endpoint for creation
@diagnostics_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    req_data = request.get_json()
    try:
        data = diagnostics_schema.load(req_data)
    except ValidationError as err:
        return custom_response(err.messages, 400)
    diagnostics = DiagnosticsModel(data)
    diagnostics.save()
    ser_data = diagnostics_schema.dump(diagnostics)
    return custom_response(ser_data, 201)


# Endpoint for deletion
@diagnostics_api.route('/<int:id>', methods=['DELETE'])
@Auth.auth_required
def delete(id):
    data = DiagnosticsModel.get_one_diagnostic(id)
    
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