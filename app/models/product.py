import uuid
from sqlalchemy import String, Boolean, ForeignKey, Integer, Numeric, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel

class Product(BaseModel):
    """
    Representa um Produto à Venda no Cardápio da Cantina.
    """
    __tablename__ = "products"

    code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    short_name: Mapped[str] = mapped_column(String(50), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    cost_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    sell_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Chave estrangeira para Categoria
    category_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("categories.id", ondelete="RESTRICT"), 
        nullable=False
    )

    # Chave estrangeira para Cantina
    canteen_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("canteens.id", ondelete="CASCADE"), 
        nullable=False
    )

    # Relacionamentos
    category: Mapped["Category"] = relationship("Category", backref="products")
    canteen: Mapped["Canteen"] = relationship("Canteen", backref="products")

    def __repr__(self):
        return f"<Product {self.code} - {self.name} (R$ {self.sell_price})>"
