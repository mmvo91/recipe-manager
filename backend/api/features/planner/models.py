import sqlalchemy as sql
import sqlalchemy.orm

from api.utils.mixins import Base


class UserWeek(Base):
    __tablename__ = "user_week"

    id = sql.Column(sql.Integer, primary_key=True)
    user_id = sql.Column(sql.Integer, sql.ForeignKey("users.id"))
    date = sql.Column(sql.Date)

    user = sql.orm.relationship("User")
    recipes = sql.orm.relationship("UserWeekRecipe")


class UserWeekRecipe(Base):
    __tablename__ = "user_week_recipe"

    id = sql.Column(sql.Integer, primary_key=True)
    user_week_id = sql.Column(sql.Integer, sql.ForeignKey("user_week.id"))
    recipe_id = sql.Column(sql.Integer, sql.ForeignKey("recipes.id"))
    servings = sql.Column(sql.Integer)
    order = sql.Column(sql.Integer)

    recipe = sql.orm.relationship("Recipe")
