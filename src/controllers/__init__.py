from fastapi import FastAPI  # APIRouter, Depends, HTTPException
from config import AppConfig
from controllers import user, advertising, product, transaction, order


def setup_routes(api: FastAPI, config: AppConfig):
    api.include_router(
        user.router,
        prefix=config.app_prefix,
        tags=["User"]
    )
    api.include_router(
        product.router,
        prefix=config.app_prefix,
        tags=["Product"]
    )
    api.include_router(
        advertising.router,
        prefix=config.app_prefix,
        tags=["Advertising"]
    )
    api.include_router(
        transaction.router,
        prefix=config.app_prefix,
        tags=["Transaction"]
    )
    api.include_router(
        order.router,
        prefix=config.app_prefix,
        tags=["Order"]
    )

    @api.get(f'{config.app_prefix}/health-check', tags=['Health Check'])
    def health_check():
        return {"message": "I'm alive!"}
