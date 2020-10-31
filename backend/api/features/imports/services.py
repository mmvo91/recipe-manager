from sqlalchemy.orm import Session

from api.features.imports import models


def get_imported_recipes(db: Session, imported=None):
    filters = {}
    if imported is not None:
        filters['imported'] = imported
    return db.query(models.RecipeImport).filter_by(**filters).all()


def get_imported_recipe(import_id: int, db: Session):
    return db.query(models.RecipeImport).get(import_id)


def update_imported_recipe(import_id: int, db: Session):
    recipe_import: models.RecipeImport = get_imported_recipe(import_id, db)

    recipe_import.imported = not recipe_import.imported

    db.commit()
    db.refresh(recipe_import)

    return recipe_import
