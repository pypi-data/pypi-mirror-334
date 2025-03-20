from .download_email import (
    download_email as _download_email,
    download_email_async as _download_email_async,
)
from ..models.default_error import DefaultError
from typing import cast
from .archive_email import (
    archive_email as _archive_email,
    archive_email_async as _archive_email_async,
)
from ..models.archive_email_response import ArchiveEmailResponse
from .apply_gmail_label import (
    apply_gmail_label as _apply_gmail_label,
    apply_gmail_label_async as _apply_gmail_label_async,
)
from ..models.apply_gmail_label_request import ApplyGmailLabelRequest
from ..models.apply_gmail_label_response import ApplyGmailLabelResponse
from .reply_to_email import (
    reply_to_email as _reply_to_email,
    reply_to_email_async as _reply_to_email_async,
)
from ..models.reply_to_email_body import ReplyToEmailBody
from ..models.reply_to_email_response import ReplyToEmailResponse
from .forward_mail import (
    forward_mail as _forward_mail,
    forward_mail_async as _forward_mail_async,
)
from ..models.forward_mail_response import ForwardMailResponse
from .turn_off_automatic_replies import (
    turn_off_automatic_replies as _turn_off_automatic_replies,
    turn_off_automatic_replies_async as _turn_off_automatic_replies_async,
)
from ..models.turn_off_automatic_replies_response import TurnOffAutomaticRepliesResponse
from .send_email import (
    send_email as _send_email,
    send_email_async as _send_email_async,
)
from ..models.send_email_body import SendEmailBody
from ..models.send_email_response import SendEmailResponse
from .remove_gmail_label import (
    remove_gmail_label as _remove_gmail_label,
    remove_gmail_label_async as _remove_gmail_label_async,
)
from ..models.remove_gmail_label_request import RemoveGmailLabelRequest
from ..models.remove_gmail_label_response import RemoveGmailLabelResponse
from .message import (
    get_email_by_id as _get_email_by_id,
    get_email_by_id_async as _get_email_by_id_async,
)
from ..models.get_email_by_id_format import GetEmailByIDFormat
from ..models.get_email_by_id_response import GetEmailByIDResponse
from .curated_calendar_list import (
    get_calendar_list as _get_calendar_list,
    get_calendar_list_async as _get_calendar_list_async,
)
from ..models.get_calendar_list import GetCalendarList
from .mark_email_read_unread import (
    mark_email_read_unread as _mark_email_read_unread,
    mark_email_read_unread_async as _mark_email_read_unread_async,
)
from ..models.mark_email_read_unread_response import MarkEmailReadUnreadResponse
from .list_calendar_event import (
    list_calendar_event as _list_calendar_event,
    list_calendar_event_async as _list_calendar_event_async,
)
from ..models.list_calendar_event import ListCalendarEvent
from dateutil.parser import isoparse
import datetime
from .folder import (
    get_single_label_by_id as _get_single_label_by_id,
    get_single_label_by_id_async as _get_single_label_by_id_async,
    get_email_labels as _get_email_labels,
    get_email_labels_async as _get_email_labels_async,
)
from ..models.get_single_label_by_id_response import GetSingleLabelByIDResponse
from ..models.get_email_labels import GetEmailLabels
from .create_calendar_event import (
    create_calendar_event as _create_calendar_event,
    create_calendar_event_async as _create_calendar_event_async,
)
from ..models.create_calendar_event_request import CreateCalendarEventRequest
from ..models.create_calendar_event_response import CreateCalendarEventResponse
from .list_email import (
    list_email as _list_email,
    list_email_async as _list_email_async,
)
from ..models.list_email import ListEmail
from .delete_email import (
    delete_email as _delete_email,
    delete_email_async as _delete_email_async,
)
from ..models.delete_email_response import DeleteEmailResponse
from .update_calendar_event import (
    update_calendar_event as _update_calendar_event,
    update_calendar_event_async as _update_calendar_event_async,
)
from ..models.update_calendar_event_request import UpdateCalendarEventRequest
from ..models.update_calendar_event_response import UpdateCalendarEventResponse
from .download_attachment import (
    download_attachment as _download_attachment,
    download_attachment_async as _download_attachment_async,
)
from .move_email import (
    move_email as _move_email,
    move_email_async as _move_email_async,
)
from ..models.move_email_response import MoveEmailResponse
from .turn_on_automatic_replies import (
    turn_on_automatic_replies as _turn_on_automatic_replies,
    turn_on_automatic_replies_async as _turn_on_automatic_replies_async,
)
from ..models.turn_on_automatic_replies_request import TurnOnAutomaticRepliesRequest
from ..models.turn_on_automatic_replies_response import TurnOnAutomaticRepliesResponse

from pydantic import Field
from typing import Any, Optional, Union

from ..client import Client
import httpx


class GoogleGmail:
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

    def download_email(
        self,
        *,
        id: str = Field(alias="id"),
    ) -> Optional[Union[Any, DefaultError]]:
        return _download_email(
            client=self.client,
            id=id,
        )

    async def download_email_async(
        self,
        *,
        id: str = Field(alias="id"),
    ) -> Optional[Union[Any, DefaultError]]:
        return await _download_email_async(
            client=self.client,
            id=id,
        )

    def archive_email(
        self,
        *,
        id: str = Field(alias="id"),
    ) -> Optional[Union[ArchiveEmailResponse, DefaultError]]:
        return _archive_email(
            client=self.client,
            id=id,
        )

    async def archive_email_async(
        self,
        *,
        id: str = Field(alias="id"),
    ) -> Optional[Union[ArchiveEmailResponse, DefaultError]]:
        return await _archive_email_async(
            client=self.client,
            id=id,
        )

    def apply_gmail_label(
        self,
        *,
        body: ApplyGmailLabelRequest,
        id: str = Field(alias="id"),
    ) -> Optional[Union[ApplyGmailLabelResponse, DefaultError]]:
        return _apply_gmail_label(
            client=self.client,
            body=body,
            id=id,
        )

    async def apply_gmail_label_async(
        self,
        *,
        body: ApplyGmailLabelRequest,
        id: str = Field(alias="id"),
    ) -> Optional[Union[ApplyGmailLabelResponse, DefaultError]]:
        return await _apply_gmail_label_async(
            client=self.client,
            body=body,
            id=id,
        )

    def reply_to_email(
        self,
        *,
        body: ReplyToEmailBody,
        save_as_draft: Optional[bool] = Field(alias="SaveAsDraft", default=None),
    ) -> Optional[Union[DefaultError, ReplyToEmailResponse]]:
        return _reply_to_email(
            client=self.client,
            body=body,
            save_as_draft=save_as_draft,
        )

    async def reply_to_email_async(
        self,
        *,
        body: ReplyToEmailBody,
        save_as_draft: Optional[bool] = Field(alias="SaveAsDraft", default=None),
    ) -> Optional[Union[DefaultError, ReplyToEmailResponse]]:
        return await _reply_to_email_async(
            client=self.client,
            body=body,
            save_as_draft=save_as_draft,
        )

    def forward_mail(
        self,
        *,
        to: str = Field(alias="To"),
        id: str = Field(alias="id"),
    ) -> Optional[Union[DefaultError, ForwardMailResponse]]:
        return _forward_mail(
            client=self.client,
            to=to,
            id=id,
        )

    async def forward_mail_async(
        self,
        *,
        to: str = Field(alias="To"),
        id: str = Field(alias="id"),
    ) -> Optional[Union[DefaultError, ForwardMailResponse]]:
        return await _forward_mail_async(
            client=self.client,
            to=to,
            id=id,
        )

    def turn_off_automatic_replies(
        self,
    ) -> Optional[Union[DefaultError, TurnOffAutomaticRepliesResponse]]:
        return _turn_off_automatic_replies(
            client=self.client,
        )

    async def turn_off_automatic_replies_async(
        self,
    ) -> Optional[Union[DefaultError, TurnOffAutomaticRepliesResponse]]:
        return await _turn_off_automatic_replies_async(
            client=self.client,
        )

    def send_email(
        self,
        *,
        body: SendEmailBody,
        save_as_draft: Optional[bool] = Field(alias="SaveAsDraft", default=None),
    ) -> Optional[Union[DefaultError, SendEmailResponse]]:
        return _send_email(
            client=self.client,
            body=body,
            save_as_draft=save_as_draft,
        )

    async def send_email_async(
        self,
        *,
        body: SendEmailBody,
        save_as_draft: Optional[bool] = Field(alias="SaveAsDraft", default=None),
    ) -> Optional[Union[DefaultError, SendEmailResponse]]:
        return await _send_email_async(
            client=self.client,
            body=body,
            save_as_draft=save_as_draft,
        )

    def remove_gmail_label(
        self,
        *,
        body: RemoveGmailLabelRequest,
        id: str = Field(alias="id"),
    ) -> Optional[Union[DefaultError, RemoveGmailLabelResponse]]:
        return _remove_gmail_label(
            client=self.client,
            body=body,
            id=id,
        )

    async def remove_gmail_label_async(
        self,
        *,
        body: RemoveGmailLabelRequest,
        id: str = Field(alias="id"),
    ) -> Optional[Union[DefaultError, RemoveGmailLabelResponse]]:
        return await _remove_gmail_label_async(
            client=self.client,
            body=body,
            id=id,
        )

    def get_email_by_id(
        self,
        id: str,
        *,
        format_: Optional[GetEmailByIDFormat] = Field(alias="format", default=None),
        metadata_headers: Optional[str] = Field(
            alias="metadataHeaders[]", default=None
        ),
    ) -> Optional[Union[DefaultError, GetEmailByIDResponse]]:
        return _get_email_by_id(
            client=self.client,
            id=id,
            format_=format_,
            metadata_headers=metadata_headers,
        )

    async def get_email_by_id_async(
        self,
        id: str,
        *,
        format_: Optional[GetEmailByIDFormat] = Field(alias="format", default=None),
        metadata_headers: Optional[str] = Field(
            alias="metadataHeaders[]", default=None
        ),
    ) -> Optional[Union[DefaultError, GetEmailByIDResponse]]:
        return await _get_email_by_id_async(
            client=self.client,
            id=id,
            format_=format_,
            metadata_headers=metadata_headers,
        )

    def get_calendar_list(
        self,
        *,
        fields: Optional[str] = Field(alias="fields", default=None),
        next_page: Optional[str] = Field(alias="nextPage", default=None),
        page_size: Optional[int] = Field(alias="pageSize", default=None),
        parent_reference: Optional[str] = Field(alias="parentReference", default=None),
    ) -> Optional[Union[DefaultError, list["GetCalendarList"]]]:
        return _get_calendar_list(
            client=self.client,
            fields=fields,
            next_page=next_page,
            page_size=page_size,
            parent_reference=parent_reference,
        )

    async def get_calendar_list_async(
        self,
        *,
        fields: Optional[str] = Field(alias="fields", default=None),
        next_page: Optional[str] = Field(alias="nextPage", default=None),
        page_size: Optional[int] = Field(alias="pageSize", default=None),
        parent_reference: Optional[str] = Field(alias="parentReference", default=None),
    ) -> Optional[Union[DefaultError, list["GetCalendarList"]]]:
        return await _get_calendar_list_async(
            client=self.client,
            fields=fields,
            next_page=next_page,
            page_size=page_size,
            parent_reference=parent_reference,
        )

    def mark_email_read_unread(
        self,
        *,
        id: str = Field(alias="id"),
        mark_as: Optional[str] = Field(alias="markAs", default="Read"),
    ) -> Optional[Union[DefaultError, MarkEmailReadUnreadResponse]]:
        return _mark_email_read_unread(
            client=self.client,
            id=id,
            mark_as=mark_as,
        )

    async def mark_email_read_unread_async(
        self,
        *,
        id: str = Field(alias="id"),
        mark_as: Optional[str] = Field(alias="markAs", default="Read"),
    ) -> Optional[Union[DefaultError, MarkEmailReadUnreadResponse]]:
        return await _mark_email_read_unread_async(
            client=self.client,
            id=id,
            mark_as=mark_as,
        )

    def list_calendar_event(
        self,
        *,
        from_: datetime.datetime = Field(alias="From"),
        until: datetime.datetime = Field(alias="Until"),
        calendar: Optional[str] = Field(alias="Calendar", default=None),
        calendar_lookup: Any,
        fields: Optional[str] = Field(alias="fields", default=None),
        limit: Optional[str] = Field(alias="limit", default="50"),
        next_page: Optional[str] = Field(alias="nextPage", default=None),
        page_size: Optional[int] = Field(alias="pageSize", default=None),
        q: Optional[str] = Field(alias="q", default=None),
        time_zone: Optional[str] = Field(alias="timeZone", default=None),
    ) -> Optional[Union[DefaultError, list["ListCalendarEvent"]]]:
        return _list_calendar_event(
            client=self.client,
            from_=from_,
            until=until,
            calendar=calendar,
            calendar_lookup=calendar_lookup,
            fields=fields,
            limit=limit,
            next_page=next_page,
            page_size=page_size,
            q=q,
            time_zone=time_zone,
        )

    async def list_calendar_event_async(
        self,
        *,
        from_: datetime.datetime = Field(alias="From"),
        until: datetime.datetime = Field(alias="Until"),
        calendar: Optional[str] = Field(alias="Calendar", default=None),
        calendar_lookup: Any,
        fields: Optional[str] = Field(alias="fields", default=None),
        limit: Optional[str] = Field(alias="limit", default="50"),
        next_page: Optional[str] = Field(alias="nextPage", default=None),
        page_size: Optional[int] = Field(alias="pageSize", default=None),
        q: Optional[str] = Field(alias="q", default=None),
        time_zone: Optional[str] = Field(alias="timeZone", default=None),
    ) -> Optional[Union[DefaultError, list["ListCalendarEvent"]]]:
        return await _list_calendar_event_async(
            client=self.client,
            from_=from_,
            until=until,
            calendar=calendar,
            calendar_lookup=calendar_lookup,
            fields=fields,
            limit=limit,
            next_page=next_page,
            page_size=page_size,
            q=q,
            time_zone=time_zone,
        )

    def get_single_label_by_id(
        self,
        id: str,
    ) -> Optional[Union[DefaultError, GetSingleLabelByIDResponse]]:
        return _get_single_label_by_id(
            client=self.client,
            id=id,
        )

    async def get_single_label_by_id_async(
        self,
        id: str,
    ) -> Optional[Union[DefaultError, GetSingleLabelByIDResponse]]:
        return await _get_single_label_by_id_async(
            client=self.client,
            id=id,
        )

    def get_email_labels(
        self,
        *,
        fields: Optional[str] = Field(alias="fields", default=None),
        next_page: Optional[str] = Field(alias="nextPage", default=None),
        page_size: Optional[int] = Field(alias="pageSize", default=None),
        parent_reference: Optional[str] = Field(alias="parentReference", default=None),
    ) -> Optional[Union[DefaultError, list["GetEmailLabels"]]]:
        return _get_email_labels(
            client=self.client,
            fields=fields,
            next_page=next_page,
            page_size=page_size,
            parent_reference=parent_reference,
        )

    async def get_email_labels_async(
        self,
        *,
        fields: Optional[str] = Field(alias="fields", default=None),
        next_page: Optional[str] = Field(alias="nextPage", default=None),
        page_size: Optional[int] = Field(alias="pageSize", default=None),
        parent_reference: Optional[str] = Field(alias="parentReference", default=None),
    ) -> Optional[Union[DefaultError, list["GetEmailLabels"]]]:
        return await _get_email_labels_async(
            client=self.client,
            fields=fields,
            next_page=next_page,
            page_size=page_size,
            parent_reference=parent_reference,
        )

    def create_calendar_event(
        self,
        *,
        body: CreateCalendarEventRequest,
        add_conference_data: Optional[bool] = Field(
            alias="AddConferenceData", default=False
        ),
        calendar: Optional[str] = Field(alias="Calendar", default=None),
        calendar_lookup: Any,
        send_notifications: Optional[str] = Field(
            alias="SendNotifications", default=None
        ),
    ) -> Optional[Union[CreateCalendarEventResponse, DefaultError]]:
        return _create_calendar_event(
            client=self.client,
            body=body,
            add_conference_data=add_conference_data,
            calendar=calendar,
            calendar_lookup=calendar_lookup,
            send_notifications=send_notifications,
        )

    async def create_calendar_event_async(
        self,
        *,
        body: CreateCalendarEventRequest,
        add_conference_data: Optional[bool] = Field(
            alias="AddConferenceData", default=False
        ),
        calendar: Optional[str] = Field(alias="Calendar", default=None),
        calendar_lookup: Any,
        send_notifications: Optional[str] = Field(
            alias="SendNotifications", default=None
        ),
    ) -> Optional[Union[CreateCalendarEventResponse, DefaultError]]:
        return await _create_calendar_event_async(
            client=self.client,
            body=body,
            add_conference_data=add_conference_data,
            calendar=calendar,
            calendar_lookup=calendar_lookup,
            send_notifications=send_notifications,
        )

    def list_email(
        self,
        *,
        email_folder: str = Field(alias="emailFolder"),
        email_folder_lookup: Any,
        additional_filters: Optional[str] = Field(
            alias="additionalFilters", default=None
        ),
        fields: Optional[str] = Field(alias="fields", default=None),
        important_only: Optional[bool] = Field(alias="importantOnly", default=None),
        next_page: Optional[str] = Field(alias="nextPage", default=None),
        page_size: Optional[int] = Field(alias="pageSize", default=None),
        starred_only: Optional[bool] = Field(alias="starredOnly", default=None),
        unread_only: Optional[bool] = Field(alias="unreadOnly", default=None),
        with_attachments_only: Optional[bool] = Field(
            alias="withAttachmentsOnly", default=None
        ),
    ) -> Optional[Union[DefaultError, list["ListEmail"]]]:
        return _list_email(
            client=self.client,
            email_folder=email_folder,
            email_folder_lookup=email_folder_lookup,
            additional_filters=additional_filters,
            fields=fields,
            important_only=important_only,
            next_page=next_page,
            page_size=page_size,
            starred_only=starred_only,
            unread_only=unread_only,
            with_attachments_only=with_attachments_only,
        )

    async def list_email_async(
        self,
        *,
        email_folder: str = Field(alias="emailFolder"),
        email_folder_lookup: Any,
        additional_filters: Optional[str] = Field(
            alias="additionalFilters", default=None
        ),
        fields: Optional[str] = Field(alias="fields", default=None),
        important_only: Optional[bool] = Field(alias="importantOnly", default=None),
        next_page: Optional[str] = Field(alias="nextPage", default=None),
        page_size: Optional[int] = Field(alias="pageSize", default=None),
        starred_only: Optional[bool] = Field(alias="starredOnly", default=None),
        unread_only: Optional[bool] = Field(alias="unreadOnly", default=None),
        with_attachments_only: Optional[bool] = Field(
            alias="withAttachmentsOnly", default=None
        ),
    ) -> Optional[Union[DefaultError, list["ListEmail"]]]:
        return await _list_email_async(
            client=self.client,
            email_folder=email_folder,
            email_folder_lookup=email_folder_lookup,
            additional_filters=additional_filters,
            fields=fields,
            important_only=important_only,
            next_page=next_page,
            page_size=page_size,
            starred_only=starred_only,
            unread_only=unread_only,
            with_attachments_only=with_attachments_only,
        )

    def delete_email(
        self,
        *,
        permanently_delete: Optional[bool] = Field(
            alias="permanentlyDelete", default=False
        ),
        id: str = Field(alias="id"),
    ) -> Optional[Union[DefaultError, DeleteEmailResponse]]:
        return _delete_email(
            client=self.client,
            permanently_delete=permanently_delete,
            id=id,
        )

    async def delete_email_async(
        self,
        *,
        permanently_delete: Optional[bool] = Field(
            alias="permanentlyDelete", default=False
        ),
        id: str = Field(alias="id"),
    ) -> Optional[Union[DefaultError, DeleteEmailResponse]]:
        return await _delete_email_async(
            client=self.client,
            permanently_delete=permanently_delete,
            id=id,
        )

    def update_calendar_event(
        self,
        id: str,
        *,
        body: UpdateCalendarEventRequest,
        add_conference_data: Optional[bool] = Field(
            alias="AddConferenceData", default=None
        ),
        calendar: Optional[str] = Field(alias="Calendar", default=None),
        send_notifications: Optional[str] = Field(
            alias="SendNotifications", default="All"
        ),
    ) -> Optional[Union[DefaultError, UpdateCalendarEventResponse]]:
        return _update_calendar_event(
            client=self.client,
            id=id,
            body=body,
            add_conference_data=add_conference_data,
            calendar=calendar,
            send_notifications=send_notifications,
        )

    async def update_calendar_event_async(
        self,
        id: str,
        *,
        body: UpdateCalendarEventRequest,
        add_conference_data: Optional[bool] = Field(
            alias="AddConferenceData", default=None
        ),
        calendar: Optional[str] = Field(alias="Calendar", default=None),
        send_notifications: Optional[str] = Field(
            alias="SendNotifications", default="All"
        ),
    ) -> Optional[Union[DefaultError, UpdateCalendarEventResponse]]:
        return await _update_calendar_event_async(
            client=self.client,
            id=id,
            body=body,
            add_conference_data=add_conference_data,
            calendar=calendar,
            send_notifications=send_notifications,
        )

    def download_attachment(
        self,
        id: str,
        *,
        exclude_inline_attachment: Optional[bool] = Field(
            alias="excludeInlineAttachment", default=False
        ),
        file_name: Optional[str] = Field(alias="fileName", default=None),
    ) -> Optional[Union[Any, DefaultError]]:
        return _download_attachment(
            client=self.client,
            id=id,
            exclude_inline_attachment=exclude_inline_attachment,
            file_name=file_name,
        )

    async def download_attachment_async(
        self,
        id: str,
        *,
        exclude_inline_attachment: Optional[bool] = Field(
            alias="excludeInlineAttachment", default=False
        ),
        file_name: Optional[str] = Field(alias="fileName", default=None),
    ) -> Optional[Union[Any, DefaultError]]:
        return await _download_attachment_async(
            client=self.client,
            id=id,
            exclude_inline_attachment=exclude_inline_attachment,
            file_name=file_name,
        )

    def move_email(
        self,
        *,
        id: str = Field(alias="id"),
        add_label_id: str = Field(alias="addLabelId"),
        add_label_id_lookup: Any,
    ) -> Optional[Union[DefaultError, MoveEmailResponse]]:
        return _move_email(
            client=self.client,
            id=id,
            add_label_id=add_label_id,
            add_label_id_lookup=add_label_id_lookup,
        )

    async def move_email_async(
        self,
        *,
        id: str = Field(alias="id"),
        add_label_id: str = Field(alias="addLabelId"),
        add_label_id_lookup: Any,
    ) -> Optional[Union[DefaultError, MoveEmailResponse]]:
        return await _move_email_async(
            client=self.client,
            id=id,
            add_label_id=add_label_id,
            add_label_id_lookup=add_label_id_lookup,
        )

    def turn_on_automatic_replies(
        self,
        *,
        body: TurnOnAutomaticRepliesRequest,
    ) -> Optional[Union[DefaultError, TurnOnAutomaticRepliesResponse]]:
        return _turn_on_automatic_replies(
            client=self.client,
            body=body,
        )

    async def turn_on_automatic_replies_async(
        self,
        *,
        body: TurnOnAutomaticRepliesRequest,
    ) -> Optional[Union[DefaultError, TurnOnAutomaticRepliesResponse]]:
        return await _turn_on_automatic_replies_async(
            client=self.client,
            body=body,
        )
