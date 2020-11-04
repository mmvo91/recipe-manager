from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.features.imports import models, parsers
from api.features.recipes.schemas import RecipeImport


def get_imported_recipes(db: Session, imported=None):
    filters = {}
    if imported is not None:
        filters['imported'] = imported
    return db.query(models.RecipeImport).filter_by(**filters).all()


def create_recipe_by_import(source: str, db: Session):
    try:
        recipe_import: RecipeImport = parsers.get_parser(source).build_recipe()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")

    recipe_dict = recipe_import.dict()
    ingredients_dict = recipe_dict.pop("ingredients")
    instructions_dict = recipe_dict.pop("instructions")

    created_recipe_import = models.RecipeImport(**recipe_dict)
    created_ingredients_imports = [
        models.RecipeIngredientImport(**ingredient_dict)
        for ingredient_dict in ingredients_dict
    ]
    created_instructions_imports = [
        models.RecipeInstructionImport(**instruction_dict)
        for instruction_dict in instructions_dict
    ]

    created_recipe_import.ingredients = created_ingredients_imports
    created_recipe_import.instructions = created_instructions_imports

    db.add(created_recipe_import)
    db.commit()
    db.refresh(created_recipe_import)

    return created_recipe_import


def get_imported_recipe(import_id: int, db: Session):
    return db.query(models.RecipeImport).get(import_id)


def update_imported_recipe(import_id: int, db: Session):
    recipe_import: models.RecipeImport = get_imported_recipe(import_id, db)

    recipe_import.imported = not recipe_import.imported

    db.commit()
    db.refresh(recipe_import)

    return recipe_import
