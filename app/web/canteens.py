from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required
from app.web import web_bp
from app.models.canteen import Canteen
from app.models.school import School
from app.extensions import db
from app.utils.tenant_utils import roles_required

@web_bp.route("/admin/canteens")
@login_required
@roles_required("ADMIN_MASTER")
def list_canteens():
    """Lista todas as cantinas pre-cadastradas."""
    canteens = Canteen.query.all()
    return render_template("admin/canteens/list.html", canteens=canteens)

@web_bp.route("/admin/canteens/new", methods=["GET", "POST"])
@login_required
@roles_required("ADMIN_MASTER")
def create_canteen():
    """Cria uma nova cantina vinculada a uma escola."""
    schools = School.query.all()
    if request.method == "POST":
        name = request.form.get("name")
        school_id = request.form.get("school_id")
        
        if not name or not school_id:
            flash("Nome e Escola são obrigatórios.", "danger")
            return render_template("admin/canteens/form.html", canteen=None, schools=schools)
            
        try:
            canteen = Canteen(
                name=name,
                school_id=school_id
            )
            db.session.add(canteen)
            db.session.commit()
            flash("Cantina criada com sucesso!", "success")
            return redirect(url_for("web.list_canteens"))
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao criar cantina: {str(e)}", "danger")
            
    return render_template("admin/canteens/form.html", canteen=None, schools=schools)

@web_bp.route("/admin/canteens/<uuid:canteen_id>/edit", methods=["GET", "POST"])
@login_required
@roles_required("ADMIN_MASTER")
def edit_canteen(canteen_id):
    """Edita uma cantina existente."""
    canteen = Canteen.query.get_or_404(canteen_id)
    schools = School.query.all()
    
    if request.method == "POST":
        canteen.name = request.form.get("name")
        canteen.school_id = request.form.get("school_id")
        canteen.active = "active" in request.form
        
        try:
            db.session.commit()
            flash("Cantina atualizada com sucesso!", "success")
            return redirect(url_for("web.list_canteens"))
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao atualizar cantina: {str(e)}", "danger")
            
    return render_template("admin/canteens/form.html", canteen=canteen, schools=schools)

@web_bp.route("/admin/canteens/<uuid:canteen_id>/delete", methods=["POST"])
@login_required
@roles_required("ADMIN_MASTER")
def delete_canteen(canteen_id):
    """Remove (desativa) uma cantina."""
    canteen = Canteen.query.get_or_404(canteen_id)
    try:
        canteen.active = False
        db.session.commit()
        flash("Cantina desativada com sucesso!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao desativar cantina: {str(e)}", "danger")
    return redirect(url_for("web.list_canteens"))
