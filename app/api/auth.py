from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from app.api import api_bp
from app.models.user import User

@api_bp.route("/auth/login", methods=["POST"])
def login():
    """
    Autentica o usuário e retorna tokens JWT.
    Claims incluídas: identity (user_id), role, canteen_id.
    """
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "E-mail e senha são obrigatórios"}), 400

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        if not user.active:
            return jsonify({"error": "Usuário inativo"}), 401
            
        # Claims adicionais para o token
        additional_claims = {
            "role": user.role,
            "canteen_id": str(user.canteen_id) if user.canteen_id else None
        }

        access_token = create_access_token(identity=str(user.id), additional_claims=additional_claims)
        refresh_token = create_refresh_token(identity=str(user.id))

        return jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "id": str(user.id),
                "name": user.name,
                "role": user.role,
                "canteen_id": str(user.canteen_id) if user.canteen_id else None
            }
        }), 200

    return jsonify({"error": "Credenciais inválidas"}), 401
