from fastapi.middleware.cors import CORSMiddleware


def setup_cors(app):
    """
    Configura CORS para a aplicação.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",  # React dev
            "http://localhost:8080",  # Vue dev
            "http://localhost:5173",  # Vite dev
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"]
    )
