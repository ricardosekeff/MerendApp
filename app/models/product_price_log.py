from sqlalchemy import String, Boolean, ForeignKey, Integer, Numeric, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel
import uuid

class ProductPriceLog(BaseModel):
    """
    Log de alterações de preço de um produto.
    Rastreia tanto o preço de custo quanto o preço de venda.
    """
    __tablename__ = "product_price_logs"

    product_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("products.id"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    
    old_cost_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=True)
    new_cost_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    
    old_sell_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=True)
    new_sell_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    # Relacionamentos
    product: Mapped["Product"] = relationship("Product", backref="price_logs")
    user: Mapped["User"] = relationship("User")
