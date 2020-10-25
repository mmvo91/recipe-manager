from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from api.utils.mixins import Audit
from . import models, schemas


def get_units(db: Session):
    return db.query(models.Unit).all()


def get_states(db: Session):
    return db.query(models.State).all()


def get_recipes(db: Session):
    return db.query(models.Recipe).all()


def _find_or_create_object(data, model, parameter, db: Session):
    try:
        db_object: Audit = db.query(model).filter_by(name=data[parameter]).one()
    except NoResultFound:
        db_object = model(name=data[parameter])

        db.add(db_object)
        db.commit()
        db.refresh(db_object)

    return db_object


def _create_recipe_ingredient(ingredient: dict, db: Session):
    db_ingredient: models.Ingredient = _find_or_create_object(ingredient, models.Ingredient, 'ingredient', db)
    unit: models.Unit = _find_or_create_object(ingredient, models.Unit, 'unit', db)
    state: models.State = _find_or_create_object(ingredient, models.State, 'state', db)

    recipe_ingredient = models.RecipeIngredient(
        ingredient_id=db_ingredient.id,
        amount=ingredient['amount'],
        unit_id=unit.id,
        state_id=state.id
    )

    return recipe_ingredient


def create_recipe(recipe: schemas.RecipeCreate, db: Session):
    recipe_dict = recipe.dict()
    ingredients = recipe_dict.pop('ingredients')
    instructions = recipe_dict.pop('instructions')

    created_ingredients = [_create_recipe_ingredient(ingredient, db) for ingredient in ingredients]
    created_instructions = [models.Instruction(**instruction) for instruction in instructions]
    created_recipe = models.Recipe(**recipe_dict)
    created_recipe.ingredients = created_ingredients
    created_recipe.instructions = created_instructions

    db.add(created_recipe)

    db.commit()
    db.refresh(created_recipe)

    return created_recipe


def get_recipe_by_id(recipe_id: int, db: Session):
    return db.query(models.Recipe).get(recipe_id)
