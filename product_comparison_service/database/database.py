from typing import List
import sqlite3
import aiosqlite
from datetime import datetime

from data_classes.data_classes import Product, Supplier, SupplierProduct, Category


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
    conn.commit()


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
        price real NOT NULL,
        FOREIGN KEY(supplier) REFERENCES supplier(name),
        FOREIGN KEY(product) REFERENCES product(name)
    );
    """
    cursor.execute(create_table_sql)
    conn.commit()


def insert_product(conn, cursor, product: Product):
    """
    Insert product into database
    """
    cursor.execute(
        "INSERT INTO product values(?, ?, ?, ?, ?)",
        (
            product.name,
            product.description,
            product.category,
            product.last_updated,
            product.rating,
        ),
    )
    conn.commit()


async def update_product_search_results(conn, cursor, search_results):
    """
    Insert product into database
    """

    for result in search_results:

        supplier_product_sql = """UPDATE supplier_product
            SET price = ?
            WHERE supplier = ? AND product = ?"""

        await cursor.execute(
            supplier_product_sql,
            (
                result.get("price"),
                result.get("supplier"),
                result.get("product")
            ),
        )

        product_sql = """UPDATE product
            SET last_updated = ?
            WHERE name = ?"""

        await cursor.execute(
            product_sql,
            (
                result.get("last_updated"),
                result.get("product")
            ),
        )
        
    await conn.commit()


def insert_supplier(conn, cursor, supplier: Supplier):
    """
    Insert supplier into database
    """
    cursor.execute(
        "INSERT INTO supplier values(?, ?, ?)",
        (supplier.name, supplier.pull_url, supplier.rating),
    )
    conn.commit()


def insert_supplier_product(conn, cursor, supplier_product: SupplierProduct):
    """
    Insert supplier into database
    """
    cursor.execute(
        "INSERT INTO supplier_product values(?, ?, ?)",
        (supplier_product.supplier, supplier_product.product, supplier_product.price),
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
        filter_term = (
            f"\n        WHERE product = '{product}' AND category = '{category}'"
        )
    elif product:
        filter_term = f"\n        WHERE product = '{product}'"
    else:
        filter_term = f"\n        WHERE category = '{category}'"

    statement = f"""
        SELECT product.name as product,
            product.category as category,
            supplier_product.price as price,
            supplier_product.supplier as supplier,
            supplier_product.price as price,
            product.rating as product_rating,
            supplier.rating as supplier_rating,
            ROUND(((product.rating + supplier.rating)/2),2) as combined_rating,
            product.last_updated as last_updated 
        FROM product 
        INNER JOIN supplier_product
        ON product.name = supplier_product.product
        INNER JOIN supplier 
        ON supplier_product.supplier = supplier.name {filter_term}
        ORDER BY (product.rating + supplier.rating) DESC
        """
    await cursor.execute(statement)
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
