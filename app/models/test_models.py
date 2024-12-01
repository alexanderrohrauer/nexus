from typing import Optional, List

from beanie import Document, Indexed, Link
from pydantic import BaseModel


class Comment(BaseModel):
    author: str
    body: str
    email: str


class Post(Document):
    author: str
    body: str
    comments: List[Comment]
    date: dict
    permalink: str
    tags: List[str]
    title: str


class Category(BaseModel):
    name: str
    description: str


# This is the model that will be saved to the database
class Product(Document):
    name: str  # You can use normal types just like in pydantic
    description: Optional[str]
    price: Indexed(float)  # You can also specify that a field should correspond to an index
    category: Category  # You can include pydantic models as well
    post: Optional[Link[Post]]
