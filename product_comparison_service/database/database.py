from typing import List
import sqlite3
import aiosqlite
from datetime import datetime

from data_classes.data_classes import (
    Product,
    Supplier,
    SupplierProduct,
    Category,
)


def setup_database(database: str):
    conn, cursor = get_database_conn_and_cursor(database)
    create_product_table(conn=conn, cursor=cursor)
    create_supplier_table(conn=conn, cursor=cursor)
    create_supplier_product_table(conn=conn, cursor=cursor)


def get_database_conn_and_cursor(database: str):
    """
    Get a connection and cursor connection to an Sqlite database instance
    """
    # Connect to DB (or create if does not exist)
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    return conn, cursor


def create_product_table(conn, cursor):
    """ 
    Create product table 
    :param conn: Connection object
    :return:
    """
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS product (
        name text PRIMARY KEY,
        description text,
        category text NOT NULL,
        last_updated timestamp NOT NULL,
        rating real
    );
    """
    cursor.execute(create_table_sql)
    conn.commit()


def create_supplier_table(conn, cursor):
    """ 
    Create supplier table 
    :param conn: Connection object
    :return:
    """
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS supplier (
        name text PRIMARY KEY,
        pull_url text,
        rating real
    );
    """
    cursor.execute(create_table_sql)


def create_supplier_product_table(conn, cursor):
    """ 
    Create category table 
    :param conn: Connection object
    :return:
    """
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS supplier_product (
        supplier text NOT NULL,
        product text NOT NULL,
        price real NOT NULL
    );
    """
    cursor.execute(create_table_sql)


def insert_product(conn, cursor, product: Product):
    """
    Insert product into database
    """
    cursor.execute(
        "INSERT INTO product values(?, ?, ?, ?, ?)",
        (product.name, product.description, product.category, product.last_updated, product.rating),
    )
    conn.commit()


def insert_category(conn, cursor, insert_supplier_product: SupplierProduct):
    """
    Insert category into database
    """
    cursor.execute(
        "INSERT INTO supplier_product values(?, ?, ?)",
        (supplier_product.supplier, supplier_product.product, supplier_product.price),
    )
    conn.commit()


def insert_supplier(conn, cursor, supplier: Supplier):
    """
    Insert supplier into database
    """
    cursor.execute(
        "INSERT INTO supplier values(?, ?, ?)",
        (supplier.name, supplier.pull_url, supplier.rating),
    )
    conn.commit()


## Async functions

async def search_by_product_or_category(
    conn, cursor, product: str = "", category: str = ""
) -> List[str]:
    """
    Search products by product and or category
    """

    if (not product) and (not category):
        filter_term = ""
    elif product and category:
        filter_term = f"\n      WHERE product = {product} AND category = {category}\n"
    elif product:
        filter_term = f"\n      WHERE product = {product}\n"
    else:
        filter_term = f"\n      WHERE category = {category}\n"

    filter_term = f"""
        SELECT product.name as product,
            product.category as category,
            supplier_product.price as price,
            supplier_product.supplier as supplier,
            supplier_product.price as price,
            product.rating as product_rating,
            supplier.rating as supplier_rating,
        FROM product 
        INNER JOIN supplier_product
        ON product.name = supplier_product.product
        INNER JOIN supplier 
        ON supplier_product.supplier = supplier.name {filter_term}
        ORDER BY (product.rating + supplier.rating) DESC
        """
    await cursor.execute()
    categories = await cursor.fetchall()
    return categories


def insert_supplier(conn, cursor, supplier: Supplier):
    """
    Insert supplier into database
    """
    cursor.execute(
        "INSERT INTO supplier values(?, ?, ?)",
        (supplier.name, supplier.pull_url, supplier.rating),
    )
    conn.commit()
