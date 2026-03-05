from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel

class School(BaseModel):
    """
    Representa uma Instituição de Ensino (Tenant Group).
    Uma Escola pode ter múltiplas Cantinas (Canteens).
    """
    __tablename__ = "schools"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    cnpj: Mapped[str] = mapped_column(String(18), unique=True, nullable=False, index=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    address: Mapped[str] = mapped_column(String(500), nullable=True)
    city: Mapped[str] = mapped_column(String(100), nullable=True)
    state: Mapped[str] = mapped_column(String(2), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relacionamentos
    canteens: Mapped[list["Canteen"]] = relationship(
        "Canteen", 
        back_populates="school",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<School {self.name} ({self.cnpj})>"
