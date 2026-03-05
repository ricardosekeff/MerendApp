from flask import request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.api import api_bp
from app.models.combo import Combo, ComboItem
from app.api.schemas import ComboSchema
from app.api.auth import require_role
from sqlalchemy.exc import IntegrityError
import uuid

combo_schema = ComboSchema()
combos_schema = ComboSchema(many=True)

@api_bp.route("/combos", methods=["GET"])
@jwt_required()
def get_combos():
    combos = Combo.query_scoped().all()
    return jsonify(combos_schema.dump(combos)), 200

@api_bp.route("/combos/<uuid:combo_id>", methods=["GET"])
@jwt_required()
def get_combo(combo_id):
    combo = Combo.query_scoped().filter_by(id=combo_id).first_or_404()
    return jsonify(combo_schema.dump(combo)), 200

@api_bp.route("/combos", methods=["POST"])
@jwt_required()
@require_role("GESTOR")
def create_combo():
    data = request.get_json()
    items_data = data.pop("items", [])
    
    errors = combo_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        new_combo = combo_schema.load(data, session=db.session)
        
        for item in items_data:
            combo_item = ComboItem(product_id=uuid.UUID(item["product_id"]), quantity=item.get("quantity", 1))
            new_combo.items.append(combo_item)

        db.session.add(new_combo)
        db.session.commit()
        return jsonify(combo_schema.dump(new_combo)), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Código de combo já existente nesta cantina"}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

@api_bp.route("/combos/<uuid:combo_id>", methods=["PUT"])
@jwt_required()
@require_role("GESTOR")
def update_combo(combo_id):
    combo = Combo.query_scoped().filter_by(id=combo_id).first_or_404()
    data = request.get_json()
    items_data = data.pop("items", None)
    
    errors = combo_schema.validate(data, partial=True)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        combo = combo_schema.load(data, instance=combo, partial=True, session=db.session)
        
        # Atualização dos itens
        if items_data is not None:
            # Drop de itens antigos
            for old_item in combo.items[:]:
                db.session.delete(old_item)
            combo.items = []
            
            # Recriação
            for item in items_data:
                combo_item = ComboItem(product_id=uuid.UUID(item["product_id"]), quantity=item.get("quantity", 1))
                combo.items.append(combo_item)
                
        db.session.commit()
        return jsonify(combo_schema.dump(combo)), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Código de combo já existente nesta cantina"}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

@api_bp.route("/combos/<uuid:combo_id>", methods=["DELETE"])
@jwt_required()
@require_role("GESTOR")
def delete_combo(combo_id):
    combo = Combo.query_scoped().filter_by(id=combo_id).first_or_404()
    try:
        db.session.delete(combo)
        db.session.commit()
        return "", 204
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500
