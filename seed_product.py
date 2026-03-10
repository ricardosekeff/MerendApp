from app import create_app
from app.extensions import db
from app.models.product import Product
from app.models.category import Category
from app.models.canteen import Canteen

app = create_app('development')

with app.app_context():
    category = Category.query.filter_by(code="BEB").first()
    canteen = Canteen.query.first()
    
    product = Product(
        code="COCA",
        name="Coca-Cola Lata 350ml",
        short_name="Coca Lata",
        stock=50,
        cost_price=3.50,
        sell_price=6.00,
        status=True,
        category_id=category.id,
        canteen_id=canteen.id
    )
    db.session.add(product)
    db.session.commit()
    print(f"Produto 'Coca-Cola' criado! ID: {product.id}")
