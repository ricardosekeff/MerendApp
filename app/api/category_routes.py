from flask import request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.api import api_bp
from app.models.category import Category
from app.api.schemas import CategorySchema
from app.api.auth import require_role
from sqlalchemy.exc import IntegrityError

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)

@api_bp.route("/categories", methods=["GET"])
@jwt_required()
def get_categories():
    """
    Lista todas as categorias da cantina
    Futuramente será fitrado pelo canteen_id no g (Tenant)
    """
    categories = Category.query_scoped().all()
    return jsonify(categories_schema.dump(categories)), 200

@api_bp.route("/categories/<uuid:category_id>", methods=["GET"])
@jwt_required()
def get_category(category_id):
    category = Category.query_scoped().filter_by(id=category_id).first_or_404()
    return jsonify(category_schema.dump(category)), 200

@api_bp.route("/categories", methods=["POST"])
@jwt_required()
@require_role("GESTOR")
def create_category():
    data = request.get_json()
    errors = category_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        new_category = category_schema.load(data, session=db.session)
        # TODO: Quando o auth injetar o canteen_id real do gestor no JWT:
        # from flask import g
        # new_category.canteen_id = g.canteen_id
        
        db.session.add(new_category)
        db.session.commit()
        return jsonify(category_schema.dump(new_category)), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Código de categoria já existente nesta cantina"}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

@api_bp.route("/categories/<uuid:category_id>", methods=["PUT"])
@jwt_required()
@require_role("GESTOR")
def update_category(category_id):
    category = Category.query_scoped().filter_by(id=category_id).first_or_404()
    data = request.get_json()
    
    errors = category_schema.validate(data, partial=True)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        category = category_schema.load(data, instance=category, partial=True, session=db.session)
        db.session.commit()
        return jsonify(category_schema.dump(category)), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Código de categoria já existente nesta cantina"}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500
