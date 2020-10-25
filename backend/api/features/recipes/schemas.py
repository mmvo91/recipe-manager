from typing import List, Optional

from api.utils.schema import JSONModel


class TagCreate(JSONModel):
    name: str
    description: str


class Tag(TagCreate):
    id: int

    class Config:
        orm_mode = True


class InstructionCreate(JSONModel):
    step: int
    instruction: str


class Instruction(InstructionCreate):
    id: int

    class Config:
        orm_mode = True


class IngredientCreate(JSONModel):
    name: str


class Ingredient(IngredientCreate):
    id: int

    class Config:
        orm_mode = True


class UnitCreate(JSONModel):
    name: str


class Unit(UnitCreate):
    id: int

    class Config:
        orm_mode = True


class StateCreate(JSONModel):
    name: str


class State(StateCreate):
    id: int

    class Config:
        orm_mode = True


class RecipeIngredient(JSONModel):
    ingredient: str
    amount: float
    unit: str
    state: str

    class Config:
        orm_mode = True


class RecipeBase(JSONModel):
    title: Optional[str]
    description: Optional[str]
    image: Optional[str]
    author: Optional[str]
    source: Optional[str]
    servings: Optional[int]


class RecipeCreate(RecipeBase):
    ingredients: List[RecipeIngredient]
    instructions: List[InstructionCreate]


class Recipe(RecipeBase):
    id: int

    class Config:
        orm_mode = True


class SingleRecipe(Recipe):
    ingredients: List[RecipeIngredient]
    instructions: List[Instruction]

    tags: Optional[List[Tag]]

    class Config:
        orm_mode = True


class RecipeImport(RecipeBase):
    ingredients: List[RecipeIngredient]
    instructions: List[InstructionCreate]

    tags: Optional[List[Tag]]

    class Config:
        orm_mode = True
