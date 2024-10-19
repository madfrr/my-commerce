from fastapi.middleware.cors import CORSMiddleware

def CORS(app):
    origins = [ #passar para variavel de ambiente
        "http://localhost",
        "http://localhost:8080",
        "http://localhost:5000",
        "http://localhost:3000"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )