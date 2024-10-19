from fastapi import APIRouter, Depends, Response, Request, HTTPException
from config import AppConfig
from models.user import CreateUserResponse, UserDTO
from domain.user import UserDomain
from data.repository import Repo
router = APIRouter()

@router.get('/user', response_model=None)
def read_user(request: Request, response: Response, config: AppConfig = Depends(AppConfig)):
    pass

@router.post('/user', response_model=CreateUserResponse, status_code=201)
def create_user(request: Request, payload: UserDTO, response: Response, config: AppConfig = Depends(AppConfig)):    
    repo = Repo(db=request.app.state.db)
    
    user = UserDomain(
        repo=repo, config=config).create_user(payload)
    if user is None:
        raise HTTPException(status_code=500)
    response.status_code = 201

    return user

# @router.post('', response_model=PolygonDto, status_code=201, dependencies=[Depends(need_credentials)])
# def create_service_zone(request: Request, payload: CreateServiceZoneInput = Body(
#     title='Banan',
#     alias='Bananinha nanica',
#     description='ablublebleide',
#     openapi_examples = service_zone_docs['create_service_zone']['input_examples'],
# ), config: AppConfig = Depends(AppConfig), dependencies=[Depends(need_credentials)]):
#     user = request.state.user['email'] if hasattr(
#         request.state, 'user') else None
#     uow = request.app.state.uow
#     with uow.connection() as conn:
#         repo = CartographicRepository(db=conn.cursor())
#         sz = CartographicMap(
#             repo=repo, config=config).create_service_zone(payload, user)

#     return sz


@router.patch('/user', response_model=None)
def update_user(request: Request, response: Response, config: AppConfig = Depends(AppConfig)):
    pass

@router.delete('/user', response_model=None)
def delete_user(request: Request, response: Response, config: AppConfig = Depends(AppConfig)):
    pass
