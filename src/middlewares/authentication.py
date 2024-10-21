from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.authentication import AuthenticationBackend, AuthCredentials, SimpleUser
from fastapi import HTTPException
from config import AppConfig


class BasicAuthBackend(AuthenticationBackend):
    def free_paths(self, path):
        paths = [f"{AppConfig.app_prefix}/health-check", f"{AppConfig.app_prefix}/docs", "/openapi.json"]
        for free_path in paths:
            if free_path in path:
                return True

        return False

    async def authenticate(self, conn):
        if self.free_paths(conn.url.path):
            return

        if "Authorization" not in conn.headers:
            raise HTTPException(status_code=400, detail="Authorization header required.")

        auth = conn.headers.get("Authorization")

        if auth is not None:
            auth = auth.removeprefix("Bearer ")

        if auth != AppConfig.auth_token:
            raise HTTPException(status_code=401, detail="token header invalid!")

        return AuthCredentials(["authenticated"]), SimpleUser("username")


def auth(app):
    app.add_middleware(AuthenticationMiddleware, backend=BasicAuthBackend())
