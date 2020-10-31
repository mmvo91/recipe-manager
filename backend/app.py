from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.features.recipes.routes import recipes_router
from api.features.imports.routes import imports_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recipes_router, prefix="/api/recipes")
app.include_router(imports_router, prefix="/api/imports")
