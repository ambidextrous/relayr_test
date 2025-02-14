from typing import List, Dict, Optional
import sqlite3
import aiosqlite
from datetime import datetime
from sqlite3 import Connection, Cursor
from aiosqlite import Connection as AsyncConnection, Cursor as AsyncCursor

from product_comparison_service.data_classes.data_classes import (
    Product,
    Supplier,
    SupplierProduct,
    Category,
)


def setup_database(database: str) -> None:
    conn, cursor = get_database_conn_and_cursor(database)
    create_product_table(conn=conn, cursor=cursor)
    create_supplier_table(conn=conn, cursor=cursor)
    create_supplier_product_table(conn=conn, cursor=cursor)


def get_database_conn_and_cursor(database: str) -> None:
    """
    Get a synchronous connection and cursor connection to an Sqlite database instance
    """
    # Connect to DB (or create if does not exist)
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    return conn, cursor


def create_product_table(conn: Connection, cursor: Cursor) -> None:
    """ 
    Create product table 
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


def create_supplier_table(conn: Connection, cursor: Cursor) -> None:
    """ 
    Create supplier table 
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


def create_supplier_product_table(conn: Connection, cursor: Cursor) -> None:
    """ 
    Create supplier_product table 
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


def insert_product(conn: Connection, cursor: Cursor, product: Product) -> None:
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


async def update_product_search_results(
    conn: AsyncConnection, cursor: AsyncCursor, search_results: Dict[str, str]
) -> None:
    """
    Update product search results in database
    """

    for result in search_results:

        supplier_product_sql = """UPDATE supplier_product
            SET price = ?
            WHERE supplier = ? AND product = ?"""

        await cursor.execute(
            supplier_product_sql,
            (result.get("price"), result.get("supplier"), result.get("product")),
        )

        product_sql = """UPDATE product
            SET last_updated = ?
            WHERE name = ?"""

        await cursor.execute(
            product_sql, (result.get("last_updated"), result.get("product"))
        )

    await conn.commit()


async def delete_supplier_product_data(
    conn: AsyncConnection,
    cursor: AsyncCursor,
    product: Product,
    supplier: Supplier,
    commit: bool = True,
) -> None:
    """
    Delete supplier_product data from database
    """

    # Delete supplier_product

    supplier_product_sql = """DELETE FROM supplier_product 
        WHERE supplier = ? AND product = ?"""

    await cursor.execute(supplier_product_sql, (supplier, product))

    # If no remaining suppliers for product, delete product too

    product_select_sql = """SELECT supplier FROM supplier_product 
        WHERE product = ?"""

    select_results = await cursor.execute(product_select_sql, (product,))

    if not select_results:

        delete_product_sql = """DELETE FROM product WHERE name = ?"""

        await cursor.execute(delete_product_sql, (product,))

    if commit:
        await conn.commit()


async def update_supplier_product_data(
    conn: AsyncConnection,
    cursor: AsyncCursor,
    product: str,
    description: str,
    category: str,
    price: float,
    supplier: str,
    product_rating: float,
    last_updated: str,
) -> None:
    """
    Update product search results in database
    """

    # Delete existing supplier_product
    await delete_supplier_product_data(conn, cursor, product, supplier, commit=False)

    product_select_sql = """SELECT name FROM product 
        WHERE name = ?"""

    select_results = await cursor.execute(product_select_sql, (product,))

    # If product exists, update data
    if select_results:

        product_sql = """UPDATE product
            SET description = ?,
            category = ?,
            product_rating = ?, 
            last_updated = ?
            WHERE name = ?"""

        await cursor.execute(product_sql, (last_updated, product))

    # Else create product
    else:
        await cursor.execute(
            "INSERT INTO product values(?, ?, ?, ?, ?)",
            (product, description, category, last_updated, product_rating),
        )

    # Insert supplier_product
    await cursor.execute(
        "INSERT INTO supplier_product values(?, ?, ?)", (supplier, product, price)
    )

    await conn.commit()


def insert_supplier(conn: Connection, cursor: Cursor, supplier: Supplier) -> None:
    """
    Insert supplier into database
    """
    cursor.execute(
        "INSERT INTO supplier values(?, ?, ?)",
        (supplier.name, supplier.pull_url, supplier.rating),
    )
    conn.commit()


def insert_supplier_product(
    conn: Connection, cursor: Cursor, supplier_product: SupplierProduct
) -> None:
    """
    Insert supplier into database
    """
    cursor.execute(
        "INSERT INTO supplier_product values(?, ?, ?)",
        (supplier_product.supplier, supplier_product.product, supplier_product.price),
    )
    conn.commit()


async def search_by_product_or_category(
    conn, cursor, product: str = "", category: str = ""
) -> List[str]:
    """
    Search products by product and or category

    Returns results ranked by combined product.rating + supplier.rating
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
            product.description as description,
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


def insert_supplier(conn, cursor, supplier: Supplier) -> None:
    """
    Insert supplier into database
    """
    cursor.execute(
        "INSERT INTO supplier values(?, ?, ?)",
        (supplier.name, supplier.pull_url, supplier.rating),
    )
    conn.commit()
