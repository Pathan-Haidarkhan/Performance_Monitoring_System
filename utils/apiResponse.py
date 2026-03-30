from flask import jsonify


def api_response(success, message=None,data=None, error=None,status_code=200):
    response = {
        'success': success,
        'message': message,
        'data': data,
        'error': error,
    }
    return jsonify(response), status_code