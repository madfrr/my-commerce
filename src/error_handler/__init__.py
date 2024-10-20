from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from exceptions import BusinessException
from utils.logger import logger


async def handle_business_exception(request: Request, exception: Exception):
    return JSONResponse(
        status_code=exception.status_code,
        content={"error": type(exception).__name__, "message": exception.message},
    )


async def handle_value_error(request: Request, exception: Exception):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": type(exception).__name__, "message": str(exception)},
    )


def find_error_name(error):
    return str(type(error)).replace("'>", "").split(".")[-1]


async def handle_validation_error(request: Request, exception: Exception):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": find_error_name(exception), "message": exception.errors()},
    )


async def handle_fastapi_http_exception(request: Request, exception: Exception):
    return JSONResponse(
        status_code=exception.status_code,
        content={"error": type(exception).__name__, "message": exception.detail},
    )


async def handle_unexpected_error(request: Request, exception: Exception):
    logger.error(
        f"UnexpectedException | An exception of type {type(exception).__name__} occurred. Details: {str(exception)}"
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "UnexpectedException",
            "message": "An unexpected error has occurred.",
        },
    )


def setup_error_handler(app: FastAPI):
    app.add_exception_handler(BusinessException, handle_business_exception)
    app.add_exception_handler(RequestValidationError, handle_validation_error)
    app.add_exception_handler(ValueError, handle_value_error)
    app.add_exception_handler(HTTPException, handle_fastapi_http_exception)
    app.add_exception_handler(StarletteHTTPException, handle_fastapi_http_exception)
    app.add_exception_handler(Exception, handle_unexpected_error)
