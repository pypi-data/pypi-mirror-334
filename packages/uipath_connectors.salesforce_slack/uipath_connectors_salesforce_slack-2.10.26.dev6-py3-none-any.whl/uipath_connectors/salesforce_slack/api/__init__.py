from .send_files_to_channel import (
    upload_file as _upload_file,
    upload_file_async as _upload_file_async,
)
from ..models.default_error import DefaultError
from ..models.upload_file_body import UploadFileBody
from ..models.upload_file_response import UploadFileResponse
from typing import cast
from .conversations_invite_post import (
    invite_to_channel as _invite_to_channel,
    invite_to_channel_async as _invite_to_channel_async,
)
from ..models.invite_to_channel_request import InviteToChannelRequest
from ..models.invite_to_channel_response import InviteToChannelResponse
from .conversations_info_get import (
    get_conversation_info as _get_conversation_info,
    get_conversation_info_async as _get_conversation_info_async,
)
from ..models.get_conversation_info_response import GetConversationInfoResponse
from .channel_archive import (
    channel_archive as _channel_archive,
    channel_archive_async as _channel_archive_async,
)
from ..models.channel_archive_request import ChannelArchiveRequest
from ..models.channel_archive_response import ChannelArchiveResponse
from .send_reply_v2 import (
    send_reply as _send_reply,
    send_reply_async as _send_reply_async,
)
from ..models.send_reply_request import SendReplyRequest
from ..models.send_reply_response import SendReplyResponse
from .send_button_response import (
    send_button_response as _send_button_response,
    send_button_response_async as _send_button_response_async,
)
from ..models.send_button_response_request import SendButtonResponseRequest
from ..models.send_button_response_response import SendButtonResponseResponse
from .usergroups import (
    list_all_usergroups as _list_all_usergroups,
    list_all_usergroups_async as _list_all_usergroups_async,
    create_usergroup as _create_usergroup,
    create_usergroup_async as _create_usergroup_async,
)
from ..models.list_all_usergroups import ListAllUsergroups
from ..models.create_usergroup_request import CreateUsergroupRequest
from ..models.create_usergroup_response import CreateUsergroupResponse
from .conversations_open import (
    conversations_open as _conversations_open,
    conversations_open_async as _conversations_open_async,
)
from ..models.conversations_open_request import ConversationsOpenRequest
from ..models.conversations_open_response import ConversationsOpenResponse
from .conversations_join_post import (
    conversations_join as _conversations_join,
    conversations_join_async as _conversations_join_async,
)
from ..models.conversations_join_request import ConversationsJoinRequest
from ..models.conversations_join_response import ConversationsJoinResponse
from .send_message_to_channel_v2 import (
    send_message as _send_message,
    send_message_async as _send_message_async,
)
from ..models.send_message_request import SendMessageRequest
from ..models.send_message_response import SendMessageResponse
from .add_users_usergroups import (
    add_users_to_usergroup as _add_users_to_usergroup,
    add_users_to_usergroup_async as _add_users_to_usergroup_async,
)
from ..models.add_users_to_usergroup_request import AddUsersToUsergroupRequest
from ..models.add_users_to_usergroup_response import AddUsersToUsergroupResponse
from .conversations_kick_post import (
    remove_from_channel as _remove_from_channel,
    remove_from_channel_async as _remove_from_channel_async,
)
from ..models.remove_from_channel_request import RemoveFromChannelRequest
from ..models.remove_from_channel_response import RemoveFromChannelResponse
from .conversations import (
    create_channel as _create_channel,
    create_channel_async as _create_channel_async,
)
from ..models.create_channel_request import CreateChannelRequest
from ..models.create_channel_response import CreateChannelResponse
from .users import (
    list_all_users as _list_all_users,
    list_all_users_async as _list_all_users_async,
)
from ..models.list_all_users import ListAllUsers
from .send_message_to_user_v2 import (
    send_message_to_user as _send_message_to_user,
    send_message_to_user_async as _send_message_to_user_async,
)
from ..models.send_message_to_user_request import SendMessageToUserRequest
from ..models.send_message_to_user_response import SendMessageToUserResponse
from .set_channel_topic import (
    set_channel_topic as _set_channel_topic,
    set_channel_topic_async as _set_channel_topic_async,
)
from ..models.set_channel_topic_request import SetChannelTopicRequest
from ..models.set_channel_topic_response import SetChannelTopicResponse
from .users_by_email_get import (
    get_user_by_email as _get_user_by_email,
    get_user_by_email_async as _get_user_by_email_async,
)
from ..models.get_user_by_email_response import GetUserByEmailResponse

from pydantic import Field
from typing import Any, Optional, Union

from ..client import Client
import httpx


class SalesforceSlack:
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

    def upload_file(
        self,
        *,
        body: UploadFileBody,
        send_as: str = Field(alias="send_as"),
        send_as_lookup: Any,
        channels: Optional[str] = Field(alias="channels", default=None),
        channels_lookup: Any,
        filename: Optional[str] = Field(alias="filename", default=None),
        filetype: Optional[str] = Field(alias="filetype", default=None),
        initial_comment: Optional[str] = Field(alias="initial_comment", default=None),
        thread_ts: Optional[str] = Field(alias="thread_ts", default=None),
        title: Optional[str] = Field(alias="title", default=None),
    ) -> Optional[Union[DefaultError, UploadFileResponse]]:
        return _upload_file(
            client=self.client,
            body=body,
            send_as=send_as,
            send_as_lookup=send_as_lookup,
            channels=channels,
            channels_lookup=channels_lookup,
            filename=filename,
            filetype=filetype,
            initial_comment=initial_comment,
            thread_ts=thread_ts,
            title=title,
        )

    async def upload_file_async(
        self,
        *,
        body: UploadFileBody,
        send_as: str = Field(alias="send_as"),
        send_as_lookup: Any,
        channels: Optional[str] = Field(alias="channels", default=None),
        channels_lookup: Any,
        filename: Optional[str] = Field(alias="filename", default=None),
        filetype: Optional[str] = Field(alias="filetype", default=None),
        initial_comment: Optional[str] = Field(alias="initial_comment", default=None),
        thread_ts: Optional[str] = Field(alias="thread_ts", default=None),
        title: Optional[str] = Field(alias="title", default=None),
    ) -> Optional[Union[DefaultError, UploadFileResponse]]:
        return await _upload_file_async(
            client=self.client,
            body=body,
            send_as=send_as,
            send_as_lookup=send_as_lookup,
            channels=channels,
            channels_lookup=channels_lookup,
            filename=filename,
            filetype=filetype,
            initial_comment=initial_comment,
            thread_ts=thread_ts,
            title=title,
        )

    def invite_to_channel(
        self,
        *,
        body: InviteToChannelRequest,
    ) -> Optional[Union[DefaultError, InviteToChannelResponse]]:
        return _invite_to_channel(
            client=self.client,
            body=body,
        )

    async def invite_to_channel_async(
        self,
        *,
        body: InviteToChannelRequest,
    ) -> Optional[Union[DefaultError, InviteToChannelResponse]]:
        return await _invite_to_channel_async(
            client=self.client,
            body=body,
        )

    def get_conversation_info(
        self,
        conversations_info_id: str,
        conversations_info_id_lookup: Any,
        *,
        include_locale: Optional[bool] = Field(alias="include_locale", default=None),
        include_num_members: Optional[bool] = Field(
            alias="include_num_members", default=None
        ),
    ) -> Optional[Union[DefaultError, GetConversationInfoResponse]]:
        return _get_conversation_info(
            client=self.client,
            conversations_info_id=conversations_info_id,
            conversations_info_id_lookup=conversations_info_id_lookup,
            include_locale=include_locale,
            include_num_members=include_num_members,
        )

    async def get_conversation_info_async(
        self,
        conversations_info_id: str,
        conversations_info_id_lookup: Any,
        *,
        include_locale: Optional[bool] = Field(alias="include_locale", default=None),
        include_num_members: Optional[bool] = Field(
            alias="include_num_members", default=None
        ),
    ) -> Optional[Union[DefaultError, GetConversationInfoResponse]]:
        return await _get_conversation_info_async(
            client=self.client,
            conversations_info_id=conversations_info_id,
            conversations_info_id_lookup=conversations_info_id_lookup,
            include_locale=include_locale,
            include_num_members=include_num_members,
        )

    def channel_archive(
        self,
        *,
        body: ChannelArchiveRequest,
    ) -> Optional[Union[ChannelArchiveResponse, DefaultError]]:
        return _channel_archive(
            client=self.client,
            body=body,
        )

    async def channel_archive_async(
        self,
        *,
        body: ChannelArchiveRequest,
    ) -> Optional[Union[ChannelArchiveResponse, DefaultError]]:
        return await _channel_archive_async(
            client=self.client,
            body=body,
        )

    def send_reply(
        self,
        *,
        body: SendReplyRequest,
        send_as: str = Field(alias="send_as", default="bot"),
        send_as_lookup: Any,
    ) -> Optional[Union[DefaultError, SendReplyResponse]]:
        return _send_reply(
            client=self.client,
            body=body,
            send_as=send_as,
            send_as_lookup=send_as_lookup,
        )

    async def send_reply_async(
        self,
        *,
        body: SendReplyRequest,
        send_as: str = Field(alias="send_as", default="bot"),
        send_as_lookup: Any,
    ) -> Optional[Union[DefaultError, SendReplyResponse]]:
        return await _send_reply_async(
            client=self.client,
            body=body,
            send_as=send_as,
            send_as_lookup=send_as_lookup,
        )

    def send_button_response(
        self,
        *,
        body: SendButtonResponseRequest,
    ) -> Optional[Union[DefaultError, SendButtonResponseResponse]]:
        return _send_button_response(
            client=self.client,
            body=body,
        )

    async def send_button_response_async(
        self,
        *,
        body: SendButtonResponseRequest,
    ) -> Optional[Union[DefaultError, SendButtonResponseResponse]]:
        return await _send_button_response_async(
            client=self.client,
            body=body,
        )

    def list_all_usergroups(
        self,
        *,
        fields: Optional[str] = Field(alias="fields", default=None),
        include_count: Optional[bool] = Field(alias="include_count", default=None),
        include_disabled: Optional[bool] = Field(
            alias="include_disabled", default=None
        ),
        include_users: Optional[bool] = Field(alias="include_users", default=None),
        next_page: Optional[str] = Field(alias="nextPage", default=None),
        page_size: Optional[int] = Field(alias="pageSize", default=None),
    ) -> Optional[Union[DefaultError, list["ListAllUsergroups"]]]:
        return _list_all_usergroups(
            client=self.client,
            fields=fields,
            include_count=include_count,
            include_disabled=include_disabled,
            include_users=include_users,
            next_page=next_page,
            page_size=page_size,
        )

    async def list_all_usergroups_async(
        self,
        *,
        fields: Optional[str] = Field(alias="fields", default=None),
        include_count: Optional[bool] = Field(alias="include_count", default=None),
        include_disabled: Optional[bool] = Field(
            alias="include_disabled", default=None
        ),
        include_users: Optional[bool] = Field(alias="include_users", default=None),
        next_page: Optional[str] = Field(alias="nextPage", default=None),
        page_size: Optional[int] = Field(alias="pageSize", default=None),
    ) -> Optional[Union[DefaultError, list["ListAllUsergroups"]]]:
        return await _list_all_usergroups_async(
            client=self.client,
            fields=fields,
            include_count=include_count,
            include_disabled=include_disabled,
            include_users=include_users,
            next_page=next_page,
            page_size=page_size,
        )

    def create_usergroup(
        self,
        *,
        body: CreateUsergroupRequest,
    ) -> Optional[Union[CreateUsergroupResponse, DefaultError]]:
        return _create_usergroup(
            client=self.client,
            body=body,
        )

    async def create_usergroup_async(
        self,
        *,
        body: CreateUsergroupRequest,
    ) -> Optional[Union[CreateUsergroupResponse, DefaultError]]:
        return await _create_usergroup_async(
            client=self.client,
            body=body,
        )

    def conversations_open(
        self,
        *,
        body: ConversationsOpenRequest,
        send_as: str = Field(alias="send_as", default="bot"),
        send_as_lookup: Any,
    ) -> Optional[Union[ConversationsOpenResponse, DefaultError]]:
        return _conversations_open(
            client=self.client,
            body=body,
            send_as=send_as,
            send_as_lookup=send_as_lookup,
        )

    async def conversations_open_async(
        self,
        *,
        body: ConversationsOpenRequest,
        send_as: str = Field(alias="send_as", default="bot"),
        send_as_lookup: Any,
    ) -> Optional[Union[ConversationsOpenResponse, DefaultError]]:
        return await _conversations_open_async(
            client=self.client,
            body=body,
            send_as=send_as,
            send_as_lookup=send_as_lookup,
        )

    def conversations_join(
        self,
        *,
        body: ConversationsJoinRequest,
        send_as: str = Field(alias="send_as", default="bot"),
        send_as_lookup: Any,
    ) -> Optional[Union[ConversationsJoinResponse, DefaultError]]:
        return _conversations_join(
            client=self.client,
            body=body,
            send_as=send_as,
            send_as_lookup=send_as_lookup,
        )

    async def conversations_join_async(
        self,
        *,
        body: ConversationsJoinRequest,
        send_as: str = Field(alias="send_as", default="bot"),
        send_as_lookup: Any,
    ) -> Optional[Union[ConversationsJoinResponse, DefaultError]]:
        return await _conversations_join_async(
            client=self.client,
            body=body,
            send_as=send_as,
            send_as_lookup=send_as_lookup,
        )

    def send_message(
        self,
        *,
        body: SendMessageRequest,
        send_as: str = Field(alias="send_as"),
        send_as_lookup: Any,
    ) -> Optional[Union[DefaultError, SendMessageResponse]]:
        return _send_message(
            client=self.client,
            body=body,
            send_as=send_as,
            send_as_lookup=send_as_lookup,
        )

    async def send_message_async(
        self,
        *,
        body: SendMessageRequest,
        send_as: str = Field(alias="send_as"),
        send_as_lookup: Any,
    ) -> Optional[Union[DefaultError, SendMessageResponse]]:
        return await _send_message_async(
            client=self.client,
            body=body,
            send_as=send_as,
            send_as_lookup=send_as_lookup,
        )

    def add_users_to_usergroup(
        self,
        *,
        body: AddUsersToUsergroupRequest,
    ) -> Optional[Union[AddUsersToUsergroupResponse, DefaultError]]:
        return _add_users_to_usergroup(
            client=self.client,
            body=body,
        )

    async def add_users_to_usergroup_async(
        self,
        *,
        body: AddUsersToUsergroupRequest,
    ) -> Optional[Union[AddUsersToUsergroupResponse, DefaultError]]:
        return await _add_users_to_usergroup_async(
            client=self.client,
            body=body,
        )

    def remove_from_channel(
        self,
        *,
        body: RemoveFromChannelRequest,
    ) -> Optional[Union[DefaultError, RemoveFromChannelResponse]]:
        return _remove_from_channel(
            client=self.client,
            body=body,
        )

    async def remove_from_channel_async(
        self,
        *,
        body: RemoveFromChannelRequest,
    ) -> Optional[Union[DefaultError, RemoveFromChannelResponse]]:
        return await _remove_from_channel_async(
            client=self.client,
            body=body,
        )

    def create_channel(
        self,
        *,
        body: CreateChannelRequest,
    ) -> Optional[Union[CreateChannelResponse, DefaultError]]:
        return _create_channel(
            client=self.client,
            body=body,
        )

    async def create_channel_async(
        self,
        *,
        body: CreateChannelRequest,
    ) -> Optional[Union[CreateChannelResponse, DefaultError]]:
        return await _create_channel_async(
            client=self.client,
            body=body,
        )

    def list_all_users(
        self,
        *,
        fields: Optional[str] = Field(alias="fields", default=None),
        include_locale: Optional[bool] = Field(alias="include_locale", default=None),
        next_page: Optional[str] = Field(alias="nextPage", default=None),
        page_size: Optional[int] = Field(alias="pageSize", default=None),
        team_id: Optional[str] = Field(alias="team_id", default=None),
    ) -> Optional[Union[DefaultError, list["ListAllUsers"]]]:
        return _list_all_users(
            client=self.client,
            fields=fields,
            include_locale=include_locale,
            next_page=next_page,
            page_size=page_size,
            team_id=team_id,
        )

    async def list_all_users_async(
        self,
        *,
        fields: Optional[str] = Field(alias="fields", default=None),
        include_locale: Optional[bool] = Field(alias="include_locale", default=None),
        next_page: Optional[str] = Field(alias="nextPage", default=None),
        page_size: Optional[int] = Field(alias="pageSize", default=None),
        team_id: Optional[str] = Field(alias="team_id", default=None),
    ) -> Optional[Union[DefaultError, list["ListAllUsers"]]]:
        return await _list_all_users_async(
            client=self.client,
            fields=fields,
            include_locale=include_locale,
            next_page=next_page,
            page_size=page_size,
            team_id=team_id,
        )

    def send_message_to_user(
        self,
        *,
        body: SendMessageToUserRequest,
        send_as: str = Field(alias="send_as", default="bot"),
        send_as_lookup: Any,
    ) -> Optional[Union[DefaultError, SendMessageToUserResponse]]:
        return _send_message_to_user(
            client=self.client,
            body=body,
            send_as=send_as,
            send_as_lookup=send_as_lookup,
        )

    async def send_message_to_user_async(
        self,
        *,
        body: SendMessageToUserRequest,
        send_as: str = Field(alias="send_as", default="bot"),
        send_as_lookup: Any,
    ) -> Optional[Union[DefaultError, SendMessageToUserResponse]]:
        return await _send_message_to_user_async(
            client=self.client,
            body=body,
            send_as=send_as,
            send_as_lookup=send_as_lookup,
        )

    def set_channel_topic(
        self,
        *,
        body: SetChannelTopicRequest,
    ) -> Optional[Union[DefaultError, SetChannelTopicResponse]]:
        return _set_channel_topic(
            client=self.client,
            body=body,
        )

    async def set_channel_topic_async(
        self,
        *,
        body: SetChannelTopicRequest,
    ) -> Optional[Union[DefaultError, SetChannelTopicResponse]]:
        return await _set_channel_topic_async(
            client=self.client,
            body=body,
        )

    def get_user_by_email(
        self,
        users_by_email_id: str,
        *,
        by: str = Field(alias="By", default="Email"),
        user_id: Optional[str] = Field(alias="UserID", default=None),
        include_locale: Optional[bool] = Field(alias="include_locale", default=None),
    ) -> Optional[Union[DefaultError, GetUserByEmailResponse]]:
        return _get_user_by_email(
            client=self.client,
            users_by_email_id=users_by_email_id,
            by=by,
            user_id=user_id,
            include_locale=include_locale,
        )

    async def get_user_by_email_async(
        self,
        users_by_email_id: str,
        *,
        by: str = Field(alias="By", default="Email"),
        user_id: Optional[str] = Field(alias="UserID", default=None),
        include_locale: Optional[bool] = Field(alias="include_locale", default=None),
    ) -> Optional[Union[DefaultError, GetUserByEmailResponse]]:
        return await _get_user_by_email_async(
            client=self.client,
            users_by_email_id=users_by_email_id,
            by=by,
            user_id=user_id,
            include_locale=include_locale,
        )
