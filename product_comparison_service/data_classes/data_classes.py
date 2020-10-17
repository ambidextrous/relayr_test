from dataclasses import dataclass
from typing import Tuple
from datetime import datetime


@dataclass
class Supplier:
    name: str
    pull_url: str
    rating: float = 0.5


@dataclass
class Category:
    name: str


@dataclass
class Product:
    name: str
    description: str
    category: str
    last_updated: datetime
    rating: float = 0.5


@dataclass
class SupplierProduct:
    supplier: Supplier
    product: Product
    price: float
