from fastapi import FastAPI
from utils.logger import logger
from config import AppConfig
from controllers import setup_routes
from middlewares import setup_middlewares
from lifespan import lifespan


def create_api(config: AppConfig = AppConfig):
    app = FastAPI(
        title=config.application_name,
        debug=config.debug,
        version=config.version,
        docs_url=config.docs_url,
        redoc_url=config.redoc_url,
        lifespan=lifespan
    )

    setup_routes(app, config)
    setup_middlewares(app)
    logger.info(f"[StartAPI]  {config.application_name} - V: {config.version}")

    return app
