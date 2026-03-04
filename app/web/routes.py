from flask import render_template, redirect, url_for
from app.web import web_bp

@web_bp.route("/")
def index():
    """Redireciona para o login por padrão na Sprint 1."""
    return redirect(url_for("web.login"))

@web_bp.route("/login")
def login():
    """Renderiza a página de login."""
    return render_template("auth/login.html")
