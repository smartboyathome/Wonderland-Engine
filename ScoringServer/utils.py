from copy import deepcopy
import json
from flask import Response

def dict_to_mongodb_list(data):
    if is_compound_dict(data):
        data_list = []
        for key in data:
            new_data = deepcopy(data[key])
            new_data['id'] = key
            data_list.append(new_data)
        return data_list


def is_compound_dict(data):
    if type(data) is not dict:
        return False
    for key in data:
        if type(data[key]) is not dict:
            return False
    return True

def mongodb_list_to_dict(data):
    if is_mongodb_list(data):
        data_dict = {}
        for item in data:
            new_data = deepcopy(item)
            key = new_data['id']
            del new_data['id']
            if '_id' in new_data:
                del new_data['_id']
            data_dict[key] = new_data
        return data_dict

def is_mongodb_list(data):
    if type(data) is not list:
        return False
    for item in data:
        if type(item) is not dict and 'id' not in item:
            return False
    return True

def create_error_response(error_type, reason, status_code=403):
    error = {
        "type": error_type,
        "reason": reason
    }
    resp = Response(json.dumps(error), status=status_code, mimetype='application/json')
    return resp