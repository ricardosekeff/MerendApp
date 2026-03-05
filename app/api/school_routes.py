from flask import request, jsonify
from app.api import api_bp
from app.extensions import db
from app.models.school import School
from app.api.schemas import SchoolSchema
from app.utils.tenant_utils import roles_required

school_schema = SchoolSchema()
schools_schema = SchoolSchema(many=True)

@api_bp.route("/schools", methods=["GET"])
@roles_required("ADMIN_MASTER")
def get_schools():
    """Retorna lista de todas as escolas."""
    schools = School.query.all()
    return jsonify(schools_schema.dump(schools)), 200

@api_bp.route("/schools", methods=["POST"])
@roles_required("ADMIN_MASTER")
def create_school():
    """Cria uma nova escola."""
    data = request.get_json()
    try:
        new_school = school_schema.load(data)
        db.session.add(new_school)
        db.session.commit()
        return jsonify(school_schema.dump(new_school)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Falha ao criar escola", "message": str(e)}), 400

@api_bp.route("/schools/<uuid:school_id>", methods=["GET"])
@roles_required("ADMIN_MASTER")
def get_school(school_id):
    """Pega detalhes de uma escola específica."""
    school = School.query.get_or_404(school_id)
    return jsonify(school_schema.dump(school)), 200

@api_bp.route("/schools/<uuid:school_id>", methods=["PUT"])
@roles_required("ADMIN_MASTER")
def update_school(school_id):
    """Atualiza dados de uma escola."""
    school = School.query.get_or_404(school_id)
    data = request.get_json()
    try:
        updated_school = school_schema.load(data, instance=school, partial=True)
        db.session.commit()
        return jsonify(school_schema.dump(updated_school)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Falha ao atualizar escola", "message": str(e)}), 400

@api_bp.route("/schools/<uuid:school_id>", methods=["DELETE"])
@roles_required("ADMIN_MASTER")
def delete_school(school_id):
    """Remove uma escola."""
    school = School.query.get_or_404(school_id)
    db.session.delete(school)
    db.session.commit()
    return jsonify({"message": "Escola removida com sucesso"}), 200
