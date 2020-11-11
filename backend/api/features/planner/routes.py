import datetime
from typing import List

from fastapi import Depends, APIRouter, Request
from sqlalchemy.orm import Session

from api.utils.security import get_current_active_user
from api.utils.db import get_db
from api.features.users.schemas import User
from . import schemas, services

planner_router = APIRouter()


@planner_router.get(
    "/weeks",
    response_model=List[schemas.UserWeek]
)
def get_weeks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return services.get_planner_weeks_by_user_id(current_user.id, db)


@planner_router.get("/weeks/{date}", response_model=schemas.SingleUserWeek)
def get_week(
    date: datetime.date,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return services.get_planner_week_by_user_and_date(current_user.id, date, db)


@planner_router.put("/weeks/{date}", response_model=schemas.SingleUserWeek)
def change_week(
    date: datetime.date,
    user_week_recipes: List[schemas.UserWeekRecipeCreate],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return services.add_recipe_to_planner_week(current_user.id, date, user_week_recipes, db=db)


@planner_router.delete("/recipes/{user_recipe_id}")
def delete_user_week_recipe(
    user_recipe_id: int,
    db: Session = Depends(get_db),
):
    return services.delete_user_week_recipe(user_recipe_id, db=db)


@planner_router.get("/weeks/{date}/summary")
def get_week_summary(
    date: datetime.date,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return services.get_planner_summary_by_user_and_date(current_user.id, date, db)
