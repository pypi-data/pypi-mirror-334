from ...utils.from_camel_case_base_model import FromCamelCaseBaseModel

class MetricTypeBase(FromCamelCaseBaseModel):
    name: str
    criteria: str | None = None
    evaluation_steps: list[str] | None = None

class MetricType(MetricTypeBase):
    id: str
    organization_id: str
    created_at: str
    deleted_at: str | None = None