from sqlalchemy import String, Boolean, ForeignKey, Integer, Numeric, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel
import uuid

class Combo(BaseModel):
    """
    Representa um Combo que agrupa vários Produtos.
    """
    __tablename__ = "combos"

    code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    short_name: Mapped[str] = mapped_column(String(100), nullable=True)
    
    # Preço calculado dinamicamente ou fixado pelo gerente
    price_type: Mapped[str] = mapped_column(String(20), default="auto_sum") # auto_sum or custom
    custom_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=True)
    
    image_url: Mapped[str] = mapped_column(String(255), nullable=True)
    status: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relacionamentos
    canteen_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("canteens.id"), nullable=False)
    canteen: Mapped["Canteen"] = relationship("Canteen", backref="combos")
    
    items: Mapped[list["ComboItem"]] = relationship("ComboItem", back_populates="combo", cascade="all, delete-orphan")

    def calculate_total_price(self):
        if self.price_type == "custom" and self.custom_price is not None:
            return self.custom_price
        
        total = 0
        for item in self.items:
            if item.product and item.product.sell_price:
                total += float(item.product.sell_price) * item.quantity
        return total

class ComboItem(BaseModel):
    """
    Associação de N para N entre Combo e Product com quantidade.
    """
    __tablename__ = "combo_items"
    
    combo_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("combos.id"), nullable=False)
    product_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    combo: Mapped["Combo"] = relationship("Combo", back_populates="items")
    product: Mapped["Product"] = relationship("Product")
