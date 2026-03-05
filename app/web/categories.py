import urllib.request
import urllib.error
import urllib.parse
import json
from flask import render_template, request, redirect, url_for, flash, current_app, session
from app.web import web_bp

# Utility para fazer requisições à própria API
def _api_request(method, endpoint, data=None):
    token = session.get("access_token")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    url = f"http://127.0.0.1:8000/api{endpoint}"
    
    req = urllib.request.Request(url, method=method, headers=headers)
    
    if data:
        json_data = json.dumps(data).encode('utf-8')
        req.add_header('Content-Type', 'application/json')
        req.data = json_data
        
    class DummyResponse:
        def __init__(self, status_code, json_data):
            self.status_code = status_code
            self._json_data = json_data
        def json(self):
            return self._json_data

    try:
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode('utf-8')
            return DummyResponse(response.status, json.loads(res_body) if res_body else {})
    except urllib.error.HTTPError as e:
        res_body = e.read().decode('utf-8')
        return DummyResponse(e.code, json.loads(res_body) if res_body else {})
    except Exception as e:
        return None

@web_bp.route("/categories")
def list_categories():
    response = _api_request("GET", "/categories")
    categories = response.json() if response and response.status_code == 200 else []
    return render_template("admin/categories/list.html", categories=categories)

@web_bp.route("/categories/new", methods=["GET", "POST"])
def create_category():
    if request.method == "POST":
        data = {
            "code": request.form.get("code"),
            "name": request.form.get("name"),
            "short_name": request.form.get("short_name"),
            "safety_stock": int(request.form.get("safety_stock", 0)),
            "status": request.form.get("status") == "on",
            "canteen_id": request.form.get("canteen_id") # TODO: Obter o canteen_id via sessão ou contexto
        }
        response = _api_request("POST", "/categories", data=data)
        if response and response.status_code == 201:
            flash("Categoria criada com sucesso!", "success")
            return redirect(url_for("web.list_categories"))
        else:
            msg = response.json().get("message", "Erro ao criar categoria") if response else "Erro de conexão"
            flash(msg, "danger")

    # MOCK Canteens para o form (até a injeção do contexto do logado)
    response_c = _api_request("GET", "/canteens")
    canteens = response_c.json() if response_c and response_c.status_code == 200 else []
    
    return render_template("admin/categories/form.html", category=None, canteens=canteens)

@web_bp.route("/categories/<uuid:category_id>/edit", methods=["GET", "POST"])
def edit_category(category_id):
    if request.method == "POST":
        data = {
            "code": request.form.get("code"),
            "name": request.form.get("name"),
            "short_name": request.form.get("short_name"),
            "safety_stock": int(request.form.get("safety_stock", 0)),
            "status": request.form.get("status") == "on"
        }
        response = _api_request("PUT", f"/categories/{category_id}", data=data)
        if response and response.status_code == 200:
            flash("Categoria atualizada com sucesso!", "success")
            return redirect(url_for("web.list_categories"))
        else:
            msg = response.json().get("message", "Erro ao atualizar categoria") if response else "Erro de conexão"
            flash(msg, "danger")

    response = _api_request("GET", f"/categories/{category_id}")
    category = response.json() if response and response.status_code == 200 else None
    
    if not category:
        flash("Categoria não encontrada.", "danger")
        return redirect(url_for("web.list_categories"))

    return render_template("admin/categories/form.html", category=category, canteens=[{"id": category["canteen_id"], "name": "Cantina Atual"}])
