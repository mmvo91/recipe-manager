import datetime
from typing import List, Optional

from sqlalchemy.sql.sqltypes import JSON

from api.features.recipes.schemas import Recipe
from api.utils.schema import JSONModel


class UserWeekRecipeCreate(JSONModel):
    recipe_id: int
    servings: int
    order: int


class UserWeekRecipe(UserWeekRecipeCreate):
    id: int
    user_week_id: int

    recipe: Optional[Recipe]

    class Config:
        orm_mode = True


class UserWeek(JSONModel):
    id: int
    user_id: int
    date: datetime.date

    class Config:
        orm_mode = True


class SingleUserWeek(UserWeek):
    recipes: List[UserWeekRecipe]

    class Config:
        orm_mode = True
