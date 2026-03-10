import uuid
from flask_login import UserMixin
from sqlalchemy import String, Boolean, Enum, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.base import BaseModel
from app.extensions import db
import enum

class User(BaseModel, UserMixin):
    """
    Representa um Usuário do sistema.
    As roles definem o nível de acesso (RBAC).
    Usuários (exceto ADMIN_MASTER) são vinculados a uma Cantina específica.
    """
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False, default="VENDEDOR")
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Chave Estrangeira para Cantina (opcional para Master Admins)
    canteen_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("canteens.id", ondelete="SET NULL"), 
        nullable=True
    )

    # Relacionamentos
    canteen: Mapped["Canteen"] = relationship("Canteen", back_populates="users")
    wallet = relationship("Wallet", back_populates="user", uselist=False, cascade="all, delete-orphan")

    def set_password(self, password):
        """Gera o hash da senha."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica se a senha coincide com o hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.email} [{self.role}]>"
