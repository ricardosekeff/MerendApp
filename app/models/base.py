import uuid
from datetime import datetime, timezone
from sqlalchemy import UUID, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from app.extensions import db

class Base(DeclarativeBase):
    """Classe base para o SQLAlchemy DeclarativeBase."""
    pass

class BaseModel(db.Model):
    """
    BaseModel abstrato para todas as entidades do sistema.
    Provê ID via UUID, e timestamps de criação/atualização.
    """
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc)
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self):
        """Conversão básica para dicionário (debug/logs)."""
        return {
            c.name: getattr(self, c.name) 
            for c in self.__table__.columns
        }
