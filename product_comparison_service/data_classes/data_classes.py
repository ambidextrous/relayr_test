from dataclasses import dataclass
from typing import Tuple
from datetime import datetime


@dataclass
class Supplier:
    """
    Data class corresponding with supplier database table
    """

    name: str
    pull_url: str
    rating: float = 0.5


@dataclass
class Category:
    name: str


@dataclass
class Product:
    """
    Data class corresponding with product database table
    """

    name: str
    description: str
    category: str
    last_updated: datetime
    rating: float = 0.5


@dataclass
class SupplierProduct:
    """
    Data class corresponding with supplier_product database table
    """

    supplier: Supplier
    product: Product
    price: float
