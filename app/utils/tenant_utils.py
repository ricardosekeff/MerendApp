from flask import g, request
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from flask_login import current_user
from functools import wraps

def get_current_tenant_id():
    """Retorna o ID da cantina do contexto atual (flask.g)."""
    return getattr(g, "canteen_id", None)

def roles_required(*roles):
    """
    Decorator para restringir acesso a determinadas roles.
    Suporta JWT (API) e Sessão (Web).
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_role = None
            
            # 1. Tenta via JWT (API)
            try:
                verify_jwt_in_request(optional=True)
                claims = get_jwt()
                if claims:
                    user_role = claims.get("role")
            except Exception:
                pass
            
            # 2. Tenta via Session (Web) se não achou no JWT
            if not user_role and current_user.is_authenticated:
                user_role = current_user.role
            
            if user_role not in roles:
                if request.path.startswith("/api/"):
                    return {"error": "Acesso negado", "message": f"Requer roles: {roles}"}, 403
                # Web redirect ou erro
                from flask import abort
                abort(403)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def resolve_tenant():
    """
    Middleware (hook) para extrair o canteen_id do contexto (JWT ou Session).
    """
    g.canteen_id = None
    g.user_role = None
    g.user_id = None

    # 1. Tenta via JWT
    try:
        verify_jwt_in_request(optional=True)
        claims = get_jwt()
        if claims:
            g.canteen_id = claims.get("canteen_id")
            g.user_role = claims.get("role")
            g.user_id = claims.get("sub")
            return
    except Exception:
        pass

    # 2. Tenta via Session (Web)
    if current_user.is_authenticated:
        g.canteen_id = str(current_user.canteen_id) if current_user.canteen_id else None
        g.user_role = current_user.role
        g.user_id = str(current_user.id)
