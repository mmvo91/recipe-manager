import sqlalchemy as sql
import sqlalchemy.orm
import sqlalchemy.ext.associationproxy

from api.utils.mixins import Audit

recipe_tag = sql.Table(
    "recipe_tag",
    Audit.metadata,
    sql.Column("recipe_id", sql.Integer, sql.ForeignKey("recipes.id"), nullable=False),
    sql.Column(
        "recipe_tag_id", sql.Integer, sql.ForeignKey("recipe_tags.id"), nullable=False
    ),
    sql.PrimaryKeyConstraint("recipe_id", "recipe_tag_id"),
)

recipe_ingredient = sql.Table(
    "recipe_ingredient",
    Audit.metadata,
    sql.Column("recipe_id", sql.Integer, sql.ForeignKey("recipes.id")),
    sql.Column(
        "recipe_ingredient_id", sql.Integer, sql.ForeignKey("recipe_ingredients.id")
    ),
)


class Recipe(Audit):
    __tablename__ = "recipes"

    title = sql.Column(sql.String)
    description = sql.Column(sql.Text)
    image = sql.Column(sql.String)
    author = sql.Column(sql.String)
    source = sql.Column(sql.String, unique=True)

    servings = sql.Column(sql.Integer)

    ingredients = sql.orm.relationship("RecipeIngredient", secondary=recipe_ingredient)
    instructions = sql.orm.relationship("Instruction")

    tags = sql.orm.relationship("RecipeTags", secondary=recipe_tag)


class RecipeTags(Audit):
    __tablename__ = "recipe_tags"

    name = sql.Column(sql.String, unique=True, nullable=False)
    description = sql.Column(sql.Text)


class RecipeIngredient(Audit):
    __tablename__ = "recipe_ingredients"

    ingredient_id = sql.Column(sql.Integer, sql.ForeignKey("ingredients.id"))
    amount = sql.Column(sql.Float)
    unit_id = sql.Column(sql.Integer, sql.ForeignKey("units.id"))
    state_id = sql.Column(sql.Integer, sql.ForeignKey("states.id"))

    _ingredient = sql.orm.relationship("Ingredient")
    _unit = sql.orm.relationship("Unit")
    _state = sql.orm.relationship("State")

    ingredient = sql.ext.associationproxy.association_proxy("_ingredient", "name")
    unit = sql.ext.associationproxy.association_proxy("_unit", "name")
    state = sql.ext.associationproxy.association_proxy("_state", "name")


class Ingredient(Audit):
    __tablename__ = "ingredients"

    name = sql.Column(sql.String, unique=True)


class Unit(Audit):
    __tablename__ = "units"

    name = sql.Column(sql.String, unique=True)


class State(Audit):
    __tablename__ = "states"

    name = sql.Column(sql.String, unique=True)


class Instruction(Audit):
    __tablename__ = "instructions"

    recipe_id = sql.Column(sql.Integer, sql.ForeignKey("recipes.id"))
    step = sql.Column(sql.Integer)
    instruction = sql.Column(sql.Text)
