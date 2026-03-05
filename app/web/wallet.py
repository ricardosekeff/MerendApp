from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.extensions import db
from app.web import web_bp
from app.models.wallet import Wallet, WalletLimit, WalletCategoryRestriction, WalletProductRestriction
from app.models.user import User
from app.models.category import Category
from app.models.product import Product

@web_bp.route("/wallet")
@login_required
def parent_wallet():
    """
    Exibe a carteira do usuário atual (Parente/Resp ou Aluno).
    Caso a carteira não exista, exibirá um botão/convite para criá-la.
    """
    # Para simplificar na ISSUE-15, assumimos que o próprio current_user 
    # visualiza sua carteira (na vida real o Parente veria a carteira do Filho dependente).
    wallet = Wallet.query_scoped().filter_by(user_id=current_user.id).first()
    
    # Se tivéssemos a relação responsavel->aluno, buscaríamos a wallet do aluno aqui.
    # Ex: student = User.query.filter_by(parent_id=current_user.id).first() -> wallet = student.wallet

    categories = Category.query_scoped().filter_by(status=True).all()
    products = Product.query_scoped().filter_by(status=True).all()

    # Mapear restrições atuais para checkboxes
    restricted_categories = []
    restricted_products = []
    if wallet:
        restricted_categories = [r.category_id for r in wallet.category_restrictions]
        restricted_products = [r.product_id for r in wallet.product_restrictions]

    return render_template(
        "parent/wallet.html", 
        wallet=wallet, 
        categories=categories, 
        products=products,
        restricted_categories=restricted_categories,
        restricted_products=restricted_products
    )

@web_bp.route("/wallet/create", methods=["POST"])
@login_required
def create_wallet_web():
    """Cria a carteira via requisição Web Frontend"""
    existing_wallet = Wallet.query_scoped().filter_by(user_id=current_user.id).first()
    if not existing_wallet:
        new_wallet = Wallet(user_id=current_user.id, balance=0.00, active=True)
        db.session.add(new_wallet)
        db.session.commit()
        flash("Carteira criada com sucesso!", "success")
    else:
        flash("Sua carteira já existe.", "info")
        
    return redirect(url_for("web.parent_wallet"))

@web_bp.route("/wallet/limits", methods=["POST"])
@login_required
def update_wallet_limits():
    """Atualiza limites diário, semanal e mensal via formulário HTML"""
    wallet = Wallet.query_scoped().filter_by(user_id=current_user.id).first()
    if not wallet:
        flash("Carteira não encontrada.", "danger")
        return redirect(url_for("web.parent_wallet"))

    daily_amount = request.form.get("daily_amount", 0, type=float)
    weekly_amount = request.form.get("weekly_amount", 0, type=float)
    monthly_amount = request.form.get("monthly_amount", 0, type=float)

    # Deleta limites atuais
    WalletLimit.query_scoped().filter_by(wallet_id=wallet.id).delete()

    if daily_amount > 0:
        db.session.add(WalletLimit(wallet_id=wallet.id, period_type="daily", amount=daily_amount))
    if weekly_amount > 0:
        db.session.add(WalletLimit(wallet_id=wallet.id, period_type="weekly", amount=weekly_amount))
    if monthly_amount > 0:
        db.session.add(WalletLimit(wallet_id=wallet.id, period_type="monthly", amount=monthly_amount))

    db.session.commit()
    flash("Limites de gastos atualizados com sucesso!", "success")
    return redirect(url_for("web.parent_wallet"))

@web_bp.route("/wallet/restrictions", methods=["POST"])
@login_required
def update_wallet_restrictions():
    """Atualiza as listas de restrição (categorias/produtos) via HTML."""
    wallet = Wallet.query_scoped().filter_by(user_id=current_user.id).first()
    if not wallet:
        flash("Carteira não encontrada.", "danger")
        return redirect(url_for("web.parent_wallet"))

    category_ids = request.form.getlist("restricted_categories")
    product_ids = request.form.getlist("restricted_products")

    # Deletar antigas
    WalletCategoryRestriction.query_scoped().filter_by(wallet_id=wallet.id).delete()
    WalletProductRestriction.query_scoped().filter_by(wallet_id=wallet.id).delete()

    import uuid
    for cid in category_ids:
        try:
            db.session.add(WalletCategoryRestriction(wallet_id=wallet.id, category_id=uuid.UUID(cid)))
        except ValueError:
            pass
            
    for pid in product_ids:
        try:
            db.session.add(WalletProductRestriction(wallet_id=wallet.id, product_id=uuid.UUID(pid)))
        except ValueError:
            pass

    db.session.commit()
    flash("Restrições de consumo atualizadas com sucesso!", "success")
    return redirect(url_for("web.parent_wallet"))
