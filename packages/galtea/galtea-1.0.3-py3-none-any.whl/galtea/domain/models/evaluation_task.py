from ...utils.from_camel_case_base_model import FromCamelCaseBaseModel

class EvaluationTaskBase(FromCamelCaseBaseModel):
  evaluation_id: str
  input: str
  actual_output: str
  expected_output: str | None
  context: str | None

class EvaluationTask(EvaluationTaskBase):
  id: str
  metric_type_id: str
  user_id: str | None = None
  status: str
  score: float | None = None
  reason: str | None = None
  error: str | None = None
  created_at: str | None
  deleted_at: str | None = None
  evaluated_at: str | None = None