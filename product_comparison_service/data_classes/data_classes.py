from dataclasses import dataclass
from typing import Tuple


@dataclass
class Supplier:
    name: str
    can_pull_from: bool
    pull_url: str 


@dataclass
class Category:
    name: str
    products: Tuple[Product]


@dataclass
class Product:
    name: str 
    category: str 
    last_updated: 
    rating: int = 0



