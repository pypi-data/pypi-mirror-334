from http import HTTPStatus
from typing import Any, Optional, Union

import httpx
from pydantic import Field

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.default_error import DefaultError
from ...models.search import Search
import datetime


def _get_kwargs(
    *,
    query: str = Field(alias="query"),
    ancestor_folder_ids: Optional[str] = Field(
        alias="ancestor_folder_ids", default=None
    ),
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
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["query"] = query

    params["ancestor_folder_ids"] = ancestor_folder_ids

    params["content_types"] = content_types

    json_created_at_range_end_date: Optional[str] = None
    if created_at_range_end_date is not None:
        json_created_at_range_end_date = created_at_range_end_date.isoformat()
    params["created_at_range_end_date"] = json_created_at_range_end_date

    json_created_at_range_start_date: Optional[str] = None
    if created_at_range_start_date is not None:
        json_created_at_range_start_date = created_at_range_start_date.isoformat()
    params["created_at_range_start_date"] = json_created_at_range_start_date

    params["direction"] = direction

    params["fields"] = fields

    params["file_extensions"] = file_extensions

    params["include_recent_shared_links"] = include_recent_shared_links

    params["mdfilters"] = mdfilters

    params["nextPage"] = next_page

    params["owner_user_ids"] = owner_user_ids

    params["pageSize"] = page_size

    params["scope"] = scope

    params["sort"] = sort

    params["trash_content"] = trash_content

    params["type"] = type_

    json_updated_at_range_end_date: Optional[str] = None
    if updated_at_range_end_date is not None:
        json_updated_at_range_end_date = updated_at_range_end_date.isoformat()
    params["updated_at_range_end_date"] = json_updated_at_range_end_date

    json_updated_at_range_start_date: Optional[str] = None
    if updated_at_range_start_date is not None:
        json_updated_at_range_start_date = updated_at_range_start_date.isoformat()
    params["updated_at_range_start_date"] = json_updated_at_range_start_date

    params["where"] = where

    params = {k: v for k, v in params.items() if v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/search",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DefaultError, list["Search"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_search_list_item_data in _response_200:
            componentsschemas_search_list_item = Search.from_dict(
                componentsschemas_search_list_item_data
            )

            response_200.append(componentsschemas_search_list_item)

        return response_200
    if response.status_code == 400:
        response_400 = DefaultError.from_dict(response.json())

        return response_400
    if response.status_code == 401:
        response_401 = DefaultError.from_dict(response.json())

        return response_401
    if response.status_code == 403:
        response_403 = DefaultError.from_dict(response.json())

        return response_403
    if response.status_code == 404:
        response_404 = DefaultError.from_dict(response.json())

        return response_404
    if response.status_code == 405:
        response_405 = DefaultError.from_dict(response.json())

        return response_405
    if response.status_code == 406:
        response_406 = DefaultError.from_dict(response.json())

        return response_406
    if response.status_code == 409:
        response_409 = DefaultError.from_dict(response.json())

        return response_409
    if response.status_code == 415:
        response_415 = DefaultError.from_dict(response.json())

        return response_415
    if response.status_code == 500:
        response_500 = DefaultError.from_dict(response.json())

        return response_500
    if response.status_code == 402:
        response_402 = DefaultError.from_dict(response.json())

        return response_402
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[DefaultError, list["Search"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
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
) -> Response[Union[DefaultError, list["Search"]]]:
    """Search for Content

     Searches for content in Box based on the filters specified

    Args:
        query (str):
        ancestor_folder_ids (Optional[str]):
        content_types (Optional[str]):
        created_at_range_end_date (Optional[datetime.datetime]):
        created_at_range_start_date (Optional[datetime.datetime]):
        direction (Optional[str]):
        fields (Optional[str]):
        file_extensions (Optional[str]):
        include_recent_shared_links (Optional[bool]):
        mdfilters (Optional[str]):
        next_page (Optional[str]):
        owner_user_ids (Optional[str]):
        page_size (Optional[int]):
        scope (Optional[str]):
        sort (Optional[str]):
        trash_content (Optional[str]):
        type_ (Optional[str]):
        updated_at_range_end_date (Optional[datetime.datetime]):
        updated_at_range_start_date (Optional[datetime.datetime]):
        where (Optional[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, list['Search']]]
    """

    if not ancestor_folder_ids and ancestor_folder_ids_lookup:
        lookup_response_raw = client.get_httpx_client().request(
            method="get", url="/folder_picker_folder"
        )
        lookup_response = lookup_response_raw.json()

        found_items = []
        for item in lookup_response:
            if ancestor_folder_ids_lookup in item["FullName"]:
                found_items.append(item)

        if not found_items:
            raise ValueError(
                "No matches found for ancestor_folder_ids_lookup in folder_picker_folder"
            )
        if len(found_items) > 1:
            print(
                "Warning: Multiple matches found for ancestor_folder_ids_lookup in folder_picker_folder. Using the first match."
            )

        ancestor_folder_ids = found_items[0]["ReferenceID"]

    kwargs = _get_kwargs(
        query=query,
        ancestor_folder_ids=ancestor_folder_ids,
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

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
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
    """Search for Content

     Searches for content in Box based on the filters specified

    Args:
        query (str):
        ancestor_folder_ids (Optional[str]):
        content_types (Optional[str]):
        created_at_range_end_date (Optional[datetime.datetime]):
        created_at_range_start_date (Optional[datetime.datetime]):
        direction (Optional[str]):
        fields (Optional[str]):
        file_extensions (Optional[str]):
        include_recent_shared_links (Optional[bool]):
        mdfilters (Optional[str]):
        next_page (Optional[str]):
        owner_user_ids (Optional[str]):
        page_size (Optional[int]):
        scope (Optional[str]):
        sort (Optional[str]):
        trash_content (Optional[str]):
        type_ (Optional[str]):
        updated_at_range_end_date (Optional[datetime.datetime]):
        updated_at_range_start_date (Optional[datetime.datetime]):
        where (Optional[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, list['Search']]
    """

    return sync_detailed(
        client=client,
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
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
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
) -> Response[Union[DefaultError, list["Search"]]]:
    """Search for Content

     Searches for content in Box based on the filters specified

    Args:
        query (str):
        ancestor_folder_ids (Optional[str]):
        content_types (Optional[str]):
        created_at_range_end_date (Optional[datetime.datetime]):
        created_at_range_start_date (Optional[datetime.datetime]):
        direction (Optional[str]):
        fields (Optional[str]):
        file_extensions (Optional[str]):
        include_recent_shared_links (Optional[bool]):
        mdfilters (Optional[str]):
        next_page (Optional[str]):
        owner_user_ids (Optional[str]):
        page_size (Optional[int]):
        scope (Optional[str]):
        sort (Optional[str]):
        trash_content (Optional[str]):
        type_ (Optional[str]):
        updated_at_range_end_date (Optional[datetime.datetime]):
        updated_at_range_start_date (Optional[datetime.datetime]):
        where (Optional[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, list['Search']]]
    """

    if not ancestor_folder_ids and ancestor_folder_ids_lookup:
        lookup_response_raw = await client.get_async_httpx_client().request(
            method="get", url="/folder_picker_folder"
        )
        lookup_response = lookup_response_raw.json()

        found_items = []
        for item in lookup_response:
            if ancestor_folder_ids_lookup in item["FullName"]:
                found_items.append(item)

        if not found_items:
            raise ValueError(
                "No matches found for ancestor_folder_ids_lookup in folder_picker_folder"
            )
        if len(found_items) > 1:
            print(
                "Warning: Multiple matches found for ancestor_folder_ids_lookup in folder_picker_folder. Using the first match."
            )

        ancestor_folder_ids = found_items[0]["ReferenceID"]

    kwargs = _get_kwargs(
        query=query,
        ancestor_folder_ids=ancestor_folder_ids,
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

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
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
    """Search for Content

     Searches for content in Box based on the filters specified

    Args:
        query (str):
        ancestor_folder_ids (Optional[str]):
        content_types (Optional[str]):
        created_at_range_end_date (Optional[datetime.datetime]):
        created_at_range_start_date (Optional[datetime.datetime]):
        direction (Optional[str]):
        fields (Optional[str]):
        file_extensions (Optional[str]):
        include_recent_shared_links (Optional[bool]):
        mdfilters (Optional[str]):
        next_page (Optional[str]):
        owner_user_ids (Optional[str]):
        page_size (Optional[int]):
        scope (Optional[str]):
        sort (Optional[str]):
        trash_content (Optional[str]):
        type_ (Optional[str]):
        updated_at_range_end_date (Optional[datetime.datetime]):
        updated_at_range_start_date (Optional[datetime.datetime]):
        where (Optional[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, list['Search']]
    """

    return (
        await asyncio_detailed(
            client=client,
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
    ).parsed
