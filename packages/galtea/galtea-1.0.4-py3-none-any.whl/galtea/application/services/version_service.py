from ...domain.models.version import VersionBase, Version, VersionBaseOptionalProps
from ...utils.string import sanitize_string, build_query_params
from ...infrastructure.clients.http_client import Client

class VersionService:
    def __init__(self, client: Client):
        self._client = client

    def version_exists(self, version_name: str) -> bool:
        """
        Check if a version exists by its name.
        
        Args:
            version_name (str): Name of the version.
            
        Returns:
            bool: True if the version exists, False otherwise.
        """
        version = self._client.versions(version_name)
        return bool(version)

    def create(self, product_id: str, name: str, optional_props: dict[str, str] = {}):
        """
        Given a version name, create a new version if it doesn't exist.
        
        Args:
            product_id (str): ID of the product.
            name (str): Name of the version.
            optional_props (dict[str, str], optional): Optional properties of the version.
                Possible keys include:
                - dataset_description: Description of the dataset used
                - dataset_uri: URI to the dataset
                - description: Version description
                - endpoint: API endpoint of the version
                - foundational_model: Base model information
                - guardrails: Guardrails configuration
                - provider: Model provider
                - system_prompt: Default system prompt of the model
            
        Returns:
            Version: The created version object.
        """
        for key, _ in optional_props.items():
            if key not in VersionBaseOptionalProps.__fields__:
                raise ValueError(f"Invalid key: {key}. Must be one of: {', '.join(VersionBaseOptionalProps.__fields__.keys())}")
        
        try:
            name = sanitize_string(name)
            version = VersionBase(
                name=name,
                product_id=product_id,
                **optional_props
            )
            version.model_validate(version.model_dump())
            response = self._client.post(f"versions", json=version.model_dump(by_alias=True))
            version_response = Version(**response.json())
            return version_response
        except Exception as e:
            print(f"Error creating version {name}: {e}")
            return None

    def get(self, version_id: str):
        """
        Retrieve a version by its ID.
        
        Args:
            version_id (str): ID of the version to retrieve.
            
        Returns:
            Version: The retrieved version object.
        """
        response = self._client.get(f"versions/{version_id}")
        return Version(**response.json())

    def list(self, product_id: str, offset: int = None, limit: int = None):
        """
        Get a list of versions for a given product.
        
        Args:
            product_id (str): ID of the product.
            offset (int, optional): Offset for pagination.
            limit (int, optional): Limit for pagination.
            
        Returns:
            list[Version]: List of version objects.
        """
        query_params = build_query_params(productIds=[product_id], offset=offset, limit=limit)
        response = self._client.get(f"versions?{query_params}")
        versions = [Version(**version) for version in response.json()]
        return versions

    def delete(self, version_id: str):
        """
        Delete a version by its ID.
        
        Args:
            version_id (str): ID of the version to delete.
            
        Returns:
            Version: Deleted version object.
        """
        self._client.delete(f"versions/{version_id}")