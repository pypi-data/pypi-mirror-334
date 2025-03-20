from .curated_incident import (
    list_incidents as _list_incidents,
    list_incidents_async as _list_incidents_async,
    create_new_incident as _create_new_incident,
    create_new_incident_async as _create_new_incident_async,
    update_incident as _update_incident,
    update_incident_async as _update_incident_async,
)
from ..models.default_error import DefaultError
from ..models.list_incidents import ListIncidents
from typing import cast
from ..models.create_new_incident_request import CreateNewIncidentRequest
from ..models.create_new_incident_response import CreateNewIncidentResponse
from ..models.update_incident_request import UpdateIncidentRequest
from ..models.update_incident_response import UpdateIncidentResponse
from .curated_search_incident import (
    search_incidents as _search_incidents,
    search_incidents_async as _search_incidents_async,
)
from ..models.search_incidents import SearchIncidents
from .curated_incident_task import (
    list_incident_tasks as _list_incident_tasks,
    list_incident_tasks_async as _list_incident_tasks_async,
    create_incident_task as _create_incident_task,
    create_incident_task_async as _create_incident_task_async,
    get_incident_task as _get_incident_task,
    get_incident_task_async as _get_incident_task_async,
    update_incident_task as _update_incident_task,
    update_incident_task_async as _update_incident_task_async,
)
from ..models.list_incident_tasks import ListIncidentTasks
from ..models.create_incident_task_request import CreateIncidentTaskRequest
from ..models.create_incident_task_response import CreateIncidentTaskResponse
from ..models.get_incident_task_response import GetIncidentTaskResponse
from ..models.update_incident_task_request import UpdateIncidentTaskRequest
from ..models.update_incident_task_response import UpdateIncidentTaskResponse
from .curated_search_user import (
    search_users as _search_users,
    search_users_async as _search_users_async,
)
from ..models.search_users import SearchUsers
from .attachment_download import (
    download_attachment as _download_attachment,
    download_attachment_async as _download_attachment_async,
)
from ..types import File, FileJsonType
from io import BytesIO
from .attachment_delete import (
    delete_attachment as _delete_attachment,
    delete_attachment_async as _delete_attachment_async,
)
from .attachment_getbyid import (
    get_attachment as _get_attachment,
    get_attachment_async as _get_attachment_async,
)
from ..models.get_attachment_response import GetAttachmentResponse
from .add_attachment import (
    add_attachment as _add_attachment,
    add_attachment_async as _add_attachment_async,
)
from ..models.add_attachment_body import AddAttachmentBody
from ..models.add_attachment_response import AddAttachmentResponse
from .attachment_get import (
    list_all_attachment as _list_all_attachment,
    list_all_attachment_async as _list_all_attachment_async,
)
from ..models.list_all_attachment import ListAllAttachment

from pydantic import Field
from typing import Any, Optional, Union

from ..client import Client
import httpx


class ServicenowServicenow:
    def __init__(self, *, instance_id: str, client: httpx.Client):
        base_url = str(client.base_url).rstrip("/")
        new_headers = {
            k: v for k, v in client.headers.items() if k not in ["content-type"]
        }
        new_client = httpx.Client(
            base_url=base_url + f"/elements_/v3/element/instances/{instance_id}",
            headers=new_headers,
            timeout=100,
        )
        new_client_async = httpx.AsyncClient(
            base_url=base_url + f"/elements_/v3/element/instances/{instance_id}",
            headers=new_headers,
            timeout=100,
        )
        self.client = (
            Client(
                base_url="",  # this will be overridden by the base_url in the Client constructor
            )
            .set_httpx_client(new_client)
            .set_async_httpx_client(new_client_async)
        )

    def list_incidents(
        self,
        *,
        fields: Optional[str] = Field(alias="fields", default=None),
        next_page: Optional[str] = Field(alias="nextPage", default=None),
        page_size: Optional[int] = Field(alias="pageSize", default=None),
        where: Optional[str] = Field(alias="where", default=None),
    ) -> Optional[Union[DefaultError, list["ListIncidents"]]]:
        return _list_incidents(
            client=self.client,
            fields=fields,
            next_page=next_page,
            page_size=page_size,
            where=where,
        )

    async def list_incidents_async(
        self,
        *,
        fields: Optional[str] = Field(alias="fields", default=None),
        next_page: Optional[str] = Field(alias="nextPage", default=None),
        page_size: Optional[int] = Field(alias="pageSize", default=None),
        where: Optional[str] = Field(alias="where", default=None),
    ) -> Optional[Union[DefaultError, list["ListIncidents"]]]:
        return await _list_incidents_async(
            client=self.client,
            fields=fields,
            next_page=next_page,
            page_size=page_size,
            where=where,
        )

    def create_new_incident(
        self,
        *,
        body: CreateNewIncidentRequest,
    ) -> Optional[Union[CreateNewIncidentResponse, DefaultError]]:
        return _create_new_incident(
            client=self.client,
            body=body,
        )

    async def create_new_incident_async(
        self,
        *,
        body: CreateNewIncidentRequest,
    ) -> Optional[Union[CreateNewIncidentResponse, DefaultError]]:
        return await _create_new_incident_async(
            client=self.client,
            body=body,
        )

    def update_incident(
        self,
        incident_id: str,
        incident_id_lookup: Any,
        *,
        body: UpdateIncidentRequest,
    ) -> Optional[Union[DefaultError, UpdateIncidentResponse]]:
        return _update_incident(
            client=self.client,
            incident_id=incident_id,
            incident_id_lookup=incident_id_lookup,
            body=body,
        )

    async def update_incident_async(
        self,
        incident_id: str,
        incident_id_lookup: Any,
        *,
        body: UpdateIncidentRequest,
    ) -> Optional[Union[DefaultError, UpdateIncidentResponse]]:
        return await _update_incident_async(
            client=self.client,
            incident_id=incident_id,
            incident_id_lookup=incident_id_lookup,
            body=body,
        )

    def search_incidents(
        self,
        *,
        number: str = Field(alias="number"),
        fields: Optional[str] = Field(alias="fields", default=None),
        next_page: Optional[str] = Field(alias="nextPage", default=None),
        page_size: Optional[int] = Field(alias="pageSize", default=None),
        where: Optional[str] = Field(alias="where", default=None),
    ) -> Optional[Union[DefaultError, list["SearchIncidents"]]]:
        return _search_incidents(
            client=self.client,
            number=number,
            fields=fields,
            next_page=next_page,
            page_size=page_size,
            where=where,
        )

    async def search_incidents_async(
        self,
        *,
        number: str = Field(alias="number"),
        fields: Optional[str] = Field(alias="fields", default=None),
        next_page: Optional[str] = Field(alias="nextPage", default=None),
        page_size: Optional[int] = Field(alias="pageSize", default=None),
        where: Optional[str] = Field(alias="where", default=None),
    ) -> Optional[Union[DefaultError, list["SearchIncidents"]]]:
        return await _search_incidents_async(
            client=self.client,
            number=number,
            fields=fields,
            next_page=next_page,
            page_size=page_size,
            where=where,
        )

    def list_incident_tasks(
        self,
        *,
        fields: Optional[str] = Field(alias="fields", default=None),
        next_page: Optional[str] = Field(alias="nextPage", default=None),
        page_size: Optional[int] = Field(alias="pageSize", default=None),
        where: Optional[str] = Field(alias="where", default=None),
    ) -> Optional[Union[DefaultError, list["ListIncidentTasks"]]]:
        return _list_incident_tasks(
            client=self.client,
            fields=fields,
            next_page=next_page,
            page_size=page_size,
            where=where,
        )

    async def list_incident_tasks_async(
        self,
        *,
        fields: Optional[str] = Field(alias="fields", default=None),
        next_page: Optional[str] = Field(alias="nextPage", default=None),
        page_size: Optional[int] = Field(alias="pageSize", default=None),
        where: Optional[str] = Field(alias="where", default=None),
    ) -> Optional[Union[DefaultError, list["ListIncidentTasks"]]]:
        return await _list_incident_tasks_async(
            client=self.client,
            fields=fields,
            next_page=next_page,
            page_size=page_size,
            where=where,
        )

    def create_incident_task(
        self,
        *,
        body: CreateIncidentTaskRequest,
    ) -> Optional[Union[CreateIncidentTaskResponse, DefaultError]]:
        return _create_incident_task(
            client=self.client,
            body=body,
        )

    async def create_incident_task_async(
        self,
        *,
        body: CreateIncidentTaskRequest,
    ) -> Optional[Union[CreateIncidentTaskResponse, DefaultError]]:
        return await _create_incident_task_async(
            client=self.client,
            body=body,
        )

    def get_incident_task(
        self,
        curated_incident_task_id: str,
        curated_incident_task_id_lookup: Any,
    ) -> Optional[Union[DefaultError, GetIncidentTaskResponse]]:
        return _get_incident_task(
            client=self.client,
            curated_incident_task_id=curated_incident_task_id,
            curated_incident_task_id_lookup=curated_incident_task_id_lookup,
        )

    async def get_incident_task_async(
        self,
        curated_incident_task_id: str,
        curated_incident_task_id_lookup: Any,
    ) -> Optional[Union[DefaultError, GetIncidentTaskResponse]]:
        return await _get_incident_task_async(
            client=self.client,
            curated_incident_task_id=curated_incident_task_id,
            curated_incident_task_id_lookup=curated_incident_task_id_lookup,
        )

    def update_incident_task(
        self,
        curated_incident_task_id: str,
        curated_incident_task_id_lookup: Any,
        *,
        body: UpdateIncidentTaskRequest,
    ) -> Optional[Union[DefaultError, UpdateIncidentTaskResponse]]:
        return _update_incident_task(
            client=self.client,
            curated_incident_task_id=curated_incident_task_id,
            curated_incident_task_id_lookup=curated_incident_task_id_lookup,
            body=body,
        )

    async def update_incident_task_async(
        self,
        curated_incident_task_id: str,
        curated_incident_task_id_lookup: Any,
        *,
        body: UpdateIncidentTaskRequest,
    ) -> Optional[Union[DefaultError, UpdateIncidentTaskResponse]]:
        return await _update_incident_task_async(
            client=self.client,
            curated_incident_task_id=curated_incident_task_id,
            curated_incident_task_id_lookup=curated_incident_task_id_lookup,
            body=body,
        )

    def search_users(
        self,
        *,
        page: Optional[str] = Field(alias="Page", default=None),
        email: Optional[str] = Field(alias="email", default=None),
        fields: Optional[str] = Field(alias="fields", default=None),
        next_page: Optional[str] = Field(alias="nextPage", default=None),
        page_size: Optional[int] = Field(alias="pageSize", default=None),
        user_name: Optional[str] = Field(alias="user_name", default=None),
        where: Optional[str] = Field(alias="where", default=None),
    ) -> Optional[Union[DefaultError, list["SearchUsers"]]]:
        return _search_users(
            client=self.client,
            page=page,
            email=email,
            fields=fields,
            next_page=next_page,
            page_size=page_size,
            user_name=user_name,
            where=where,
        )

    async def search_users_async(
        self,
        *,
        page: Optional[str] = Field(alias="Page", default=None),
        email: Optional[str] = Field(alias="email", default=None),
        fields: Optional[str] = Field(alias="fields", default=None),
        next_page: Optional[str] = Field(alias="nextPage", default=None),
        page_size: Optional[int] = Field(alias="pageSize", default=None),
        user_name: Optional[str] = Field(alias="user_name", default=None),
        where: Optional[str] = Field(alias="where", default=None),
    ) -> Optional[Union[DefaultError, list["SearchUsers"]]]:
        return await _search_users_async(
            client=self.client,
            page=page,
            email=email,
            fields=fields,
            next_page=next_page,
            page_size=page_size,
            user_name=user_name,
            where=where,
        )

    def download_attachment(
        self,
        id: str,
        id_lookup: Any,
    ) -> Optional[Union[DefaultError, File]]:
        return _download_attachment(
            client=self.client,
            id=id,
            id_lookup=id_lookup,
        )

    async def download_attachment_async(
        self,
        id: str,
        id_lookup: Any,
    ) -> Optional[Union[DefaultError, File]]:
        return await _download_attachment_async(
            client=self.client,
            id=id,
            id_lookup=id_lookup,
        )

    def delete_attachment(
        self,
        id: str,
        id_lookup: Any,
    ) -> Optional[Union[Any, DefaultError]]:
        return _delete_attachment(
            client=self.client,
            id=id,
            id_lookup=id_lookup,
        )

    async def delete_attachment_async(
        self,
        id: str,
        id_lookup: Any,
    ) -> Optional[Union[Any, DefaultError]]:
        return await _delete_attachment_async(
            client=self.client,
            id=id,
            id_lookup=id_lookup,
        )

    def get_attachment(
        self,
        id: str,
        id_lookup: Any,
    ) -> Optional[Union[DefaultError, GetAttachmentResponse]]:
        return _get_attachment(
            client=self.client,
            id=id,
            id_lookup=id_lookup,
        )

    async def get_attachment_async(
        self,
        id: str,
        id_lookup: Any,
    ) -> Optional[Union[DefaultError, GetAttachmentResponse]]:
        return await _get_attachment_async(
            client=self.client,
            id=id,
            id_lookup=id_lookup,
        )

    def add_attachment(
        self,
        *,
        body: AddAttachmentBody,
        table_name: Optional[str] = Field(alias="table_name", default=None),
        table_name_lookup: Any,
        table_sys_id: Optional[str] = Field(alias="table_sys_id", default=None),
        table_sys_id_lookup: Any,
    ) -> Optional[Union[AddAttachmentResponse, DefaultError]]:
        return _add_attachment(
            client=self.client,
            body=body,
            table_name=table_name,
            table_name_lookup=table_name_lookup,
            table_sys_id=table_sys_id,
            table_sys_id_lookup=table_sys_id_lookup,
        )

    async def add_attachment_async(
        self,
        *,
        body: AddAttachmentBody,
        table_name: Optional[str] = Field(alias="table_name", default=None),
        table_name_lookup: Any,
        table_sys_id: Optional[str] = Field(alias="table_sys_id", default=None),
        table_sys_id_lookup: Any,
    ) -> Optional[Union[AddAttachmentResponse, DefaultError]]:
        return await _add_attachment_async(
            client=self.client,
            body=body,
            table_name=table_name,
            table_name_lookup=table_name_lookup,
            table_sys_id=table_sys_id,
            table_sys_id_lookup=table_sys_id_lookup,
        )

    def list_all_attachment(
        self,
        *,
        fields: Optional[str] = Field(alias="fields", default=None),
        next_page: Optional[str] = Field(alias="nextPage", default=None),
        page_size: Optional[int] = Field(alias="pageSize", default=None),
        where: Optional[str] = Field(alias="where", default=None),
    ) -> Optional[Union[DefaultError, list["ListAllAttachment"]]]:
        return _list_all_attachment(
            client=self.client,
            fields=fields,
            next_page=next_page,
            page_size=page_size,
            where=where,
        )

    async def list_all_attachment_async(
        self,
        *,
        fields: Optional[str] = Field(alias="fields", default=None),
        next_page: Optional[str] = Field(alias="nextPage", default=None),
        page_size: Optional[int] = Field(alias="pageSize", default=None),
        where: Optional[str] = Field(alias="where", default=None),
    ) -> Optional[Union[DefaultError, list["ListAllAttachment"]]]:
        return await _list_all_attachment_async(
            client=self.client,
            fields=fields,
            next_page=next_page,
            page_size=page_size,
            where=where,
        )
