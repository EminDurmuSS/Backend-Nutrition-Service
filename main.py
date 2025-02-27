# main.py
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from routers import mapping_routes, nutrition_routes

def main() -> FastAPI:
    app = FastAPI()

    # Set up CORS to allow your Flutter web app's domain
    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include the mapping and nutrition routers.
    app.include_router(mapping_routes.router)
    app.include_router(nutrition_routes.router)
    return app

if __name__ == "__main__":
    uvicorn.run("app.main:main", host="0.0.0.0", port=5000, reload=True)
