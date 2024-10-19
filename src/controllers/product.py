from fastapi import APIRouter, Depends, Response, Request
from config import AppConfig


router = APIRouter()

@router.get('/user', response_model=None)
def get_user(request: Request, response: Response, config: AppConfig = Depends(AppConfig)):
    pass