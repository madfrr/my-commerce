from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.authentication import AuthenticationBackend, AuthCredentials, SimpleUser
from fastapi import HTTPException
from config import AppConfig



class BasicAuthBackend(AuthenticationBackend):
    def __init__(self):
        self.free_paths = [
            f'{AppConfig.app_prefix}/health-check'
        ]
        

    def _endpoint_requires_email_header(self, url_path, url_method):
        is_create_user_endpoint = (url_path == f'{AppConfig.app_prefix}/user' and url_method == 'POST')
        require_email_header = not is_create_user_endpoint
        return require_email_header

    async def authenticate(self, conn):
        if conn.url.path in self.free_paths:
            return
        
        if "Authorization" not in conn.headers:
            raise HTTPException(status_code=400, detail="Authorization header required.")
        if self._endpoint_requires_email_header(
                url_path = conn.url.path, 
                url_method = conn.scope['method']
            ) and "email" not in conn.headers:
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
