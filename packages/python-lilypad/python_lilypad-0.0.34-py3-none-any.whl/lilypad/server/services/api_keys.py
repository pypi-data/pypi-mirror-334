"""The `APIKeyService` class for api_keys."""

from collections.abc import Sequence
from typing import Any
from uuid import UUID

from ..models import APIKeyTable
from ..schemas import APIKeyCreate
from .base_organization import BaseOrganizationService


class APIKeyService(BaseOrganizationService[APIKeyTable, APIKeyCreate]):
    """The service class for api_keys."""

    table: type[APIKeyTable] = APIKeyTable
    create_model: type[APIKeyCreate] = APIKeyCreate

    def find_keys_by_user_and_project(
        self, project_uuid: UUID
    ) -> Sequence[APIKeyTable]:
        """Find api key by user and project"""
        return self.find_all_records(project_uuid=project_uuid)

    def create_record(self, data: APIKeyCreate, **kwargs: Any) -> APIKeyTable:
        """Create a new api key"""
        return super().create_record(
            data,
            user_uuid=self.user.uuid,
            **kwargs,
        )
