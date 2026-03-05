from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.web import web_bp
from app.extensions import db
from app.models.category import Category
from app.models.canteen import Canteen


@web_bp.route("/categories")
@login_required
def list_categories():
    categories = Category.query.all()
    return render_template("admin/categories/list.html", categories=categories)


@web_bp.route("/categories/new", methods=["GET", "POST"])
@login_required
def create_category():
    if request.method == "POST":
        try:
            category = Category(
                code=request.form.get("code"),
                name=request.form.get("name"),
                short_name=request.form.get("short_name"),
                safety_stock=int(request.form.get("safety_stock", 0)),
                status=request.form.get("status") == "on",
                canteen_id=request.form.get("canteen_id")
            )
            db.session.add(category)
            db.session.commit()
            flash("Categoria criada com sucesso!", "success")
            return redirect(url_for("web.list_categories"))
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao criar categoria: {e}", "danger")

    canteens = Canteen.query.all()
    return render_template("admin/categories/form.html", category=None, canteens=canteens)


@web_bp.route("/categories/<uuid:category_id>/edit", methods=["GET", "POST"])
@login_required
def edit_category(category_id):
    category = db.session.get(Category, category_id)
    if not category:
        flash("Categoria não encontrada.", "danger")
        return redirect(url_for("web.list_categories"))

    if request.method == "POST":
        try:
            category.code = request.form.get("code")
            category.name = request.form.get("name")
            category.short_name = request.form.get("short_name")
            category.safety_stock = int(request.form.get("safety_stock", 0))
            category.status = request.form.get("status") == "on"
            db.session.commit()
            flash("Categoria atualizada com sucesso!", "success")
            return redirect(url_for("web.list_categories"))
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao atualizar categoria: {e}", "danger")

    canteens = [{"id": str(category.canteen_id), "name": "Cantina Atual"}]
    return render_template("admin/categories/form.html", category=category, canteens=canteens)
