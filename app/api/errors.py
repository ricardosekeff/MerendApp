from flask import jsonify

def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"error": "Bad Request", "message": str(e.description)}), 400

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not Found", "message": "O recurso solicitado não existe"}), 404

    @app.errorhandler(422)
    def unprocessable_entity(e):
        return jsonify({"error": "Unprocessable Entity", "message": str(e.description)}), 422

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"error": "Internal Server Error", "message": "Ocorreu um erro inesperado no servidor"}), 500
