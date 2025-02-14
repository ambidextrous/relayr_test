import json
from datetime import datetime
import asyncio
from typing import List, Dict, Tuple
from datetime import datetime

from tornado.web import RequestHandler
import aiosqlite
from aiosqlite import Connection as AsyncConnection, Cursor as AsyncCursor

from product_comparison_service.database.database import (
    search_by_product_or_category,
    update_product_search_results,
    delete_supplier_product_data,
    update_supplier_product_data,
)
from product_comparison_service.cache.cachedict import CacheDict
from product_comparison_service.docs.docs import DOCS
from product_comparison_service.config import DATABASE, CACHE_MAX_LENGTH, REFETCH_LIMIT

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"


def dict_factory(cursor, row) -> Dict:
    """
    Helper method to transform aiosqlite results into dict format
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class ProductHandler(RequestHandler):
    def __init__(self, *args, **kwargs):
        """
        Initialize Product endpoint handler, with instance variables
        storing database connection and cache dict
        """
        super(ProductHandler, self).__init__(*args, **kwargs)
        self.async_conn = None
        self.cache_dict = CacheDict(cache_len=CACHE_MAX_LENGTH)

    async def get_async_conn_and_cur(self) -> Tuple[AsyncConnection, AsyncCursor]:
        """
        Get async database connection and cursor        
        """
        if self.async_conn:
            cursor = await self.async_conn.cursor()
        else:
            self.async_conn = await aiosqlite.connect(DATABASE)
            self.async_conn.row_factory = dict_factory
            cursor = await self.async_conn.cursor()
        return self.async_conn, cursor

    async def get(self) -> None:
        """
        Returns search results ordered by combined product and supplier scores.

        Handles calls to GET method of /product end-point
        - First searches cache for search results
        - If no results found in cache, searches database
        - If results not found or out of date results found, searches supplier APIs
        - Updates database and cache with new results
        - Gives results as response

        localhost:8888/v0.1/product?product=coyotee&category=Canines

        curl -d "product=coyotee&category=Canines" -X GET localhost:8888/v0.1/product
        """
        out_of_date_results = []

        product = self.get_argument("product", default=None)
        category = self.get_argument("category", default=None)

        # Check if search results in cache

        if (product, category) in self.cache_dict:

            results = self.cache_dict[(product, category)]

        # Check if search results in database

        else:

            conn, cursor = await self.get_async_conn_and_cur()

            results = await search_by_product_or_category(
                conn=conn, cursor=cursor, product=product, category=category
            )

        now = datetime.now()

        # Check if any results out of date

        out_of_date_results = [
            result
            for result in results
            if now - datetime.strptime(result.get("last_updated"), DATETIME_FORMAT)
            > REFETCH_LIMIT
        ]

        # Update results in db and cache

        if out_of_date_results or not results:

            updated_results = await self.make_dummy_calls_to_supplier_apis(results)

            combined_results = []

            for result in results:

                key = (result["supplier"], result["product"])

                if key in updated_results:
                    combined_results.append(updated_results[key])

                else:
                    combined_results.append(result)

            results = combined_results

            await self.update_db(combined_results)

            self.cache_dict[(product, category)] = results

        # Write response
        self.write({"success": True, "search_results": results})

    async def make_dummy_calls_to_supplier_apis(
        self, search_results: List[Dict]
    ) -> Dict[Tuple[str, str], List]:
        """
        Method mocks simultaneous asynchronous calls to external APIs
        """
        updated_results_dict = {}
        num_api_calls = len(search_results) or 10

        delay_in_seconds = 1
        print(
            f"Simulating {num_api_calls} simultaneous asynchronous API calls, each with a delay of {delay_in_seconds} seconds..."
        )
        starttime = datetime.now()
        dummy_external_api_calls = [
            asyncio.sleep(delay_in_seconds) for i in range(num_api_calls)
        ]
        await asyncio.gather(*dummy_external_api_calls, return_exceptions=True)

        now = datetime.strftime(datetime.now(), DATETIME_FORMAT)

        for result in search_results:
            result["last_updated"] = now
            result["price"] += 1
            updated_results_dict[(result["supplier"], result["product"])] = result

        time_taken = datetime.now() - starttime
        print(f"Total time for asynchronous API calls taken: {time_taken}")

        return search_results

    async def update_db(self, search_results: List[Dict]) -> None:
        conn, cursor = await self.get_async_conn_and_cur()
        await update_product_search_results(conn, cursor, search_results)

    async def put(self) -> None:
        """
        Handles calls to PUT method of /product end-point
        - If required parameters supplied, responds updates database with
        new product data (inserting rows in product and supplier_product tables)
        and returns a success message.

        localhost:8888/v0.1/product?product=owl&description=wise&price=3&supplier=DavesPets&product_rating=0.98&category=Birds
        
        curl -d "product=owl&description=wise&price=3&supplier=DavesPets&product_rating=0.98&category=Birds" -X PUT localhost:8888/v0.1/product
        """
        product = self.get_argument("product")
        description = self.get_argument("description")
        category = self.get_argument("category")
        price = self.get_argument("price")
        supplier = self.get_argument("supplier")
        product_rating = self.get_argument("product_rating", default=0.5)
        last_updated = datetime.strftime(datetime.now(), DATETIME_FORMAT)
        conn, cursor = await self.get_async_conn_and_cur()
        await update_supplier_product_data(
            conn,
            cursor,
            product,
            description,
            category,
            price,
            supplier,
            product_rating,
            last_updated,
        )
        self.write(
            {
                "success": True,
                "upserted": {
                    "product": product,
                    "description": description,
                    "category": category,
                    "price": price,
                    "supplier": supplier,
                    "product_rating": product_rating,
                    "last_updated": last_updated,
                },
            }
        )

    async def delete(self) -> None:
        """
        Handles calls to DELETE method of /product end-point
        - If required parameters supplied, removes product data (deleting any rows 
        in product and supplier_product tables) and returns a success message.

        localhost:8888/v0.1/product?product=coyotee&supplier=DavesPets

        curl -d "product=coyotee&supplier=DavesPets" -X DELETE localhost:8888/v0.1/product

        """
        product = self.get_argument("product")
        supplier = self.get_argument("supplier")
        conn, cursor = await self.get_async_conn_and_cur()
        await delete_supplier_product_data(conn, cursor, product, supplier)
        self.write(
            {"success": True, "deleted": {"product": product, "supplier": supplier}}
        )


class DocsHandler(RequestHandler):
    async def get(self) -> None:
        """
        Handles calls to documentation page. Returns static file of documenation in
        OpenAPI format.
        """
        self.write(get_docs())


def get_docs() -> str:
    return DOCS
