from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from app.api import api_bp
from app.models.user import User
from functools import wraps

def require_role(role_name):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            user_role = claims.get("role")
            if user_role != role_name and user_role != "ADMIN_MASTER":
                return jsonify({"error": "Acesso negado."}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

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

@api_bp.route("/auth/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """
    Gera um novo access token a partir de um refresh token válido.
    Mantém claims de role e canteen_id.
    """
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or not user.active:
        return jsonify({"error": "Usuário inválido ou inativo"}), 401
        
    additional_claims = {
        "role": user.role,
        "canteen_id": str(user.canteen_id) if user.canteen_id else None
    }
    
    new_access_token = create_access_token(identity=user_id, additional_claims=additional_claims)
    return jsonify({"access_token": new_access_token}), 200
