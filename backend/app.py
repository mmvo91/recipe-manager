from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.features.recipes.routes import recipes_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recipes_router, prefix="/recipes")
