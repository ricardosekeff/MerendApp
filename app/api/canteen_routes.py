from flask import request, jsonify
from app.api import api_bp
from app.extensions import db
from app.models.canteen import Canteen
from app.api.schemas import CanteenSchema
from app.utils.tenant_utils import roles_required

canteen_schema = CanteenSchema()
canteens_schema = CanteenSchema(many=True)

@api_bp.route("/canteens", methods=["GET"])
@roles_required("ADMIN_MASTER")
def get_canteens():
    """Retorna lista de todas as cantinas (acesso global para admin)."""
    # Na Sprint 1 ainda não filtramos por tenant no GET global de admin
    canteens = Canteen.query.all()
    return jsonify(canteens_schema.dump(canteens)), 200

@api_bp.route("/schools/<uuid:school_id>/canteens", methods=["POST"])
@roles_required("ADMIN_MASTER")
def create_canteen(school_id):
    """Cria uma nova cantina vinculada a uma escola."""
    data = request.get_json()
    try:
        data["school_id"] = str(school_id)
        new_canteen = canteen_schema.load(data)
        db.session.add(new_canteen)
        db.session.commit()
        return jsonify(canteen_schema.dump(new_canteen)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Falha ao criar cantina", "message": str(e)}), 400

@api_bp.route("/canteens/<uuid:canteen_id>", methods=["GET"])
@roles_required("ADMIN_MASTER")
def get_canteen(canteen_id):
    """Pega detalhes de uma cantina específica."""
    canteen = Canteen.query.get_or_404(canteen_id)
    return jsonify(canteen_schema.dump(canteen)), 200

@api_bp.route("/canteens/<uuid:canteen_id>", methods=["PUT"])
@roles_required("ADMIN_MASTER")
def update_canteen(canteen_id):
    """Atualiza dados de uma cantina."""
    canteen = Canteen.query.get_or_404(canteen_id)
    data = request.get_json()
    try:
        updated_canteen = canteen_schema.load(data, instance=canteen, partial=True)
        db.session.commit()
        return jsonify(canteen_schema.dump(updated_canteen)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Falha ao atualizar cantina", "message": str(e)}), 400

@api_bp.route("/canteens/<uuid:canteen_id>", methods=["DELETE"])
@roles_required("ADMIN_MASTER")
def delete_canteen(canteen_id):
    """Remove uma cantina."""
    canteen = Canteen.query.get_or_404(canteen_id)
    db.session.delete(canteen)
    db.session.commit()
    return jsonify({"message": "Cantina removida com sucesso"}), 200
