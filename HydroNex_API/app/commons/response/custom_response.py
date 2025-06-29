from flask import jsonify

class CustomResponse:
    @staticmethod
    def success(message: str, data=None, status_code: int = 200):
        response = {
            'success': True,
            'message': message
        }
        if data is not None:
            response['data'] = data
        return jsonify(response), status_code

    @staticmethod
    def error(message: str, status_code: int = 400):
        response = {
            'success': False,
            'message': message
        }
        return jsonify(response), status_code 