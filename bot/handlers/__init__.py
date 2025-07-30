from bot.handlers.start import router as start_router
from bot.handlers.admin import router as admin_router
from bot.handlers.handler import router as user_router

all_routers = [
    start_router,
    admin_router,
    user_router,
]
