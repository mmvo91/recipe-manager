import datetime
from typing import List

import sqlalchemy as sql
from sqlalchemy.orm import Session
import pandas as pd

from ..recipes import models as recipe_models
from . import models, schemas


def get_planner_weeks_by_user_id(user_id: int, db: Session):
    return db.query(models.UserWeek).filter_by(user_id=user_id).all()


def get_planner_week_by_user_and_date(user_id: int, date: datetime.date, db: Session):
    try:
        user_week = (
            db.query(models.UserWeek).filter_by(user_id=user_id, date=date).one()
        )
    except sql.orm.exc.NoResultFound:
        user_week = create_planner_week_by_user_and_date(
            user_id=user_id, date=date, db=db
        )

    return user_week


def add_recipe_to_planner_week(
    user_id: int,
    date: datetime.date,
    user_week_recipes: List[schemas.UserWeekRecipeCreate],
    db: Session,
):
    user_week: models.UserWeek = get_planner_week_by_user_and_date(
        user_id=user_id, date=date, db=db
    )

    for user_week_recipe in user_week_recipes:
        try:
            user_week_recipe_orm: models.UserWeekRecipe = (
                db.query(models.UserWeekRecipe)
                .filter_by(user_week_id=user_week.id, order=user_week_recipe.order)
                .one()
            )

            user_week_recipe_orm.recipe_id = user_week_recipe.recipe_id
            user_week_recipe_orm.servings = user_week_recipe.servings

        except sql.orm.exc.NoResultFound:
            user_week_recipe_orm = models.UserWeekRecipe(**user_week_recipe.dict())

            user_week.recipes.append(user_week_recipe_orm)

    db.commit()
    db.refresh(user_week)

    return user_week


def delete_user_week_recipe(
    user_recipe_id: int,
    db: Session,
):
    user_week_recipe = db.query(models.UserWeekRecipe).get(user_recipe_id)

    db.delete(user_week_recipe)
    db.commit()


def create_planner_week_by_user_and_date(
    user_id: int, date: datetime.date, db: Session
):
    user_week = models.UserWeek(user_id=user_id, date=date)

    db.add(user_week)
    db.commit()
    db.refresh(user_week)

    return user_week


def get_planner_summary_by_user_and_date(
    user_id: int, date: datetime.date, db: Session
):
    query = (
        db.query(
            sql.func.count(models.UserWeek.user_id).label("instances"),
            sql.func.sum(recipe_models.RecipeIngredient.amount).label("amount"),
            recipe_models.Ingredient.name.label("ingredients"),
            recipe_models.Unit.name.label("units"),
            sql.func.sum(models.UserWeekRecipe.servings).label("servings"),
        )
        .filter(
            models.UserWeek.user_id == user_id,
            sql.func.date_part("week", models.UserWeek.date)
            == sql.func.date_part("week", date),
        )
        .join(
            models.UserWeekRecipe,
            recipe_models.Recipe,
            recipe_models.recipe_ingredient,
            recipe_models.RecipeIngredient,
            recipe_models.Ingredient,
            recipe_models.Unit,
            recipe_models.State,
        )
        .group_by(
            models.UserWeek.user_id,
            recipe_models.Ingredient.name,
            recipe_models.Unit.name,
        )
        .all()
    )

    x = pd.DataFrame(query)

    return list(x.T.to_dict().values())
