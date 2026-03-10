from app import create_app
from app.extensions import db
from app.models.school import School
from app.models.canteen import Canteen
from app.models.user import User

app = create_app('development')

with app.app_context():
    # 1. Criar Escola
    school = School(
        name="Escola Primária de Teste",
        cnpj="12345678000199",
        active=True
    )
    db.session.add(school)
    db.session.flush()

    # 2. Criar Cantina
    canteen = Canteen(
        name="Cantina Central",
        school_id=school.id,
        active=True
    )
    db.session.add(canteen)
    db.session.flush()

    # 3. Atualizar Admin Master
    admin = User.query.filter_by(email="admin@merendapp.com.br").first()
    if admin:
        admin.canteen_id = canteen.id
        db.session.add(admin)
    
    db.session.commit()
    print(f"Seed concluído! Escola: {school.id}, Cantina: {canteen.id}")
