from typing import List, Optional

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from api.utils.db import get_db
from . import schemas, services

imports_router = APIRouter()


@imports_router.get("/", response_model=List[schemas.RecipeImport])
def get_recipe_imports(
    imported: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    return services.get_imported_recipes(db, imported=imported)


@imports_router.post(
    "/",
    response_model=schemas.SingleRecipeImport
)
def create_recipe_import(
    url: schemas.URL,
    db: Session = Depends(get_db),
):
    return services.create_recipe_by_import(url.url, db)


@imports_router.get("/{imported_id}", response_model=schemas.SingleRecipeImport)
def get_recipe_import(
    imported_id: int,
    db: Session = Depends(get_db),
):
    return services.get_imported_recipe(imported_id, db)


@imports_router.put("/{imported_id}", response_model=schemas.SingleRecipeImport)
def update_recipe_import(
    imported_id: int,
    db: Session = Depends(get_db),
):
    return services.update_imported_recipe(imported_id, db)
