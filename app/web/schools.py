from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.web import web_bp
from app.models.school import School
from app.extensions import db
from app.utils.tenant_utils import roles_required


def _empty_or_none(value):
    """Converte string vazia ou None para None (SQL NULL)."""
    if value is None:
        return None
    stripped = value.strip()
    return stripped if stripped else None

@web_bp.route("/admin/schools")
@login_required
@roles_required("ADMIN_MASTER")
def list_schools():
    """Lista todas as escolas cadastradas."""
    schools = School.query.all()
    return render_template("admin/schools/list.html", schools=schools)

@web_bp.route("/admin/schools/new", methods=["GET", "POST"])
@login_required
@roles_required("ADMIN_MASTER")
def create_school():
    """Cria uma nova escola."""
    if request.method == "POST":
        name = request.form.get("name")
        cnpj = request.form.get("cnpj")
        phone = _empty_or_none(request.form.get("phone"))
        address = _empty_or_none(request.form.get("address"))
        city = _empty_or_none(request.form.get("city"))
        state = _empty_or_none(request.form.get("state"))
        
        if not name or not cnpj:
            flash("Nome e CNPJ são obrigatórios.", "danger")
            return render_template("admin/schools/form.html", school=None)
            
        try:
            school = School(
                name=name,
                cnpj=cnpj,
                phone=phone,
                address=address,
                city=city,
                state=state
            )
            db.session.add(school)
            db.session.commit()
            flash("Escola criada com sucesso!", "success")
            return redirect(url_for("web.list_schools"))
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao criar escola: {str(e)}", "danger")
            
    return render_template("admin/schools/form.html", school=None)

@web_bp.route("/admin/schools/<uuid:school_id>/edit", methods=["GET", "POST"])
@login_required
@roles_required("ADMIN_MASTER")
def edit_school(school_id):
    """Edita uma escola existente."""
    school = School.query.get_or_404(school_id)
    
    if request.method == "POST":
        school.name = request.form.get("name")
        school.cnpj = request.form.get("cnpj")
        school.phone = _empty_or_none(request.form.get("phone"))
        school.address = _empty_or_none(request.form.get("address"))
        school.city = _empty_or_none(request.form.get("city"))
        school.state = _empty_or_none(request.form.get("state"))
        school.active = "active" in request.form
        
        try:
            db.session.commit()
            flash("Escola atualizada com sucesso!", "success")
            return redirect(url_for("web.list_schools"))
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao atualizar escola: {str(e)}", "danger")
            
    return render_template("admin/schools/form.html", school=school)

@web_bp.route("/admin/schools/<uuid:school_id>/delete", methods=["POST"])
@login_required
@roles_required("ADMIN_MASTER")
def delete_school(school_id):
    """Remove (desativa) uma escola."""
    school = School.query.get_or_404(school_id)
    try:
        # Soft delete ou hard delete? Issue #45 diz "remover (soft delete via is_active)"
        school.active = False
        db.session.commit()
        flash("Escola desativada com sucesso!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao desativar escola: {str(e)}", "danger")
    return redirect(url_for("web.list_schools"))
