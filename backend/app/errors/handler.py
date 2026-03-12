from flask import jsonify
from werkzeug.exceptions import HTTPException
from ..exceptions.user_exceptions import APIException


def register_error_handlers(app):

    def handle_api_exception(e):
        response = {
            "success": False,
            "error": e.message,
            "type": e.__class__.__name__
        }

        return jsonify(response), e.status_code


    def handle_http_exception(e):
        response = {
            "success": False,
            "error": e.description,
            "type": e.name
        }

        return jsonify(response), e.code


    def handle_unexpected_exception(e):
        response = {
            "success": False,
            "error": "Internal server error",
            "type": "InternalServerError"
        }

        return jsonify(response), 500


    app.register_error_handler(APIException, handle_api_exception)
    app.register_error_handler(HTTPException, handle_http_exception)
    app.register_error_handler(Exception, handle_unexpected_exception)