import sqlalchemy as sql
import sqlalchemy.orm

from api.utils.mixins import Audit


class RecipeImport(Audit):
    __tablename__ = "recipes_import"

    title = sql.Column(sql.String)
    description = sql.Column(sql.Text)
    image = sql.Column(sql.String)
    author = sql.Column(sql.String)
    source = sql.Column(sql.String, unique=True)
    imported = sql.Column(sql.Boolean, default=False, nullable=False)

    servings = sql.Column(sql.Integer)

    ingredients = sql.orm.relationship(
        "RecipeIngredientImport", order_by="RecipeIngredientImport.id"
    )
    instructions = sql.orm.relationship(
        "RecipeInstructionImport", order_by="RecipeInstructionImport.step"
    )


class RecipeIngredientImport(Audit):
    __tablename__ = "recipe_ingredients_import"

    recipe_id = sql.Column(sql.Integer, sql.ForeignKey("recipes_import.id"))
    ingredient = sql.Column(sql.String)
    amount = sql.Column(sql.Float)
    unit = sql.Column(sql.String)
    state = sql.Column(sql.String)


class RecipeInstructionImport(Audit):
    __tablename__ = "recipe_instructions_import"

    recipe_id = sql.Column(sql.Integer, sql.ForeignKey("recipes_import.id"))
    step = sql.Column(sql.Integer)
    instruction = sql.Column(sql.Text)
