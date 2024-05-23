from db.base_class import Base
from sqlalchemy import Boolean, ForeignKey
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship

class Rating(Base):
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("user.id"))
    recipe_id = Column(Integer, ForeignKey("recipe.id"))
    __table_args__ = (UniqueConstraint('owner_id', 'recipe_id', name='unique_owner_recipe'),)


