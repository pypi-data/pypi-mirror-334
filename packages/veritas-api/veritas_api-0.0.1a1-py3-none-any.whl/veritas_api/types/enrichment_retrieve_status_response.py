# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["EnrichmentRetrieveStatusResponse", "Candidate"]


class Candidate(BaseModel):
    email: Optional[str] = None

    linkedin_id: Optional[str] = None

    location: Optional[str] = None

    name: Optional[str] = None

    phone: Optional[str] = None

    role: Optional[Literal["rn", "lpn", "cna", "allied_health", "other"]] = None

    specialty: Optional[str] = None


class EnrichmentRetrieveStatusResponse(BaseModel):
    id: Optional[str] = None

    candidates: Optional[List[Candidate]] = None

    status: Optional[Literal["pending", "processing", "completed", "failed"]] = None
