import json

import click

from database.database import (
    get_database_conn_and_cursor,
    insert_product,
    insert_supplier,
    insert_supplier_product,
)
from config import DATABASE
from data_classes.data_classes import Product, Supplier, SupplierProduct


@click.group()
def cli():
    """
    Command processor for a single entry point to product comparison service batch processing
    """
    pass


@click.command(
    name="add_products",
    help='Inserts products from a JSONL file of the format: {"name": "organutan", "description": "Ball of evervescent orange fury", "category": "Great Apes", "last_updated":"now", "rating": 0.999} to database',
)
@click.argument("filename")
def add_products(filename: str):
    """
    Insert product table entries
    """
    with open(filename, encoding="utf-8") as file:
        products = [json.loads(l.rstrip("\n")) for l in file if l]
        conn, cursor = get_database_conn_and_cursor(DATABASE)
        for product in products:
            current_product = Product(
                name=product.get("name"),
                description=product.get("description"),
                category=product.get("category"),
                last_updated=product.get("last_updated"),
                rating=product.get("rating"),
            )
            insert_product(conn, cursor, current_product)


@click.command(
    name="add_suppliers",
    help='Inserts suppliers from a JSONL file of the format: {"name": "iPet", "pull_url": "www.ipet.com/animals", "rating": 0.1} to database',
)
@click.argument("filename")
def add_suppliers(filename: str):
    """
    Insert supplier table entries
    """
    with open(filename, encoding="utf-8") as file:
        suppliers = [json.loads(l.rstrip("\n")) for l in file if l]
        conn, cursor = get_database_conn_and_cursor(DATABASE)
        for supplier in suppliers:
            current_supplier = Supplier(
                name=supplier.get("name"),
                pull_url=supplier.get("pull_url"),
                rating=supplier.get("rating"),
            )
            insert_supplier(conn, cursor, current_supplier)


@click.command(
    name="add_supplier_products",
    help='Inserts supplier_products from a JSONL file of the format: {"supplier": "iPet", "product": "coyotee", "price": 5.99} to database',
)
@click.argument("filename")
def add_supplier_products(filename: str):
    """
    Insert supplier_product table entries
    """
    with open(filename, encoding="utf-8") as file:
        supplier_products = [json.loads(l.rstrip("\n")) for l in file if l]
        conn, cursor = get_database_conn_and_cursor(DATABASE)
        for supplier_product in supplier_products:
            current_supplier_product = SupplierProduct(
                supplier=supplier_product.get("supplier"),
                product=supplier_product.get("product"),
                price=supplier_product.get("price"),
            )
            insert_supplier_product(conn, cursor, current_supplier_product)


cli.add_command(add_products)
cli.add_command(add_suppliers)
cli.add_command(add_supplier_products)


if __name__ == "__main__":
    cli()
