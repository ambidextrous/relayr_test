import json
from datetime import datetime
import asyncio
from typing import List, Dict
from datetime import datetime

from tornado.web import RequestHandler
import aiosqlite

from database.database import search_by_product_or_category, update_product_search_results
from cache.cachedict import CacheDict
from config import DATABASE, CACHE_MAX_LENGTH, REFETCH_LIMIT

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class ProductHandler(RequestHandler):
    def __init__(self, *args, **kwargs):
        super(ProductHandler, self).__init__(*args, **kwargs)
        self.async_conn = None
        self.cache_dict = CacheDict(cache_len=CACHE_MAX_LENGTH)

    async def get_async_conn_and_cur(self):
        if self.async_conn:
            cursor = await self.async_conn.cursor()
        else:
            self.async_conn = await aiosqlite.connect(DATABASE)
            self.async_conn.row_factory = dict_factory
            cursor = await self.async_conn.cursor()
        return self.async_conn, cursor

    async def get(self):
        out_of_date_results = []

        product = self.get_argument("product", default=None)
        category = self.get_argument("category", default=None)

        # Check if search results in cache

        if (product, category) in self.cache_dict:

            products_found = self.write(self.cache_dict[(product, category)])

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
            if now - datetime.strptime(result.get("last_updated"), DATETIME_FORMAT) > REFETCH_LIMIT
        ]

        # Update results in db and cache

        if out_of_date_results:

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

        self.write({"search_results": results})

    async def make_dummy_calls_to_supplier_apis(self, search_results: List[Dict]):
        updated_results_dict = {}

        delay_in_seconds = 1
        print(f"Simulating {len(search_results)} simultaneous asynchronous API calls, each with a delay of {delay_in_seconds} seconds...")
        starttime = datetime.now() 
        dummy_external_api_calls = [asyncio.sleep(delay_in_seconds)]
        await asyncio.gather(*dummy_external_api_calls, return_exceptions=True)
        
        now = datetime.strftime(datetime.now(), DATETIME_FORMAT)

        for result in search_results:
            result["last_updated"] = now
            result["price"] += 1
            updated_results_dict[(result["supplier"],result["product"])] = result

        time_taken = datetime.now() - starttime
        print(f"Total time for asynchronous API calls taken: {time_taken}")

        return search_results

    async def update_db(self, search_results: List[Dict]):
        conn, cursor = await self.get_async_conn_and_cur()
        await update_product_search_results(conn, cursor, search_results)

    async def put(self):
        product = self.get_argument("product")
        category = self.get_argument("category")
        self.write("Hello, put!")

    async def delete(self):
        product = self.get_arguments("product")
        category = self.get_arguments("category")
        self.write("Coming soon...")
