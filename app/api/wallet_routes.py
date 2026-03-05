from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.api import api_bp
from app.models.wallet import Wallet, WalletLimit, WalletCategoryRestriction, WalletProductRestriction
from app.models.user import User
from app.models.category import Category
from app.models.product import Product
from app.api.schemas import WalletSchema, WalletLimitSchema, WalletCategoryRestrictionSchema, WalletProductRestrictionSchema

wallet_schema = WalletSchema()
limit_schema = WalletLimitSchema(many=True)

@api_bp.route("/wallets", methods=["POST"])
@jwt_required()
def create_wallet():
    """Cria a carteira de um usuário se não existir."""
    data = request.get_json()
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"message": "user_id is required."}), 400

    existing_wallet = Wallet.query_scoped().filter_by(user_id=user_id).first()
    if existing_wallet:
        return jsonify({"message": "Wallet already exists for this user."}), 409

    try:
        new_wallet = Wallet(user_id=user_id, balance=0.00, active=True)
        db.session.add(new_wallet)
        db.session.commit()
        return jsonify(wallet_schema.dump(new_wallet)), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "User not found or Integrity Error."}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

@api_bp.route("/wallets/<uuid:user_id>", methods=["GET"])
@jwt_required()
def get_wallet(user_id):
    """Busca a carteira de um usuário."""
    wallet = Wallet.query_scoped().filter_by(user_id=user_id).first()
    if not wallet:
        return jsonify({"message": "Wallet not found"}), 404
        
    return jsonify(wallet_schema.dump(wallet)), 200

@api_bp.route("/wallets/<uuid:wallet_id>/limits", methods=["POST"])
@jwt_required()
def set_wallet_limits(wallet_id):
    """
    Define os limites da carteira (daily, weekly, monthly).
    Recebe listagem: [{"period_type": "daily", "amount": 20.00}, ...]
    Substitui os limites anteriores daquele tipo.
    """
    wallet = Wallet.query_scoped().filter_by(id=wallet_id).first_or_404()
    data = request.get_json()

    if not isinstance(data, list):
        return jsonify({"message": "Expected a list of limits."}), 400

    try:
        # Remover limites atuais para reescrever
        WalletLimit.query_scoped().filter_by(wallet_id=wallet.id).delete()
        
        valid_periods = ["daily", "weekly", "monthly"]
        for p in data:
            if p.get("period_type") in valid_periods:
                new_limit = WalletLimit(
                    wallet_id=wallet.id,
                    period_type=p["period_type"],
                    amount=p.get("amount", 0.0)
                )
                db.session.add(new_limit)

        db.session.commit()
        
        # Reload relation
        db.session.refresh(wallet)
        return jsonify(wallet_schema.dump(wallet)), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

@api_bp.route("/wallets/<uuid:wallet_id>/restrictions/categories", methods=["POST"])
@jwt_required()
def set_wallet_category_restrictions(wallet_id):
    """Atualiza a lista de categorias restritas da carteira."""
    wallet = Wallet.query_scoped().filter_by(id=wallet_id).first_or_404()
    data = request.get_json()

    if not isinstance(data, list):
        return jsonify({"message": "Expected a list of category UUIDs."}), 400

    try:
        WalletCategoryRestriction.query_scoped().filter_by(wallet_id=wallet.id).delete()
        
        for cat_id in data:
            if Category.query_scoped().filter_by(id=cat_id).first():
                new_restriction = WalletCategoryRestriction(wallet_id=wallet.id, category_id=cat_id)
                db.session.add(new_restriction)
                
        db.session.commit()
        db.session.refresh(wallet)
        return jsonify(wallet_schema.dump(wallet)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

@api_bp.route("/wallets/<uuid:wallet_id>/restrictions/products", methods=["POST"])
@jwt_required()
def set_wallet_product_restrictions(wallet_id):
    """Atualiza a lista de produtos restritos da carteira."""
    wallet = Wallet.query_scoped().filter_by(id=wallet_id).first_or_404()
    data = request.get_json()

    if not isinstance(data, list):
        return jsonify({"message": "Expected a list of product UUIDs."}), 400

    try:
        WalletProductRestriction.query_scoped().filter_by(wallet_id=wallet.id).delete()
        
        for prod_id in data:
            if Product.query_scoped().filter_by(id=prod_id).first():
                new_restriction = WalletProductRestriction(wallet_id=wallet.id, product_id=prod_id)
                db.session.add(new_restriction)
                
        db.session.commit()
        db.session.refresh(wallet)
        return jsonify(wallet_schema.dump(wallet)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500
