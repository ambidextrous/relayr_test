import pytest
from asyncio import sleep
from unittest import mock
from datetime import datetime

from product_comparison_service.handlers.handlers import (
    ProductHandler,
    DocsHandler,
    DATETIME_FORMAT,
)


class AsyncMock(mock.MagicMock):
    async def __call__(self, *args, **kwargs):
        return super(AsyncMock, self).__call__(*args, **kwargs)


class TestGetDocs:
    @mock.patch("product_comparison_service.handlers.handlers.get_docs")
    @pytest.mark.asyncio
    async def test_get_docs(self, mock_get_docs):

        # Arrange
        mock_get_docs.return_value = "test_docs"
        mock_self = mock.MagicMock()

        # Act
        await DocsHandler.get(mock_self)

        # Assert
        mock_self.write.assert_called_once_with("test_docs")


class TestGetProducts:
    @mock.patch("product_comparison_service.handlers.handlers.get_docs")
    @pytest.mark.asyncio
    async def test_cached_hit(self, mock_get_docs):

        # Arrange
        timestamp = datetime.strftime(datetime.now(), DATETIME_FORMAT)
        mock_get_docs.return_value = "test_docs"

        mock_self = mock.MagicMock()
        mock_self.get_argument.side_effect = ["test_product", "test_category"]
        mock_self.cache_dict = {
            ("test_product", "test_category"): [
                {
                    "product": "coyotee",
                    "description": "Oportunistic",
                    "category": "Canines",
                    "price": 1000000000.0,
                    "supplier": "DavesPets",
                    "product_rating": 0.4,
                    "supplier_rating": 0.8,
                    "combined_rating": 0.6,
                    "last_updated": timestamp,
                }
            ]
        }

        expected_write_value = {
            "success": True,
            "search_results": [
                {
                    "product": "coyotee",
                    "description": "Oportunistic",
                    "category": "Canines",
                    "price": 1000000000.0,
                    "supplier": "DavesPets",
                    "product_rating": 0.4,
                    "supplier_rating": 0.8,
                    "combined_rating": 0.6,
                    "last_updated": timestamp,
                }
            ],
        }

        # Act
        await ProductHandler.get(mock_self)

        # Assert
        mock_self.write.assert_called_once_with(expected_write_value)

    @mock.patch(
        "product_comparison_service.handlers.handlers.search_by_product_or_category",
        new_callable=AsyncMock,
    )
    @pytest.mark.asyncio
    async def test_db_hit(self, mock_search_by_product_or_category):

        # Arrange
        timestamp = datetime.strftime(datetime.now(), DATETIME_FORMAT)
        mock_self = mock.MagicMock()
        mock_self.get_argument.side_effect = ["test_product", "test_category"]
        mock_self.cache_dict = {}
        mock_self.get_async_conn_and_cur = mock.AsyncMock()
        mock_self.get_async_conn_and_cur.return_value = ("test_conn", "test_cur")
        mock_search_by_product_or_category.return_value = [
            {
                "product": "coyotee",
                "description": "Oportunistic",
                "category": "Canines",
                "price": 1000000000.0,
                "supplier": "DavesPets",
                "product_rating": 0.4,
                "supplier_rating": 0.8,
                "combined_rating": 0.6,
                "last_updated": timestamp,
            }
        ]

        expected_write_value = {
            "success": True,
            "search_results": [
                {
                    "product": "coyotee",
                    "description": "Oportunistic",
                    "category": "Canines",
                    "price": 1000000000.0,
                    "supplier": "DavesPets",
                    "product_rating": 0.4,
                    "supplier_rating": 0.8,
                    "combined_rating": 0.6,
                    "last_updated": timestamp,
                }
            ],
        }

        # Act
        await ProductHandler.get(mock_self)

        # Assert
        mock_self.write.assert_called_once_with(expected_write_value)

    @mock.patch(
        "product_comparison_service.handlers.handlers.search_by_product_or_category",
        new_callable=AsyncMock,
    )
    @pytest.mark.asyncio
    async def test_api_hit(self, mock_search_by_product_or_category):

        # Arrange
        mock_self = mock.MagicMock()
        mock_self.get_argument.side_effect = ["test_product", "test_category"]
        mock_self.cache_dict = {}
        mock_self.get_async_conn_and_cur = mock.AsyncMock()
        mock_self.get_async_conn_and_cur.return_value = ("test_conn", "test_cur")
        mock_search_by_product_or_category.return_value = [
            {
                "product": "coyotee",
                "description": "Oportunistic",
                "category": "Canines",
                "price": 1000000000.0,
                "supplier": "DavesPets",
                "product_rating": 0.4,
                "supplier_rating": 0.8,
                "combined_rating": 0.6,
                "last_updated": "2020-10-10T09:22:37.398697",
            }
        ]
        updated_results = {
            ("DavesPets", "coyotee"): {
                "product": "coyotee",
                "description": "Oportunistic",
                "category": "Canines",
                "price": 1,
                "supplier": "DavesPets",
                "product_rating": 0.4,
                "supplier_rating": 0.8,
                "combined_rating": 0.6,
                "last_updated": "2020-10-10T09:22:37.398697",
            }
        }
        mock_self.make_dummy_calls_to_supplier_apis = mock.AsyncMock()
        mock_self.make_dummy_calls_to_supplier_apis.return_value = updated_results
        mock_self.update_db = mock.AsyncMock()

        expected_write_value = {
            "success": True,
            "search_results": [
                {
                    "product": "coyotee",
                    "description": "Oportunistic",
                    "category": "Canines",
                    "price": 1,
                    "supplier": "DavesPets",
                    "product_rating": 0.4,
                    "supplier_rating": 0.8,
                    "combined_rating": 0.6,
                    "last_updated": "2020-10-10T09:22:37.398697",
                }
            ],
        }

        # Act
        await ProductHandler.get(mock_self)

        # Assert
        mock_self.write.assert_called_once_with(expected_write_value)


class TestDeleteProduct:
    @mock.patch(
        "product_comparison_service.handlers.handlers.delete_supplier_product_data",
        new_callable=AsyncMock,
    )
    @pytest.mark.asyncio
    async def test_delete(self, mock_delete_supplier_product_data):

        # Arrange
        timestamp = datetime.strftime(datetime.now(), DATETIME_FORMAT)
        mock_self = mock.MagicMock()
        mock_self.get_argument.side_effect = ["test_product", "test_category"]
        mock_self.get_async_conn_and_cur = mock.AsyncMock()
        mock_self.get_async_conn_and_cur.return_value = ("test_conn", "test_cur")

        expected_write_value = {
            "success": True,
            "deleted": {"product": "test_product", "supplier": "test_category"},
        }

        # Act
        await ProductHandler.delete(mock_self)

        # Assert
        mock_delete_supplier_product_data.assert_called_once_with(
            "test_conn", "test_cur", "test_product", "test_category"
        )
        mock_self.write.assert_called_once_with(expected_write_value)


class TestPutProduct:
    @mock.patch("product_comparison_service.handlers.handlers.datetime")
    @mock.patch(
        "product_comparison_service.handlers.handlers.update_supplier_product_data",
        new_callable=AsyncMock,
    )
    @pytest.mark.asyncio
    async def test_delete(self, mock_update_supplier_product_data, mock_datetime):

        # Arrange
        timestamp = datetime.strftime(datetime.now(), DATETIME_FORMAT)
        mock_datetime.strftime.return_value = timestamp
        mock_self = mock.MagicMock()
        mock_self.get_argument.side_effect = [
            "test_product",
            "test_desciption",
            "test_category",
            "test_price",
            "test_supplier",
            "test_product_rating",
        ]
        mock_self.get_async_conn_and_cur = mock.AsyncMock()
        mock_self.get_async_conn_and_cur.return_value = ("test_conn", "test_cur")

        expected_write_value = {
            "success": True,
            "upserted": {
                "product": "test_product",
                "description": "test_desciption",
                "category": "test_category",
                "price": "test_price",
                "supplier": "test_supplier",
                "product_rating": "test_product_rating",
                "last_updated": timestamp,
            },
        }

        # Act
        await ProductHandler.put(mock_self)

        # Assert
        mock_update_supplier_product_data.assert_called_once()
        mock_self.write.assert_called_once_with(expected_write_value)
