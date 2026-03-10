from app import create_app
from app.extensions import db
from app.models.category import Category
from app.models.canteen import Canteen

app = create_app('development')

with app.app_context():
    canteen = Canteen.query.first()
    if not canteen:
        print("Erro: Nenhuma cantina encontrada.")
        exit(1)
    
    category = Category(
        code="BEB",
        name="Bebidas",
        short_name="Beb",
        safety_stock=10,
        status=True,
        canteen_id=canteen.id
    )
    db.session.add(category)
    db.session.commit()
    print(f"Categoria 'Bebidas' criada com sucesso! ID: {category.id}")
