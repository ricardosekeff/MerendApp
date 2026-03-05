import uuid
from sqlalchemy import Boolean, Numeric, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel

class Wallet(BaseModel):
    """
    Representa a Carteira Digital de um usuário (ex: Aluno).
    """
    __tablename__ = "wallets"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    balance: Mapped[float] = mapped_column(Numeric(10, 2), default=0.00, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    user = relationship("User", back_populates="wallet")
    limits = relationship("WalletLimit", back_populates="wallet", cascade="all, delete-orphan")
    category_restrictions = relationship("WalletCategoryRestriction", backref="wallet", cascade="all, delete-orphan")
    product_restrictions = relationship("WalletProductRestriction", backref="wallet", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Wallet {self.id} User:{self.user_id} Balance:{self.balance}>"


class WalletLimit(BaseModel):
    """
    Representa o limite de gasto de uma carteira para um período específico.
    """
    __tablename__ = "wallet_limits"

    wallet_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("wallets.id"), nullable=False)
    period_type: Mapped[str] = mapped_column(String(50), nullable=False)  # daily, weekly, monthly
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    wallet = relationship("Wallet", back_populates="limits")

    def __repr__(self):
        return f"<WalletLimit {self.id} Wallet:{self.wallet_id} {self.period_type}:{self.amount}>"


class WalletCategoryRestriction(BaseModel):
    """
    Lista de categorias bloqueadas para consumo por esta carteira.
    """
    __tablename__ = "wallet_category_restrictions"

    wallet_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("wallets.id"), nullable=False)
    category_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("categories.id"), nullable=False)


class WalletProductRestriction(BaseModel):
    """
    Lista de produtos avulsos bloqueados para consumo por esta carteira.
    """
    __tablename__ = "wallet_product_restrictions"

    wallet_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("wallets.id"), nullable=False)
    product_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("products.id"), nullable=False)

