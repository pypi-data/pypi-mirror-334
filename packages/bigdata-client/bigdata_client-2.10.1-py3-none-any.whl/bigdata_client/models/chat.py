from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PrivateAttr, computed_field, field_validator

from bigdata_client.connection_protocol import BigdataConnectionProtocol
from bigdata_client.constants import MAX_CHAT_QUESTION_LENGTH, MIN_CHAT_QUESTION_LENGTH
from bigdata_client.enum_utils import StrEnum
from bigdata_client.exceptions import BigdataClientChatInvalidQuestion


class ChatScope(StrEnum):
    EARNING_CALLS = "transcripts"
    FILES = "files"
    NEWS = "news"
    REGULATORY_FILINGS = "filings"


class ChatInteraction(BaseModel):
    """Represents a single interaction with chat"""

    question: str
    answer: str
    interaction_timestamp: str
    date_created: datetime
    last_updated: datetime
    scope: Optional[ChatScope] = None

    @field_validator("scope", mode="before")
    @classmethod
    def validate_scope(cls, value):
        if isinstance(value, str):
            try:
                return ChatScope(value)
            except ValueError:
                return None
        return value


class Chat(BaseModel):
    id: str
    name: str
    user_id: str
    date_created: datetime
    last_updated: datetime

    @computed_field
    @property
    def interactions(self) -> list[ChatInteraction]:
        if not self._loaded:
            self.reload_from_server()
        return self._interactions

    _api_connection: BigdataConnectionProtocol
    _interactions: list[ChatInteraction]
    _loaded: bool

    def __init__(
        self,
        _api_connection: BigdataConnectionProtocol,
        _interactions: Optional[list[ChatInteraction]],
        _loaded: bool = False,
        **values
    ):
        super().__init__(**values)
        self._api_connection = _api_connection
        self._loaded = _loaded

        if _interactions is not None:
            self._interactions = _interactions

    def ask(
        self, question: str, *, scope: Optional[ChatScope] = None
    ) -> ChatInteraction:
        """Ask a question in the chat"""
        self._validate_question(question)
        chat_scope = scope.value if scope else None
        value = self._api_connection.ask_chat(self.id, question, scope=chat_scope)
        answer = value.content_block.get("value", "")

        from bigdata_client.api.chat import ChatInteraction as ApiChatInteraction

        answer = ApiChatInteraction._strip_references(answer)
        now = datetime.utcnow()
        interation = ChatInteraction(
            question=question,
            answer=answer,
            interaction_timestamp=value.interaction_timestamp,
            date_created=now,
            last_updated=now,
            scope=scope,
        )
        self._interactions.append(interation)
        return interation

    def reload_from_server(self):
        chat = self._api_connection.get_chat(self.id).to_chat_model(
            self._api_connection
        )
        self.name = chat.name
        self.user_id = chat.user_id
        self.date_created = chat.date_created
        self.last_updated = chat.last_updated
        self._interactions = chat._interactions
        self._loaded = True

    def delete(self):
        """Delete the chat"""
        self._api_connection.delete_chat(self.id)

    @staticmethod
    def _validate_question(question: str):
        message_length = len(question or "")
        if not (MIN_CHAT_QUESTION_LENGTH < message_length < MAX_CHAT_QUESTION_LENGTH):
            raise BigdataClientChatInvalidQuestion(message_length)
