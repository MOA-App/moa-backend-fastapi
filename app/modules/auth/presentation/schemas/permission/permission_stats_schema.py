from pydantic import BaseModel
from typing import List

class PermissionStats(BaseModel):
    total_permissions: int
    total_resources: int
    resources: List[str]
    most_used_permissions: List[str]
