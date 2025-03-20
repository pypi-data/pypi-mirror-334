from ...domain.models.product import Product
from ...utils.string import build_query_params
from ...infrastructure.clients.http_client import Client
from typing import List

class ProductService:
    def __init__(self, client: Client):
        self._client = client

    def get(self, product_id: str):
        """
        Retrieve a product by its ID.
        
        Args:
            product_id (str): ID of the product to retrieve.
            
        Returns:
            Product: The retrieved product object.
        """
        response = self._client.get(f"products/{product_id}")
        return Product(**response.json())

    def delete(self, product_id: str):
        """
        Delete a product by its ID.
        
        Args:
            product_id (str): ID of the product to delete.
            
        Returns:
            Product: Deleted product object.
        """
        self._client.delete(f"products/{product_id}")

    def list(self, offset: int = None, limit: int = None) -> List[Product]:
        """
        Get a list of products.
        
        Args:
            offset (int, optional): Offset for pagination.
            limit (int, optional): Limit for pagination.
            
        Returns:
            list[Product]: List of products.
        """
        query_params = build_query_params(offset=offset, limit=limit)
        response = self._client.get(f"products?{query_params}")
        products = [Product(**product) for product in response.json()]
        return products
