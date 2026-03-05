import uuid
from sqlalchemy import String, Boolean, ForeignKey, Integer, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel

class Category(BaseModel):
    """
    Representa uma Categoria de Produtos do Cardápio de uma Cantina.
    """
    __tablename__ = "categories"

    # Código único (idealmente único por cantina, gerenciado via UniqueConstraint ou validação na lógica de negócios)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    short_name: Mapped[str] = mapped_column(String(50), nullable=False)
    safety_stock: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Chave estrangeira para a Cantina (Tenant)
    canteen_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("canteens.id", ondelete="CASCADE"), 
        nullable=False
    )

    # Relacionamentos
    canteen: Mapped["Canteen"] = relationship("Canteen", backref="categories")

    def __repr__(self):
        return f"<Category {self.code} - {self.name} (Canteen ID: {self.canteen_id})>"
