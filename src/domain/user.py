from models import UserDTO, CreateUserResponse
from data.repository import Repo


class UserDomain:
    def __init__(self, repo:Repo, config):
        self.repo:Repo = repo
        self.config = config

    def create_user(self, user: UserDTO):  
        id = self.repo.create_user(user)
        return CreateUserResponse(id=id)
    
    def update_user_name(self):
        pass

    def read_user(self):
        pass

    def list_user(self):
        pass

    def delete_user(self):
        pass