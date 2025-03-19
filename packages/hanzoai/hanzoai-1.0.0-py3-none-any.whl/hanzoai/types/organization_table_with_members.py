# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from .._models import BaseModel
from .budget_table import BudgetTable
from .lite_llm_team_table import LiteLlmTeamTable
from .organization_membership_table import OrganizationMembershipTable

__all__ = ["OrganizationTableWithMembers"]


class OrganizationTableWithMembers(BaseModel):
    budget_id: str

    created_at: datetime

    created_by: str

    models: List[str]

    updated_at: datetime

    updated_by: str

    litellm_budget_table: Optional[BudgetTable] = None
    """Represents user-controllable params for a LiteLLM_BudgetTable record"""

    members: Optional[List[OrganizationMembershipTable]] = None

    metadata: Optional[object] = None

    organization_alias: Optional[str] = None

    organization_id: Optional[str] = None

    spend: Optional[float] = None

    teams: Optional[List[LiteLlmTeamTable]] = None
