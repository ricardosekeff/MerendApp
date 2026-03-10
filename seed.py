from app import create_app
from app.extensions import db
from app.models.school import School
from app.models.canteen import Canteen
from app.models.user import User
from app.models.wallet import Wallet
import uuid

app = create_app('development')

with app.app_context():
    print("Iniciando seed base...")
    
    school = School.query.first()
    if not school:
        school = School(
            name="Escola Primária de Teste",
            cnpj="12345678000199",
            active=True
        )
        db.session.add(school)
        db.session.flush()

    canteen = Canteen.query.first()
    if not canteen:
        canteen = Canteen(
            name="Cantina Central",
            school_id=school.id,
            active=True
        )
        db.session.add(canteen)
        db.session.flush()

    admin = User.query.filter_by(email="admin@merendapp.com.br").first()
    if not admin:
        admin = User(
            id=uuid.uuid4(),
            name="Administrador Master",
            email="admin@merendapp.com.br",
            role="ADMIN_MASTER",
            canteen_id=canteen.id,
            active=True
        )
        admin.set_password("admin123")
        db.session.add(admin)
        print("Admin criado!")

    gestor = User.query.filter_by(email="gestor@merendapp.com.br").first()
    if not gestor:
        gestor = User(
            id=uuid.uuid4(),
            name="Gestor da Cantina Central",
            email="gestor@merendapp.com.br",
            role="GESTOR",
            canteen_id=canteen.id,
            active=True
        )
        gestor.set_password("gestor123")
        db.session.add(gestor)
        print("Gestor criado!")

    finan = User.query.filter_by(email="financeiro@merendapp.com.br").first()
    if not finan:
        finan = User(
            id=uuid.uuid4(),
            name="Financeiro da Cantina Central",
            email="financeiro@merendapp.com.br",
            role="FINANCEIRO",
            canteen_id=canteen.id,
            active=True
        )
        finan.set_password("finan123")
        db.session.add(finan)
        print("Financeiro criado!")

    resp = User.query.filter_by(email="responsavel@merendapp.com.br").first()
    if not resp:
        resp = User(
            id=uuid.uuid4(),
            name="João Responsável",
            email="responsavel@merendapp.com.br",
            role="RESPONSAVEL",
            canteen_id=canteen.id,
            active=True
        )
        resp.set_password("resp123")
        db.session.add(resp)
        print("Responsável criado!")

    aluno = User.query.filter_by(email="aluno@merendapp.com.br").first()
    if not aluno:
        aluno = User(
            id=uuid.uuid4(),
            name="Pedrinho (Aluno)",
            email="aluno@merendapp.com.br",
            role="ALUNO",
            canteen_id=canteen.id,
            parent_id=resp.id,
            active=True
        )
        aluno.set_password("aluno123")
        db.session.add(aluno)
        db.session.flush()
        print("Aluno criado e vinculado ao Responsável!")
        
        # Cria a carteira para o aluno
        wallet = Wallet(user_id=aluno.id, balance=50.00, active=True, student_can_recharge=True)
        db.session.add(wallet)
        print("Carteira do aluno inserida!")

    db.session.commit()
    print("Seed concluído com sucesso!")
