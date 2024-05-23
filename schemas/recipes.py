from datetime import date
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# shared properties
class RecipeBase(BaseModel):
    title: Optional[str] = None
    ingredients: Optional[str] = None
    cooking: Optional[str] = None
    date_posted: Optional[date] = datetime.now().date()


# this will be used to validate data while creating a Recipe
class RecipeCreate(RecipeBase):
    title: str
    ingredients: str
    cooking: str


# this will be used to format the response to not to have id,owner_id etc
class ShowRecipe(RecipeBase):
    title: str
    date_posted: date
    ingredients: Optional[str]
    cooking: Optional[str]


    class Config:  # to convert non dict obj to json
        orm_mode = True
