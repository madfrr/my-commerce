from data.repositories.user_repo import UserRepo
from models import CreateUser, CreateUserResponse, UpdateUser, UserDTO, ListUserDTO, FilterParams
from exceptions import UserDoesNotExist

class UserDomain:
    def __init__(self, repo:UserRepo, config):
        self.repo:UserRepo = repo
        self.config = config

    def create(self, user: CreateUser) -> CreateUserResponse:  
        id = self.repo.create_user(user)
        return CreateUserResponse(id=id)
    
    def update(self, user: UpdateUser):
        return self.repo.update_user(user)

    def read(self, filter_query: FilterParams) -> ListUserDTO:
        user_id = filter_query.id
        email = filter_query.email
        users = self.repo.read_user(user_id, email)
        users = [UserDTO(**user) for user in users]
        return ListUserDTO(users=users)
    
    def delete(self, id: str):
        user = self.repo.read_user(id, format_output=True)
        if len(user) == 0:
            raise UserDoesNotExist()
        id = user[0].get("id")
        return self.repo.delete_user(id)