from flask import Blueprint

web_bp = Blueprint("web", __name__)

from app.web import routes, schools, canteens, categories, products
