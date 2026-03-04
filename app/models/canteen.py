import uuid
from sqlalchemy import String, Boolean, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel

class Canteen(BaseModel):
    """
    Representa uma Cantina específica (Tenant).
    Toda a isolação lógica do sistema é baseada no canteen_id.
    """
    __tablename__ = "canteens"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Chave Estrangeira para Escola
    school_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("schools.id", ondelete="CASCADE"), 
        nullable=False
    )

    # Relacionamentos
    school: Mapped["School"] = relationship("School", back_populates="canteens")
    users: Mapped[list["User"]] = relationship(
        "User", 
        back_populates="canteen",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Canteen {self.name} (School ID: {self.school_id})>"
