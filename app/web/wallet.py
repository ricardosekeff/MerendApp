from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.extensions import db
from app.web import web_bp
from app.models.wallet import Wallet, WalletLimit
from app.models.user import User

@web_bp.route("/wallet")
@login_required
def parent_wallet():
    """
    Exibe a carteira do usuário atual (Parente/Resp ou Aluno).
    Caso a carteira não exista, exibirá um botão/convite para criá-la.
    """
    # Se for PARENTE, pega a carteira do primeiro Filho. Se for ALUNO, pega a dele.
    if current_user.role == "RESPONSAVEL":
        student = User.query.filter_by(parent_id=current_user.id).first()
        wallet = Wallet.query_scoped().filter_by(user_id=student.id).first() if student else None
    else:
        wallet = Wallet.query_scoped().filter_by(user_id=current_user.id).first()
        
    recent_transactions = []
    if wallet:
        recent_transactions = sorted(wallet.transactions, key=lambda t: t.created_at, reverse=True)[:5]

    return render_template("parent/wallet.html", wallet=wallet, recent_transactions=recent_transactions)

@web_bp.route("/wallet/create", methods=["POST"])
@login_required
def create_wallet_web():
    """Cria a carteira via requisição Web Frontend"""
    if current_user.role == "RESPONSAVEL":
        # Se for parente, ele tentará criar para o primeiro filho.
        student = User.query.filter_by(parent_id=current_user.id).first()
        target_id = student.id if student else None
    else:
        target_id = current_user.id
        
    if not target_id:
        flash("Nenhum usuário alvo encontrado para criar carteira.", "danger")
        return redirect(url_for("web.parent_wallet"))
        
    existing_wallet = Wallet.query_scoped().filter_by(user_id=target_id).first()
    if not existing_wallet:
        new_wallet = Wallet(user_id=target_id, balance=0.00, active=True)
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
    if current_user.role == "RESPONSAVEL":
        student = User.query.filter_by(parent_id=current_user.id).first()
        wallet = Wallet.query_scoped().filter_by(user_id=student.id).first() if student else None
    else:
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

@web_bp.route("/wallet/recharge_permission", methods=["POST"])
@login_required
def update_recharge_permission_web():
    """Toggle web da permissão de recarregar a carteira via html"""
    if current_user.role == "RESPONSAVEL":
        student = User.query.filter_by(parent_id=current_user.id).first()
        wallet = Wallet.query_scoped().filter_by(user_id=student.id).first() if student else None
    else:
        wallet = Wallet.query_scoped().filter_by(user_id=current_user.id).first()
        
    if not wallet:
        flash("Carteira não encontrada.", "danger")
        return redirect(url_for("web.parent_wallet"))

    # Verifica se o checkbox 'student_can_recharge' veia no payload (como on/off/true)
    student_can_recharge = request.form.get("student_can_recharge") == "on"

    wallet.student_can_recharge = student_can_recharge
    db.session.commit()
    
    status_msg = "Permitir" if student_can_recharge else "Bloquear"
    flash(f"Configuração '{status_msg} aluno recarregar' salva com sucesso!", "success")
    return redirect(url_for("web.parent_wallet"))

@web_bp.route("/wallet/statement", methods=["GET"])
@login_required
def wallet_statement():
    """Visualização Web do Extrato de Transações Financeiras (Parent's View)"""
    if current_user.role == "RESPONSAVEL":
        student = User.query.filter_by(parent_id=current_user.id).first()
        wallet = Wallet.query_scoped().filter_by(user_id=student.id).first() if student else None
    else:
        wallet = Wallet.query_scoped().filter_by(user_id=current_user.id).first()
    
    if not wallet:
        flash("Nenhuma carteira digital encontrada para sua conta.", "warning")
        return redirect(url_for("web.index"))
        
    transactions = sorted(wallet.transactions, key=lambda t: t.created_at, reverse=True)
    
    return render_template("parent/wallet_statement.html", wallet=wallet, transactions=transactions)

@web_bp.route("/wallet/recharge", methods=["POST"])
@login_required
def recharge_wallet_web():
    """Adiciona saldo à carteira do aluno simulando Pix/Cartão"""
    from decimal import Decimal
    
    amount_str = request.form.get("amount", "0")
    try:
        amount = Decimal(amount_str)
    except Exception:
        amount = Decimal('0.0')
        
    if amount <= 0:
        flash("Valor inválido para recarga.", "danger")
        return redirect(url_for("web.parent_wallet"))
        
    if current_user.role == "RESPONSAVEL":
        student = User.query.filter_by(parent_id=current_user.id).first()
        wallet = Wallet.query_scoped().filter_by(user_id=student.id).first() if student else None
    else:
        wallet = Wallet.query_scoped().filter_by(user_id=current_user.id).first()
        # Se for aluno, verificar se ele tem permissão ativa do Parente
        if wallet and not wallet.student_can_recharge:
            flash("Sua recarga foi bloqueada pelo Responsável. Solicite a liberação no aplicativo.", "danger")
            return redirect(url_for("web.parent_wallet"))
            
    if not wallet:
        flash("Carteira não encontrada.", "danger")
        return redirect(url_for("web.parent_wallet"))

    wallet.balance += amount
    
    # Gerando Comprovante de Transação
    from app.models.wallet import WalletTransaction
    tx = WalletTransaction(
        wallet_id=wallet.id,
        amount=amount,
        transaction_type="credit",
        description="Recarga via PIX/Cartão"
    )
    db.session.add(tx)
    db.session.commit()
    
    flash(f"Recarga de R$ {amount:.2f} realizada com sucesso!", "success")
    return redirect(url_for("web.parent_wallet"))
