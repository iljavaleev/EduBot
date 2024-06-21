from aiogram import Router

from . import main_handlers
from .article_handler import article_handlers
from .event_handlers import event_handlers
from .question_handlers import questions_handlers

main_router: Router = Router()

main_router.include_routers(
    main_handlers.router,
    questions_handlers.router,
    event_handlers.event_router,
    article_handlers.router
)
