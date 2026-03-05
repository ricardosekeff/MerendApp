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

@web_bp.route("/products")
def list_products():
    response = _api_request("GET", "/products")
    products = response.json() if response and response.status_code == 200 else []
    
    # Busca categorias para dar display do nome da categoria
    cat_response = _api_request("GET", "/categories")
    categories = cat_response.json() if cat_response and cat_response.status_code == 200 else []
    cat_dict = {cat['id']: cat['name'] for cat in categories}
    
    for p in products:
        p['category_name'] = cat_dict.get(p.get('category_id'), 'Desconhecida')

    return render_template("admin/products/list.html", products=products)

@web_bp.route("/products/new", methods=["GET", "POST"])
def create_product():
    if request.method == "POST":
        data = {
            "code": request.form.get("code"),
            "name": request.form.get("name"),
            "short_name": request.form.get("short_name"),
            "stock": int(request.form.get("stock", 0)),
            "cost_price": float(request.form.get("cost_price", 0.0)),
            "sell_price": float(request.form.get("sell_price", 0.0)),
            "status": request.form.get("status") == "on",
            "category_id": request.form.get("category_id"),
            "canteen_id": request.form.get("canteen_id") # TODO: Inject backend side
        }
        response = _api_request("POST", "/products", data=data)
        if response and response.status_code == 201:
            flash("Produto criado com sucesso!", "success")
            return redirect(url_for("web.list_products"))
        else:
            msg = response.json().get("message", "Erro ao criar produto") if response else "Erro de conexão"
            flash(msg, "danger")

    # Dropdowns: Cantinas e Categorias
    response_c = _api_request("GET", "/canteens")
    canteens = response_c.json() if response_c and response_c.status_code == 200 else []
    
    response_cat = _api_request("GET", "/categories")
    categories = response_cat.json() if response_cat and response_cat.status_code == 200 else []

    return render_template("admin/products/form.html", product=None, canteens=canteens, categories=categories)

@web_bp.route("/products/<uuid:product_id>/edit", methods=["GET", "POST"])
def edit_product(product_id):
    if request.method == "POST":
        data = {
            "code": request.form.get("code"),
            "name": request.form.get("name"),
            "short_name": request.form.get("short_name"),
            "stock": int(request.form.get("stock", 0)),
            "cost_price": float(request.form.get("cost_price", 0.0)),
            "sell_price": float(request.form.get("sell_price", 0.0)),
            "category_id": request.form.get("category_id"),
            "status": request.form.get("status") == "on"
        }
        response = _api_request("PUT", f"/products/{product_id}", data=data)
        if response and response.status_code == 200:
            flash("Produto atualizado com sucesso!", "success")
            return redirect(url_for("web.list_products"))
        else:
            msg = response.json().get("message", "Erro ao atualizar produto") if response else "Erro de conexão"
            flash(msg, "danger")

    response = _api_request("GET", f"/products/{product_id}")
    product = response.json() if response and response.status_code == 200 else None
    
    if not product:
        flash("Produto não encontrado.", "danger")
        return redirect(url_for("web.list_products"))

    response_cat = _api_request("GET", "/categories")
    categories = response_cat.json() if response_cat and response_cat.status_code == 200 else []

    return render_template("admin/products/form.html", product=product, canteens=[{"id": product.get("canteen_id"), "name": "Cantina Atual"}], categories=categories)
