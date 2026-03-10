from app import create_app
from app.extensions import db
from app.models.product import Product
from app.models.combo import Combo, ComboItem
from app.models.canteen import Canteen

app = create_app('development')

with app.app_context():
    canteen = Canteen.query.first()
    product = Product.query.first()
    
    if not canteen or not product:
        print("Required seed data missing")
        exit(1)
        
    combo = Combo(
        code="CMB-TEST",
        name="Combo Teste Script",
        price_type="auto_sum",
        status=True,
        canteen_id=canteen.id
    )
    
    combo_item = ComboItem(product_id=product.id, quantity=2)
    combo.items.append(combo_item)
    
    db.session.add(combo)
    db.session.commit()
    print(f"Combo created with ID: {combo.id} and {len(combo.items)} items.")
