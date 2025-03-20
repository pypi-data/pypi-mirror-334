from ...domain.models.metric_type import MetricType, MetricTypeBase
from ...utils.string import build_query_params
from ...infrastructure.clients.http_client import Client
from typing import List

class MetricTypeService:

    def __init__(self, client: Client):
        self._client = client

    def create(self, name: str, criteria: str | None = None, evaluation_steps: list[str] | None = None):
        """
        Create a new metric type.
        
        Args:
            name (str): Name of the metric type.
            criteria (str, optional): Criteria for the metric type.
            evaluation_steps (list[str], optional): Evaluation steps for the metric type.
            
        Returns:
            MetricType: The created metric type object.
        """
        try:
            metric_type = MetricTypeBase(
                name=name,
                criteria=criteria,
                evaluation_steps=evaluation_steps,
            )

            metric_type.model_validate(metric_type.model_dump())
            response = self._client.post(f"metricTypes", json=metric_type.model_dump(by_alias=True))
            metric_type_response = MetricType(**response.json())
            
            return metric_type_response
        except Exception as e:
            print(f"Error creating Metric Type: {e}")
            return None

    def get(self, metric_type_id: str):
        """
        Retrieve a metric type by its ID.
        
        Args:
            metric_type_id (str): ID of the metric type to retrieve.
            
        Returns:
            MetricType: The retrieved metric type object.
        """
        response = self._client.get(f"metricTypes/{metric_type_id}")
        return MetricType(**response.json())

    def delete(self, metric_type_id: str):
        """
        Delete a metric type by its ID.
        
        Args:
            metric_type_id (str): ID of the metric type to delete.
            
        Returns:
            MetricType: Deleted metric type object.
        """
        self._client.delete(f"metricTypes/{metric_type_id}")
    
    def list(self, offset: int = None, limit: int = None) -> List[MetricType]:
        """
        Get a list of metric types.
        
        Args:
            offset (int, optional): Offset for pagination.
            limit (int, optional): Limit for pagination.
            
        Returns:
            list[MetricType]: List of metric types.
        """
        query_params = build_query_params(offset=offset, limit=limit)
        response = self._client.get(f"metricTypes?{query_params}")
        metric_types = [MetricType(**metric_type) for metric_type in response.json()]
        return metric_types
