from .folders import (
    create_folder as _create_folder,
    create_folder_async as _create_folder_async,
    delete_folder as _delete_folder,
    delete_folder_async as _delete_folder_async,
)
from ..models.create_folder_request import CreateFolderRequest
from ..models.create_folder_response import CreateFolderResponse
from ..models.default_error import DefaultError
from typing import cast
from .add_shared_link_to_file import (
    add_shared_linktoa_file as _add_shared_linktoa_file,
    add_shared_linktoa_file_async as _add_shared_linktoa_file_async,
)
from ..models.add_shared_linktoa_file_request import AddSharedLinktoaFileRequest
from ..models.add_shared_linktoa_file_response import AddSharedLinktoaFileResponse
from .upload_file import (
    upload_file as _upload_file,
    upload_file_async as _upload_file_async,
)
from ..models.upload_file_body import UploadFileBody
from ..models.upload_file_response import UploadFileResponse
from .files_content import (
    download_file as _download_file,
    download_file_async as _download_file_async,
)
from ..types import File, FileJsonType
from io import BytesIO
from .upload_file_version import (
    upload_file_version as _upload_file_version,
    upload_file_version_async as _upload_file_version_async,
)
from ..models.upload_file_version_body import UploadFileVersionBody
from ..models.upload_file_version_response import UploadFileVersionResponse
from .sign_requests_resend import (
    resend_sign_request as _resend_sign_request,
    resend_sign_request_async as _resend_sign_request_async,
)
from .folder_items import (
    get_folder_items as _get_folder_items,
    get_folder_items_async as _get_folder_items_async,
)
from ..models.get_folder_items import GetFolderItems
from .copy_folder import (
    copy_folder as _copy_folder,
    copy_folder_async as _copy_folder_async,
)
from ..models.copy_folder_request import CopyFolderRequest
from ..models.copy_folder_response import CopyFolderResponse
from .files import (
    get_file_info as _get_file_info,
    get_file_info_async as _get_file_info_async,
    delete_file as _delete_file,
    delete_file_async as _delete_file_async,
)
from ..models.get_file_info_response import GetFileInfoResponse
from .copy_file import (
    copy_file as _copy_file,
    copy_file_async as _copy_file_async,
)
from ..models.copy_file_request import CopyFileRequest
from ..models.copy_file_response import CopyFileResponse
from .search_for_content import (
    search as _search,
    search_async as _search_async,
)
from ..models.search import Search
from dateutil.parser import isoparse
import datetime
from .create_sign_request import (
    create_sign_request as _create_sign_request,
    create_sign_request_async as _create_sign_request_async,
)
from ..models.create_sign_request_request import CreateSignRequestRequest
from ..models.create_sign_request_response import CreateSignRequestResponse
from .cancel_sign_request import (
    cancel_sign_request as _cancel_sign_request,
    cancel_sign_request_async as _cancel_sign_request_async,
)
from ..models.cancel_sign_request_response import CancelSignRequestResponse
from .sign_requests import (
    list_sign_request as _list_sign_request,
    list_sign_request_async as _list_sign_request_async,
)
from ..models.list_sign_request import ListSignRequest
from .add_shared_link_to_folder import (
    add_shared_linktoa_folder as _add_shared_linktoa_folder,
    add_shared_linktoa_folder_async as _add_shared_linktoa_folder_async,
)
from ..models.add_shared_linktoa_folder_request import AddSharedLinktoaFolderRequest
from ..models.add_shared_linktoa_folder_response import AddSharedLinktoaFolderResponse

from pydantic import Field
from typing import Any, Optional, Union

from ..client import Client
import httpx


class BoxBox:
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

    def create_folder(
        self,
        *,
        body: CreateFolderRequest,
    ) -> Optional[Union[CreateFolderResponse, DefaultError]]:
        return _create_folder(
            client=self.client,
            body=body,
        )

    async def create_folder_async(
        self,
        *,
        body: CreateFolderRequest,
    ) -> Optional[Union[CreateFolderResponse, DefaultError]]:
        return await _create_folder_async(
            client=self.client,
            body=body,
        )

    def delete_folder(
        self,
        folders_id: str,
        folders_id_lookup: Any,
    ) -> Optional[Union[Any, DefaultError]]:
        return _delete_folder(
            client=self.client,
            folders_id=folders_id,
            folders_id_lookup=folders_id_lookup,
        )

    async def delete_folder_async(
        self,
        folders_id: str,
        folders_id_lookup: Any,
    ) -> Optional[Union[Any, DefaultError]]:
        return await _delete_folder_async(
            client=self.client,
            folders_id=folders_id,
            folders_id_lookup=folders_id_lookup,
        )

    def add_shared_linktoa_file(
        self,
        file_id: str,
        file_id_lookup: Any,
        *,
        body: AddSharedLinktoaFileRequest,
    ) -> Optional[Union[AddSharedLinktoaFileResponse, DefaultError]]:
        return _add_shared_linktoa_file(
            client=self.client,
            file_id=file_id,
            file_id_lookup=file_id_lookup,
            body=body,
        )

    async def add_shared_linktoa_file_async(
        self,
        file_id: str,
        file_id_lookup: Any,
        *,
        body: AddSharedLinktoaFileRequest,
    ) -> Optional[Union[AddSharedLinktoaFileResponse, DefaultError]]:
        return await _add_shared_linktoa_file_async(
            client=self.client,
            file_id=file_id,
            file_id_lookup=file_id_lookup,
            body=body,
        )

    def upload_file(
        self,
        *,
        body: UploadFileBody,
        fields: Optional[str] = Field(alias="fields", default=None),
        elements_vendor_headers: Optional[str] = Field(
            alias="elements-vendor-headers", default=None
        ),
    ) -> Optional[Union[DefaultError, UploadFileResponse]]:
        return _upload_file(
            client=self.client,
            body=body,
            fields=fields,
            elements_vendor_headers=elements_vendor_headers,
        )

    async def upload_file_async(
        self,
        *,
        body: UploadFileBody,
        fields: Optional[str] = Field(alias="fields", default=None),
        elements_vendor_headers: Optional[str] = Field(
            alias="elements-vendor-headers", default=None
        ),
    ) -> Optional[Union[DefaultError, UploadFileResponse]]:
        return await _upload_file_async(
            client=self.client,
            body=body,
            fields=fields,
            elements_vendor_headers=elements_vendor_headers,
        )

    def download_file(
        self,
        file_id: str,
        file_id_lookup: Any,
    ) -> Optional[Union[DefaultError, File]]:
        return _download_file(
            client=self.client,
            file_id=file_id,
            file_id_lookup=file_id_lookup,
        )

    async def download_file_async(
        self,
        file_id: str,
        file_id_lookup: Any,
    ) -> Optional[Union[DefaultError, File]]:
        return await _download_file_async(
            client=self.client,
            file_id=file_id,
            file_id_lookup=file_id_lookup,
        )

    def upload_file_version(
        self,
        file_id: str,
        file_id_lookup: Any,
        *,
        body: UploadFileVersionBody,
        fields: Optional[str] = Field(alias="fields", default=None),
        elements_vendor_headers: Optional[str] = Field(
            alias="elements-vendor-headers", default=None
        ),
    ) -> Optional[Union[DefaultError, UploadFileVersionResponse]]:
        return _upload_file_version(
            client=self.client,
            file_id=file_id,
            file_id_lookup=file_id_lookup,
            body=body,
            fields=fields,
            elements_vendor_headers=elements_vendor_headers,
        )

    async def upload_file_version_async(
        self,
        file_id: str,
        file_id_lookup: Any,
        *,
        body: UploadFileVersionBody,
        fields: Optional[str] = Field(alias="fields", default=None),
        elements_vendor_headers: Optional[str] = Field(
            alias="elements-vendor-headers", default=None
        ),
    ) -> Optional[Union[DefaultError, UploadFileVersionResponse]]:
        return await _upload_file_version_async(
            client=self.client,
            file_id=file_id,
            file_id_lookup=file_id_lookup,
            body=body,
            fields=fields,
            elements_vendor_headers=elements_vendor_headers,
        )

    def resend_sign_request(
        self,
        sign_request_id: str,
        sign_request_id_lookup: Any,
    ) -> Optional[Union[Any, DefaultError]]:
        return _resend_sign_request(
            client=self.client,
            sign_request_id=sign_request_id,
            sign_request_id_lookup=sign_request_id_lookup,
        )

    async def resend_sign_request_async(
        self,
        sign_request_id: str,
        sign_request_id_lookup: Any,
    ) -> Optional[Union[Any, DefaultError]]:
        return await _resend_sign_request_async(
            client=self.client,
            sign_request_id=sign_request_id,
            sign_request_id_lookup=sign_request_id_lookup,
        )

    def get_folder_items(
        self,
        folder_id: str,
        folder_id_lookup: Any,
        *,
        fields: Optional[str] = Field(alias="fields", default=None),
        next_page: Optional[str] = Field(alias="nextPage", default=None),
        page_size: Optional[int] = Field(alias="pageSize", default=None),
        type_: Optional[str] = Field(alias="type", default="Files and Folders"),
        where: Optional[str] = Field(alias="where", default=None),
    ) -> Optional[Union[DefaultError, list["GetFolderItems"]]]:
        return _get_folder_items(
            client=self.client,
            folder_id=folder_id,
            folder_id_lookup=folder_id_lookup,
            fields=fields,
            next_page=next_page,
            page_size=page_size,
            type_=type_,
            where=where,
        )

    async def get_folder_items_async(
        self,
        folder_id: str,
        folder_id_lookup: Any,
        *,
        fields: Optional[str] = Field(alias="fields", default=None),
        next_page: Optional[str] = Field(alias="nextPage", default=None),
        page_size: Optional[int] = Field(alias="pageSize", default=None),
        type_: Optional[str] = Field(alias="type", default="Files and Folders"),
        where: Optional[str] = Field(alias="where", default=None),
    ) -> Optional[Union[DefaultError, list["GetFolderItems"]]]:
        return await _get_folder_items_async(
            client=self.client,
            folder_id=folder_id,
            folder_id_lookup=folder_id_lookup,
            fields=fields,
            next_page=next_page,
            page_size=page_size,
            type_=type_,
            where=where,
        )

    def copy_folder(
        self,
        folder_id: str,
        folder_id_lookup: Any,
        *,
        body: CopyFolderRequest,
    ) -> Optional[Union[CopyFolderResponse, DefaultError]]:
        return _copy_folder(
            client=self.client,
            folder_id=folder_id,
            folder_id_lookup=folder_id_lookup,
            body=body,
        )

    async def copy_folder_async(
        self,
        folder_id: str,
        folder_id_lookup: Any,
        *,
        body: CopyFolderRequest,
    ) -> Optional[Union[CopyFolderResponse, DefaultError]]:
        return await _copy_folder_async(
            client=self.client,
            folder_id=folder_id,
            folder_id_lookup=folder_id_lookup,
            body=body,
        )

    def get_file_info(
        self,
        files_id: str,
        files_id_lookup: Any,
        *,
        x_rep_hints: Optional[str] = Field(alias="x-rep-hints", default=None),
        elements_vendor_headers: Optional[str] = Field(
            alias="elements-vendor-headers", default=None
        ),
        if_none_match: Optional[str] = Field(alias="if-none-match", default=None),
    ) -> Optional[Union[DefaultError, GetFileInfoResponse]]:
        return _get_file_info(
            client=self.client,
            files_id=files_id,
            files_id_lookup=files_id_lookup,
            x_rep_hints=x_rep_hints,
            elements_vendor_headers=elements_vendor_headers,
            if_none_match=if_none_match,
        )

    async def get_file_info_async(
        self,
        files_id: str,
        files_id_lookup: Any,
        *,
        x_rep_hints: Optional[str] = Field(alias="x-rep-hints", default=None),
        elements_vendor_headers: Optional[str] = Field(
            alias="elements-vendor-headers", default=None
        ),
        if_none_match: Optional[str] = Field(alias="if-none-match", default=None),
    ) -> Optional[Union[DefaultError, GetFileInfoResponse]]:
        return await _get_file_info_async(
            client=self.client,
            files_id=files_id,
            files_id_lookup=files_id_lookup,
            x_rep_hints=x_rep_hints,
            elements_vendor_headers=elements_vendor_headers,
            if_none_match=if_none_match,
        )

    def delete_file(
        self,
        files_id: str,
        files_id_lookup: Any,
    ) -> Optional[Union[Any, DefaultError]]:
        return _delete_file(
            client=self.client,
            files_id=files_id,
            files_id_lookup=files_id_lookup,
        )

    async def delete_file_async(
        self,
        files_id: str,
        files_id_lookup: Any,
    ) -> Optional[Union[Any, DefaultError]]:
        return await _delete_file_async(
            client=self.client,
            files_id=files_id,
            files_id_lookup=files_id_lookup,
        )

    def copy_file(
        self,
        file_id: str,
        file_id_lookup: Any,
        *,
        body: CopyFileRequest,
    ) -> Optional[Union[CopyFileResponse, DefaultError]]:
        return _copy_file(
            client=self.client,
            file_id=file_id,
            file_id_lookup=file_id_lookup,
            body=body,
        )

    async def copy_file_async(
        self,
        file_id: str,
        file_id_lookup: Any,
        *,
        body: CopyFileRequest,
    ) -> Optional[Union[CopyFileResponse, DefaultError]]:
        return await _copy_file_async(
            client=self.client,
            file_id=file_id,
            file_id_lookup=file_id_lookup,
            body=body,
        )

    def search(
        self,
        *,
        query: str = Field(alias="query"),
        ancestor_folder_ids: Optional[str] = Field(
            alias="ancestor_folder_ids", default=None
        ),
        ancestor_folder_ids_lookup: Any,
        content_types: Optional[str] = Field(alias="content_types", default=None),
        created_at_range_end_date: Optional[datetime.datetime] = Field(
            alias="created_at_range_end_date", default=None
        ),
        created_at_range_start_date: Optional[datetime.datetime] = Field(
            alias="created_at_range_start_date", default=None
        ),
        direction: Optional[str] = Field(alias="direction", default=None),
        fields: Optional[str] = Field(alias="fields", default=None),
        file_extensions: Optional[str] = Field(alias="file_extensions", default=None),
        include_recent_shared_links: Optional[bool] = Field(
            alias="include_recent_shared_links", default=None
        ),
        mdfilters: Optional[str] = Field(alias="mdfilters", default=None),
        next_page: Optional[str] = Field(alias="nextPage", default=None),
        owner_user_ids: Optional[str] = Field(alias="owner_user_ids", default=None),
        page_size: Optional[int] = Field(alias="pageSize", default=None),
        scope: Optional[str] = Field(alias="scope", default=None),
        sort: Optional[str] = Field(alias="sort", default=None),
        trash_content: Optional[str] = Field(alias="trash_content", default=None),
        type_: Optional[str] = Field(alias="type", default=None),
        updated_at_range_end_date: Optional[datetime.datetime] = Field(
            alias="updated_at_range_end_date", default=None
        ),
        updated_at_range_start_date: Optional[datetime.datetime] = Field(
            alias="updated_at_range_start_date", default=None
        ),
        where: Optional[str] = Field(alias="where", default=None),
    ) -> Optional[Union[DefaultError, list["Search"]]]:
        return _search(
            client=self.client,
            query=query,
            ancestor_folder_ids=ancestor_folder_ids,
            ancestor_folder_ids_lookup=ancestor_folder_ids_lookup,
            content_types=content_types,
            created_at_range_end_date=created_at_range_end_date,
            created_at_range_start_date=created_at_range_start_date,
            direction=direction,
            fields=fields,
            file_extensions=file_extensions,
            include_recent_shared_links=include_recent_shared_links,
            mdfilters=mdfilters,
            next_page=next_page,
            owner_user_ids=owner_user_ids,
            page_size=page_size,
            scope=scope,
            sort=sort,
            trash_content=trash_content,
            type_=type_,
            updated_at_range_end_date=updated_at_range_end_date,
            updated_at_range_start_date=updated_at_range_start_date,
            where=where,
        )

    async def search_async(
        self,
        *,
        query: str = Field(alias="query"),
        ancestor_folder_ids: Optional[str] = Field(
            alias="ancestor_folder_ids", default=None
        ),
        ancestor_folder_ids_lookup: Any,
        content_types: Optional[str] = Field(alias="content_types", default=None),
        created_at_range_end_date: Optional[datetime.datetime] = Field(
            alias="created_at_range_end_date", default=None
        ),
        created_at_range_start_date: Optional[datetime.datetime] = Field(
            alias="created_at_range_start_date", default=None
        ),
        direction: Optional[str] = Field(alias="direction", default=None),
        fields: Optional[str] = Field(alias="fields", default=None),
        file_extensions: Optional[str] = Field(alias="file_extensions", default=None),
        include_recent_shared_links: Optional[bool] = Field(
            alias="include_recent_shared_links", default=None
        ),
        mdfilters: Optional[str] = Field(alias="mdfilters", default=None),
        next_page: Optional[str] = Field(alias="nextPage", default=None),
        owner_user_ids: Optional[str] = Field(alias="owner_user_ids", default=None),
        page_size: Optional[int] = Field(alias="pageSize", default=None),
        scope: Optional[str] = Field(alias="scope", default=None),
        sort: Optional[str] = Field(alias="sort", default=None),
        trash_content: Optional[str] = Field(alias="trash_content", default=None),
        type_: Optional[str] = Field(alias="type", default=None),
        updated_at_range_end_date: Optional[datetime.datetime] = Field(
            alias="updated_at_range_end_date", default=None
        ),
        updated_at_range_start_date: Optional[datetime.datetime] = Field(
            alias="updated_at_range_start_date", default=None
        ),
        where: Optional[str] = Field(alias="where", default=None),
    ) -> Optional[Union[DefaultError, list["Search"]]]:
        return await _search_async(
            client=self.client,
            query=query,
            ancestor_folder_ids=ancestor_folder_ids,
            ancestor_folder_ids_lookup=ancestor_folder_ids_lookup,
            content_types=content_types,
            created_at_range_end_date=created_at_range_end_date,
            created_at_range_start_date=created_at_range_start_date,
            direction=direction,
            fields=fields,
            file_extensions=file_extensions,
            include_recent_shared_links=include_recent_shared_links,
            mdfilters=mdfilters,
            next_page=next_page,
            owner_user_ids=owner_user_ids,
            page_size=page_size,
            scope=scope,
            sort=sort,
            trash_content=trash_content,
            type_=type_,
            updated_at_range_end_date=updated_at_range_end_date,
            updated_at_range_start_date=updated_at_range_start_date,
            where=where,
        )

    def create_sign_request(
        self,
        *,
        body: CreateSignRequestRequest,
    ) -> Optional[Union[CreateSignRequestResponse, DefaultError]]:
        return _create_sign_request(
            client=self.client,
            body=body,
        )

    async def create_sign_request_async(
        self,
        *,
        body: CreateSignRequestRequest,
    ) -> Optional[Union[CreateSignRequestResponse, DefaultError]]:
        return await _create_sign_request_async(
            client=self.client,
            body=body,
        )

    def cancel_sign_request(
        self,
        sign_request_id: str,
        sign_request_id_lookup: Any,
    ) -> Optional[Union[CancelSignRequestResponse, DefaultError]]:
        return _cancel_sign_request(
            client=self.client,
            sign_request_id=sign_request_id,
            sign_request_id_lookup=sign_request_id_lookup,
        )

    async def cancel_sign_request_async(
        self,
        sign_request_id: str,
        sign_request_id_lookup: Any,
    ) -> Optional[Union[CancelSignRequestResponse, DefaultError]]:
        return await _cancel_sign_request_async(
            client=self.client,
            sign_request_id=sign_request_id,
            sign_request_id_lookup=sign_request_id_lookup,
        )

    def list_sign_request(
        self,
        *,
        fields: Optional[str] = Field(alias="fields", default=None),
        next_page: Optional[str] = Field(alias="nextPage", default=None),
        page_size: Optional[int] = Field(alias="pageSize", default=None),
        where: Optional[str] = Field(alias="where", default=None),
    ) -> Optional[Union[DefaultError, list["ListSignRequest"]]]:
        return _list_sign_request(
            client=self.client,
            fields=fields,
            next_page=next_page,
            page_size=page_size,
            where=where,
        )

    async def list_sign_request_async(
        self,
        *,
        fields: Optional[str] = Field(alias="fields", default=None),
        next_page: Optional[str] = Field(alias="nextPage", default=None),
        page_size: Optional[int] = Field(alias="pageSize", default=None),
        where: Optional[str] = Field(alias="where", default=None),
    ) -> Optional[Union[DefaultError, list["ListSignRequest"]]]:
        return await _list_sign_request_async(
            client=self.client,
            fields=fields,
            next_page=next_page,
            page_size=page_size,
            where=where,
        )

    def add_shared_linktoa_folder(
        self,
        folder_id: str,
        folder_id_lookup: Any,
        *,
        body: AddSharedLinktoaFolderRequest,
    ) -> Optional[Union[AddSharedLinktoaFolderResponse, DefaultError]]:
        return _add_shared_linktoa_folder(
            client=self.client,
            folder_id=folder_id,
            folder_id_lookup=folder_id_lookup,
            body=body,
        )

    async def add_shared_linktoa_folder_async(
        self,
        folder_id: str,
        folder_id_lookup: Any,
        *,
        body: AddSharedLinktoaFolderRequest,
    ) -> Optional[Union[AddSharedLinktoaFolderResponse, DefaultError]]:
        return await _add_shared_linktoa_folder_async(
            client=self.client,
            folder_id=folder_id,
            folder_id_lookup=folder_id_lookup,
            body=body,
        )
