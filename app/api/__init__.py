from flask import Blueprint

api_bp = Blueprint("api", __name__)

from app.api import routes, errors, school_routes, canteen_routes, auth, category_routes, product_routes, combo_routes, wallet_routes
