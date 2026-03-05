from flask import render_template, redirect, url_for, request, flash
from app.web import web_bp
from app.models.user import User

@web_bp.route("/")
def index():
    """Redireciona para o login por padrão na Sprint 1."""
    return redirect(url_for("web.login"))

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
                flash(f"Bem-vindo, {user.name}!", "success")
                # Por enquanto, redireciona para a home (que voltará para cá na Sprint 1)
                # ou poderíamos criar uma rota de dashboard básica.
                return redirect(url_for("web.index"))
        else:
            flash("E-mail ou senha inválidos.", "danger")
            
    return render_template("auth/login.html")
