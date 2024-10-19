from pydantic import BaseModel


class CreateUserResponse(BaseModel):
    id: str

class UserDTO(BaseModel):
    name: str
    email: str

# CREATE TABLE "user" (
# 	id UUID primary key DEFAULT (uuid_generate_v4()) NOT null,
# 	name text NOT NULL,
# 	email text NOT NULL
# );