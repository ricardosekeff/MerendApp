from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.web import web_bp
from app.extensions import db
from app.models.product import Product
from app.models.category import Category
from app.models.canteen import Canteen


@web_bp.route("/products")
@login_required
def list_products():
    products = Product.query.all()
    return render_template("admin/products/list.html", products=products)


@web_bp.route("/products/new", methods=["GET", "POST"])
@login_required
def create_product():
    if request.method == "POST":
        try:
            product = Product(
                code=request.form.get("code"),
                name=request.form.get("name"),
                short_name=request.form.get("short_name"),
                stock=int(request.form.get("stock", 0)),
                cost_price=float(request.form.get("cost_price", 0.0)),
                sell_price=float(request.form.get("sell_price", 0.0)),
                status=request.form.get("status") == "on",
                category_id=request.form.get("category_id"),
                canteen_id=request.form.get("canteen_id")
            )
            db.session.add(product)
            db.session.commit()
            flash("Produto criado com sucesso!", "success")
            return redirect(url_for("web.list_products"))
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao criar produto: {e}", "danger")

    canteens = Canteen.query.all()
    categories = Category.query.all()
    return render_template("admin/products/form.html", product=None, canteens=canteens, categories=categories)


@web_bp.route("/products/<uuid:product_id>/edit", methods=["GET", "POST"])
@login_required
def edit_product(product_id):
    product = db.session.get(Product, product_id)
    if not product:
        flash("Produto não encontrado.", "danger")
        return redirect(url_for("web.list_products"))

    if request.method == "POST":
        try:
            product.code = request.form.get("code")
            product.name = request.form.get("name")
            product.short_name = request.form.get("short_name")
            product.stock = int(request.form.get("stock", 0))
            product.cost_price = float(request.form.get("cost_price", 0.0))
            product.sell_price = float(request.form.get("sell_price", 0.0))
            product.category_id = request.form.get("category_id")
            product.status = request.form.get("status") == "on"
            db.session.commit()
            flash("Produto atualizado com sucesso!", "success")
            return redirect(url_for("web.list_products"))
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao atualizar produto: {e}", "danger")

    categories = Category.query.all()
    return render_template("admin/products/form.html", product=product, canteens=[product.canteen] if product.canteen else [], categories=categories)
