from flask import jsonify
from app.api import api_bp

@api_bp.route("/health", methods=["GET"])
def health():
    """Health check endpoint para a API."""
    return jsonify({"status": "ok", "service": "api"}), 200
