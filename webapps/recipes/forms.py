from typing import List
from typing import Optional

from fastapi import Request


class RecipeCreateForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.title: Optional[str] = None
        self.ingredients: Optional[str] = None
        self.cooking: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.title = form.get("title")
        self.ingredients = form.get("ingredients")
        self.cooking = form.get("cooking")

    def is_valid(self):
        if not self.title:
            self.errors.append("Введите название")

        if not self.errors:
            return True
        return False
