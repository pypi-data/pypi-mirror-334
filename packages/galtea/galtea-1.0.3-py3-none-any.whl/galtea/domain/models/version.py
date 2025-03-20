from ...utils.from_camel_case_base_model import FromCamelCaseBaseModel

class VersionBaseOptionalProps(FromCamelCaseBaseModel):
    dataset_description: str | None = None
    dataset_uri: str | None = None
    description: str | None = None
    endpoint: str | None = None
    foundational_model: str | None = None
    guardrails: str | None = None
    provider: str | None = None
    system_prompt: str | None = None

class VersionBase(VersionBaseOptionalProps):
    name: str
    product_id: str

class Version(VersionBase):
    id: str
    created_at: str
    deleted_at: str | None = None