import uvicorn
from build import create_api
from config import AppConfig

api = create_api()

if __name__ == "__main__":
    AppConfig.port
    uvicorn.run(api, host="0.0.0.0", port=AppConfig.port) 