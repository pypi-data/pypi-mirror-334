from ...infrastructure.clients.http_client import Client
from galtea.domain.models.evaluation_task import EvaluationTask, EvaluationTaskBase
from galtea.utils.string import build_query_params

class EvaluationTaskService:
    def __init__(self, client: Client):
        self._client = client

    def create(self, metrics: list[str], evaluation_id: str, input: str, actual_output: str, expected_output: str = None, context: str = None):
        """
        Given an evaluation id, create a set of evaluation tasks to evaluate your product based on the metrics provided.
        This function will create a new evaluation task for each metric type provided in the list.
        
        Args:
        metrics (list[str]): List of metric type names.
        evaluation_id (str): ID of the evaluation.
        input (str): Input for the evaluation task.
        actual_output (str): Actual output for the evaluation task.
        expected_output (str, optional): Expected output for the evaluation task.
        context (str, optional): Context for the evaluation task.
        
        Returns:
        list[EvaluationTask]: List of evaluation tasks created.
        """
        try:
            # Create the base object with the fields it supports
            evaluation_task = EvaluationTaskBase(
                evaluation_id=evaluation_id,
                input=input,
                actual_output=actual_output,
                expected_output=expected_output,
                context=context,
            )
            
            # Validate the base object
            evaluation_task.model_validate(evaluation_task.model_dump())
            
            # Create a dictionary with all fields including metric_type_names
            request_body = evaluation_task.model_dump(by_alias=True)
            request_body["metricTypeNames"] = metrics
            
            # Send the request with the complete body
            response = self._client.post(f"evaluationTasks", json=request_body)
            evaluation_tasks = [EvaluationTask(**evaluation_task) for evaluation_task in response.json()]
            return evaluation_tasks
        except Exception as e:
            print(f"Error creating evaluation task: {e}")
            return None

    def get(self, evaluation_task_id: str):
        """
        Retrieve an evaluation task by its ID.
        
        Args:
            evaluation_task_id (str): ID of the evaluation task to retrieve.
            
        Returns:
            EvaluationTask: The retrieved evaluation task object.
        """
        response = self._client.get(f"evaluationTasks/{evaluation_task_id}")
        return EvaluationTask(**response.json())

    def list(self, evaluation_id: str = [], offset: int = None, limit: int = None):
        """
        Get a list of evaluation tasks for a given evaluation.
        
        Args:
            evaluation_id (str): ID of the evaluation.
            offset (int, optional): Offset for pagination.
            limit (int, optional): Limit for pagination.
            
        Returns:
            list: List of evaluation tasks.
        """
        query_params = build_query_params(evaluationIds=[evaluation_id], offset=offset, limit=limit)
        response = self._client.get(f"evaluationTasks?{query_params}")
        evaluation_tasks = [EvaluationTask(**evaluation_task) for evaluation_task in response.json()]
        return evaluation_tasks

    def delete(self, evaluation_task_id: str):
        """
        Delete an evaluation task by its ID.
        
        Args:
            evaluation_task_id (str): ID of the evaluation task to delete.
            
        Returns:
            EvaluationTask: Deleted evaluation task object.
        """
        self._client.delete(f"evaluationTasks/{evaluation_task_id}")