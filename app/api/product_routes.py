from flask import request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.api import api_bp
from app.models.product import Product
from app.api.schemas import ProductSchema
from app.api.auth import require_role
from sqlalchemy.exc import IntegrityError

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

@api_bp.route("/products", methods=["GET"])
@jwt_required()
def get_products():
    """
    Lista todos os produtos.
    """
    products = Product.query_scoped().all()
    return jsonify(products_schema.dump(products)), 200

@api_bp.route("/products/<uuid:product_id>", methods=["GET"])
@jwt_required()
def get_product(product_id):
    product = Product.query_scoped().filter_by(id=product_id).first_or_404()
    return jsonify(product_schema.dump(product)), 200

@api_bp.route("/products", methods=["POST"])
@jwt_required()
@require_role("GESTOR")
def create_product():
    data = request.get_json()
    errors = product_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        new_product = product_schema.load(data, session=db.session)
        # TODO: Inject canteen_id real do gestor no JWT
        # new_product.canteen_id = g.canteen_id
        
        db.session.add(new_product)
        db.session.commit()
        return jsonify(product_schema.dump(new_product)), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Integrity Error: Verifique as dependências, como a categoria associada."}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

@api_bp.route("/products/<uuid:product_id>", methods=["PUT"])
@jwt_required()
@require_role("GESTOR")
def update_product(product_id):
    product = Product.query_scoped().filter_by(id=product_id).first_or_404()
    data = request.get_json()
    
    errors = product_schema.validate(data, partial=True)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        product = product_schema.load(data, instance=product, partial=True, session=db.session)
        db.session.commit()
        return jsonify(product_schema.dump(product)), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Integrity Error."}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500
