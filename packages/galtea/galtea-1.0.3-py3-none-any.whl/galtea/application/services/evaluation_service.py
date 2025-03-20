from ...domain.models.evaluation import EvaluationBase, Evaluation
from ...infrastructure.clients.http_client import Client
from ...utils.string import build_query_params

class EvaluationService:
    def __init__(self, client: Client):
        self._client = client

    def create(self, test_id: str, version_id: str):
        """
        Create a new evaluation based on the test and version IDs.
        
        Args:
            test_id (str): ID of the test.
            version_id (str): ID of the version.
            
        Returns:
            Evaluation: The created evaluation object.
        """
        try:
            evaluation = EvaluationBase(
                test_id=test_id,
                version_id=version_id,
            )

            evaluation.model_validate(evaluation.model_dump())
            response = self._client.post(f"evaluations", json=evaluation.model_dump(by_alias=True))
            evaluation_response = Evaluation(**response.json())
            
            return evaluation_response
        except Exception as e:
            print(f"Error creating Evaluation: {e}")
            return None

    def get(self, evaluation_id: str):
        """
        Retrieve an evaluation by its ID.
        
        Args:
            evaluation_id (str): ID of the evaluation to retrieve.
            
        Returns:
            Evaluation: The retrieved evaluation object.
        """
        response = self._client.get(f"evaluations/{evaluation_id}")
        return Evaluation(**response.json())
    
        
    def list(self, product_id: str, offset: int = None, limit: int = None):
        """
        Get a list of evaluations for a given product.
        
        Args:
            product_id (str): ID of the product.
            offset (int, optional): Offset for pagination.
            limit (int, optional): Limit for pagination.
            
        Returns:
            list[Evaluation]: List of evaluations.
        """
        query_params = build_query_params(productIds=[product_id], offset=offset, limit=limit)
        response = self._client.get(f"evaluations/ofProducts?{query_params}")
        evaluations = [Evaluation(**evaluation) for evaluation in response.json()]
        return evaluations
    
    def delete(self, evaluation_id: str):
        """
        Delete an evaluation by its ID.
        
        Args:
            evaluation_id (str): ID of the evaluation to delete.
        """
        self._client.delete(f"evaluations/{evaluation_id}")