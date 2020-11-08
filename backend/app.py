from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.features.recipes.routes import recipes_router
from api.features.imports.routes import imports_router
from api.features.users.routes import users_router


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
app.include_router(users_router, prefix="/api/users")
