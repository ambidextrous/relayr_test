#import asynctest
import pytest
from asyncio import sleep
from unittest import mock

from product_comparison_service.handlers.handlers import ProductHandler, DocsHandler


class TestDocs:
    @mock.patch("product_comparison_service.handlers.handlers.get_docs")
    @pytest.mark.asyncio
    async def test_docs(self, mock_get_docs):
        
        # Arrange
        mock_get_docs.return_value = "test_docs"
        mock_self = mock.MagicMock()

        # Act
        await DocsHandler.get(mock_self)

        # Assert
        mock_self.write.assert_called_once_with("test_docs")
