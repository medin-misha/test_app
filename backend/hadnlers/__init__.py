__all__ = "spending_router", "users_router"

from .spending.views import router as spending_router
from .user.views import router as users_router
