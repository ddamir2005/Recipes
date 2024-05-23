from sqlalchemy.exc import IntegrityError
from db.models.ratings import Rating
from db.models.recipes import Recipe
from db.models.users import User
from schemas.recipes import RecipeCreate
from sqlalchemy.orm import Session
from fastapi import HTTPException


def create_new_recipe(recipe: RecipeCreate, db: Session, owner_id: int):
    recipe_object = Recipe(**recipe.dict(), owner_id=owner_id)
    db.add(recipe_object)
    db.commit()
    db.refresh(recipe_object)
    return recipe_object


def retreive_recipe(id: int, db: Session):
    item = db.query(Recipe).filter(Recipe.id == id).first()
    user = db.query(User).filter(User.id == item.owner_id).first()
    item.owner_rating = user.rating
    item.owner_name = user.username
    return item


def list_recipes(db: Session):
    recipes = db.query(Recipe).all()
    return recipes

def list_recipes_for_current_user(db: Session, owner_id: int):
    recipes = db.query(Recipe).filter(Recipe.owner_id == owner_id).all()
    return recipes


def update_recipe_by_id(id: int, recipe: RecipeCreate, db: Session, owner_id):
    existing_recipe = db.query(Recipe).filter(Recipe.id == id)
    if not existing_recipe.first():
        return 0
    recipe.__dict__.update(
        owner_id=owner_id
    )  # update dictionary with new key value of owner_id
    existing_recipe.update(recipe.__dict__)
    db.commit()
    return 1


def delete_recipe_by_id(id: int, db: Session, owner_id):
    existing_recipe = db.query(Recipe).filter(Recipe.id == id)
    if not existing_recipe.first():
        return 0
    existing_recipe.delete(synchronize_session=False)
    db.commit()
    return 1


def search_recipe(query: str, db: Session):
    recipes = db.query(Recipe).filter(Recipe.title.contains(query))
    return recipes

def rate_recipe_by_id(id: int, db: Session, owner_id: int):
    rate_object = Rating(owner_id=owner_id, recipe_id=id)
    try:
        db.add(rate_object)
        db.commit()
        db.refresh(rate_object)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Ошибка. Вы уже лайкали этот рецепт!")
    return rate_object