from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.authentication import AuthenticationBackend, AuthCredentials, SimpleUser
from fastapi import HTTPException
from config import AppConfig


class BasicAuthBackend(AuthenticationBackend):
    def __init__(self):
        self.free_paths = [
            f'{AppConfig.app_prefix}/health-check'
        ]

    async def authenticate(self, conn):
        if conn.url.path in self.free_paths:
            return
        
        if "Authorization" not in conn.headers:
            raise HTTPException(status_code=400, detail="Authorization header required.")
        if "email" not in conn.headers:
            raise HTTPException(status_code=400, detail="Email required.")
        
        auth = conn.headers.get("Authorization")
        email = conn.headers.get("email")
        
        if auth is not None:
            auth = auth.strip('Bearer ')

        if auth != AppConfig.auth_token:
            raise HTTPException(status_code=401, detail="token header invalid!")
        user = SimpleUser(email)
        user.email = email
        return AuthCredentials(["authenticated"]), user

def auth(app):
    app.add_middleware(AuthenticationMiddleware, backend=BasicAuthBackend())
