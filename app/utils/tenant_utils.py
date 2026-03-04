from flask import g
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from functools import wraps

def get_current_tenant_id():
    """Retorna o ID da cantina do contexto atual (flask.g)."""
    return getattr(g, "canteen_id", None)

def resolve_tenant():
    """
    Middleware (hook) para extrair o canteen_id do JWT.
    Deve ser chamado em um before_request.
    """
    try:
        # Verifica se há um JWT válido sem interromper a requisição se não houver
        # (permitindo rotas públicas como login)
        verify_jwt_in_request(optional=True)
        
        claims = get_jwt()
        if claims:
            g.canteen_id = claims.get("canteen_id")
            g.user_role = claims.get("role")
            g.user_id = claims.get("sub")
    except Exception:
        # Se falhar (ex: token inválido), g.canteen_id continua None
        g.canteen_id = None
        g.user_role = None
        g.user_id = None
