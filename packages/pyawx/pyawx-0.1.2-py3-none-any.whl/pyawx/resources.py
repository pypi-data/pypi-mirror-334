"""Defines classes for managing API resources.

It provides a `Resource` class to encapsulate common functionality and
specialized resource classes for specific API endpoints.

Features:

- Unified interface for CRUD operations (`fetch`, `create`, `update`, `delete`).
- Utilizes the `pyawx.HTTP` client for API communication.
- Leverages Pydantic models for resource validation and serialization.

Warnings:

- The API endpoints must match the `resource` name provided in the AWX API
  reference.
"""

from pydantic import BaseModel

from .http import HTTP
from .models import JobTemplateModel, WorkflowJobTemplateModel


class Resource:
    """Represents a base resource for interacting with the API.

    The `Resource` is used as a base for interacting with API resources,
    providing common methods to fetch, create, update, and delete resources. It
    uses an HTTP client to send requests to the API.

    Attributes:
        `_http` (`HTTP`): The HTTP client used to send requests.
        `resource` (`str`): The name of the resource being managed.
            This name should be the API endpoint name.
        `model` (`type[BaseModel] | None`): The optional Pydantic model class
            that defines the structure of the resource data.
    """

    def __init__(
        self,
        http: HTTP,
        resource: str,
        model: type[BaseModel] | None = None,
    ) -> None:
        """Initializes the Resource with the HTTP client, resource name, and
        optional model.

        Args:
            `_http` (`HTTP`): The HTTP client used to send requests
                to the API.
            `resource` (`str`): The resource name.
                Notice that this name should be the API endpoint name.
            `model` (`type[BaseModel] | None`): The optional Pydantic model class
                for the resource data.
        """
        self._http: HTTP = http
        self.resource: str = resource
        self.model: type[BaseModel] | None = model

    def _get_id_by_name(self, resource_name: str) -> str:
        """Fetches the resource ID by its name.

        Args:
            `resource_name` (`str`): The name of the resource.

        Returns:
            `str`: The ID of the resource.

        Raises:
            `ValueError`: If the resource with the given name is not found.
        """
        resources: dict = self._http.get(self.resource)

        for resource in resources["results"]:
            if resource["name"] == resource_name:
                return resource["id"]

        raise ValueError(f"Resource with name '{resource_name}' not found.")

    def _names_to_ids(self, data: dict) -> dict:
        """Converts resource names to IDs for specified fields in the data
        dictionary.

        Args:
            `data` (`dict`): The data dictionary containing resource names.

        Returns:
            `dict`: The data dictionary with resource names converted to IDs.
        """
        resource_map: dict[str, str] = {
            "inventory": "inventories",
            "project": "projects",
            "webhook_credential": "webhook_credentials",
            "organization": "organizations",
        }

        for field, resource_name in resource_map.items():
            if field in data and isinstance(data[field], str):
                resource_id: str = Resource(self._http, resource_name)._get_id_by_name(
                    data[field]
                )
                data[field] = resource_id

        return data

    def fetch(self, resource_name: str) -> dict:
        """Fetches a resource by its name.

        Args:
            `resource_name` (`str`): The name of the resource to fetch.

        Returns:
            `dict`: The resource data as a dictionary.

        Examples:
            >>> resource.fetch("My Job Template")
            {'id': '30', 'name': 'My Job Template', ...}
        """
        resource_id: str = self._get_id_by_name(resource_name)
        return self._http.get(self.resource, resource_id)

    def create(self, payload: BaseModel) -> dict:
        """Creates a new resource with the provided payload.

        Args:
            `payload` (`BaseModel`): The Pydantic model instance containing the
                data to create the resource. This requires the `model` attribute
                to be set.

        Returns:
            `dict`: The response data after creating the resource.

        Raises:
            `ValueError`: If the `model` attribute is not set.

        Examples:
            >>> new_job_template = JobTemplateModel(name="My New Job")
            >>> resource.create(new_job_template)
            {'id': '31', 'name': 'My New Job', ...}
        """
        if not self.model:
            raise ValueError("Model is not set for this resource.")

        data: dict = self._names_to_ids(payload.model_dump())
        return self._http.post(self.resource, data)

    def update(self, resource_name: str, payload: BaseModel) -> dict:
        """Updates an existing resource with the given name and payload.

        Args:
            `resource_name` (`str`): The name of the resource to update.
            `payload` (`BaseModel`): The Pydantic model instance containing the
                updated data. This requires the `model` attribute to be set.

        Returns:
            `dict`: The response data after updating the resource.

        Raises:
            `ValueError`: If the `model` attribute is not set.

        Examples:
            >>> updated_job_template = JobTemplateModel(name="Updated Job Template")
            >>> resource.update("My Job Template", updated_job_template)
            {'id': '31', 'name': 'Updated Job Template', ...}
        """
        if not self.model:
            raise ValueError("Model is not set for this resource.")

        resource_id: str = self._get_id_by_name(resource_name)
        data: dict = self._names_to_ids(payload.model_dump())
        return self._http.patch(self.resource, resource_id, data)

    def delete(self, resource_name: str) -> None:
        """Deletes a resource by its name.

        Args:
            `resource_name` (`str`): The name of the resource to delete.

        Examples:
            >>> resource.delete("My Job Template")
        """
        resource_id: str = self._get_id_by_name(resource_name)
        self._http.delete(self.resource, resource_id)


class JobTemplateResource(Resource):
    """Represents a resource for interacting with job templates in the API.

    Attributes:
        `_http` (`HTTP`): The HTTP client used to send requests to the API.
        `resource` (`str`): The resource name.
        `model` (`type[JobTemplateModel]`): The Pydantic model class for the job
            template data.
    """

    def __init__(self, http_client: HTTP) -> None:
        super().__init__(http_client, "job_templates", JobTemplateModel)

    # TODO: Add `launch` method to launch a job template.


class WorkflowJobTemplateResource(Resource):
    """Represents a resource for interacting with workflow job templates in the API.

    Attributes:
        `_http` (`HTTP`): The HTTP client used to send requests to the API.
        `resource` (`str`): The resource name.
        `model` (`type[WorkflowJobTemplateModel]`): The Pydantic model class for
            the workflow job template data.
    """

    def __init__(self, http_client: HTTP) -> None:
        super().__init__(
            http_client, "workflow_job_templates", WorkflowJobTemplateModel
        )

    # TODO: Add `launch` method to launch a workflow job template.
