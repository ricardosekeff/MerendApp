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

    @classmethod
    def query_scoped(cls):
        """
        Retorna uma query já filtrada pelo canteen_id se aplicável.
        Útil para o Middleware de Tenant da Sprint 2.
        """
        from flask import g
        query = cls.query
        
        # Filtra se houver canteen_id no contexto de g e não for ADMIN_MASTER
        if hasattr(g, 'canteen_id') and g.canteen_id and getattr(g, 'user_role', None) != 'ADMIN_MASTER':
            # Verifica se o modelo tem o campo canteen_id
            if hasattr(cls, 'canteen_id'):
                return query.filter_by(canteen_id=g.canteen_id)
        
        return query

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"
