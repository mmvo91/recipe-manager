from typing import List

from api.utils.schema import JSONModel

from api.features.recipes import schemas


class URL(JSONModel):
    url: str


class RecipeImport(schemas.RecipeBase):
    id: int
    imported: bool

    class Config:
        orm_mode = True


class SingleRecipeImport(RecipeImport):
    ingredients: List[schemas.RecipeIngredient]
    instructions: List[schemas.Instruction]

    class Config:
        orm_mode = True
