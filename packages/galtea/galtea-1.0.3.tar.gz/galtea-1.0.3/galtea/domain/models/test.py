from datetime import datetime
from enum import Enum

from ...utils.from_camel_case_base_model import FromCamelCaseBaseModel

class TestBase(FromCamelCaseBaseModel):
    name: str
    type: str
    product_id: str
    ground_truth_uri: str | None = None
    uri: str | None = None

class Test(TestBase):
    id: str
    created_at: datetime | None = None
    deleted_at: datetime | None = None