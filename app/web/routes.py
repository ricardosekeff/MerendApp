from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from app.web import web_bp
from app.models.user import User

@web_bp.route("/")
@login_required
def index():
    """Renderiza o Dashboard principal."""
    return render_template("index.html")

@web_bp.route("/login", methods=["GET", "POST"])
def login():
    """Gerencia o login na interface web."""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            if not user.active:
                flash("Sua conta está inativa. Entre em contato com o suporte.", "warning")
            else:
                login_user(user)
                flash(f"Bem-vindo, {user.name}!", "success")
                return redirect(url_for("web.index"))
        else:
            flash("E-mail ou senha inválidos.", "danger")
            
    return render_template("auth/login.html")

@web_bp.route("/logout")
@login_required
def logout():
    """Realiza o logout do usuário."""
    logout_user()
    flash("Você saiu do sistema.", "info")
    return redirect(url_for("web.login"))
