from dataclasses import dataclass
from typing import Tuple
from datetime import datetime


@dataclass
class Supplier:
    name: str
    pull_url: str
    rating: float = 0.5

{"name": "iPet", "pull_url": "www.ipet.com/animals", "rating": 0.1}
{"name": "CheapPets", "pull_url": "www.cheap-pets.com/animals", "rating": 0.2}
{"name": "DavesPets", "pull_url": "www.daves-pets.com/animals", "rating": 0.8}


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

{"name": "organutan", "description": "Ball of evervescent orange fury", "category": "Great Apes", "last_updated":"now", "rating": 0.999}
{"name": "gorilla", "description": "Friendly giant", "category": "Great Apes", "last_updated":"now", "rating": 0.81}
{"name": "chimpanzee", "description": "Humanish, all to humanish", "category": "Great Apes", "last_updated":"now", "rating": 0.7}
{"name": "dog", "description": "Man's best friend", "category": "Canines", "last_updated":"now", "rating": 0.2}
{"name": "wolf", "description": "Noctural", "category": "Canines", "last_updated":"now", "rating": 0.3}
{"name": "coyotee", "description": "Oportunistic", "category": "Canines", "last_updated":"now", "rating": 0.4}


@dataclass
class SupplierProduct:
    supplier: Supplier
    product: Product
    price: float

{"supplier": "iPet", "product": "coyotee", "price": 5}
{"supplier": "iPet", "product": "orangutan", "price": 1000000}
{"supplier": "iPet", "product": "dog", "price": 7}
{"supplier": "CheapPets", "product": "coyotee", "price": 100}
{"supplier": "CheapPets", "product": "gorilla", "price": 15}
{"supplier": "CheapPets", "product": "dog", "price": 1}
{"supplier": "DavesPets", "product": "dog", "price": 0.1}
{"supplier": "DavesPets", "product": "coyotee", "price": 9999999999999}
{"supplier": "DavesPets", "product": "orangutan", "price": 7}
