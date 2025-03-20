from galtea.application.services.evaluation_task_service import EvaluationTaskService
from galtea.application.services.metric_type_service import MetricTypeService
from .application.services.product_service import ProductService
from .application.services.test_service import TestService
from .application.services.version_service import VersionService
from .application.services.evaluation_service import EvaluationService
from .infrastructure.clients.http_client import Client
from termcolor import colored

class Galtea:
  def __init__(self, api_key: str):
    self.__client = Client(api_key)
    self.products = ProductService(self.__client)
    self.tests = TestService(self.__client)
    self.versions = VersionService(self.__client)
    self.metrics = MetricTypeService(self.__client)
    self.evaluations = EvaluationService(self.__client)
    self.evaluation_tasks = EvaluationTaskService(self.__client)