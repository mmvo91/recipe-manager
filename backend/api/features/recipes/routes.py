from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from api.utils.db import get_db
from . import schemas, services

recipes_router = APIRouter()


@recipes_router.get(
    "/units",
    response_model=List[schemas.Unit],
)
def get_units(
    db: Session = Depends(get_db),
):
    return services.get_units(db)


@recipes_router.get(
    "/states",
    response_model=List[schemas.State],
)
def get_states(
    db: Session = Depends(get_db),
):
    return services.get_states(db)


@recipes_router.get(
    "/",
    response_model=List[schemas.Recipe],
)
def get_recipes(
    db: Session = Depends(get_db),
):
    return services.get_recipes(db)


@recipes_router.post("/", response_model=schemas.Recipe)
def create_recipe(
    recipe: schemas.RecipeCreate,
    db: Session = Depends(get_db),
):
    return services.create_recipe(recipe, db)


@recipes_router.get(
    "/{recipe_id}",
    response_model=schemas.SingleRecipe,
)
def get_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
):
    return services.get_recipe_by_id(recipe_id, db)
