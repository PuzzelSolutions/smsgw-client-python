from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class MessageStatus(Parsable):
    # The clientReference property
    client_reference: Optional[str] = None
    # The messageId property
    message_id: Optional[str] = None
    # The recipient property
    recipient: Optional[str] = None
    # The sequenceIndex property
    sequence_index: Optional[int] = None
    # The sessionId property
    session_id: Optional[str] = None
    # The statusCode property
    status_code: Optional[int] = None
    # The statusMessage property
    status_message: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> MessageStatus:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: MessageStatus
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return MessageStatus()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "clientReference": lambda n : setattr(self, 'client_reference', n.get_str_value()),
            "messageId": lambda n : setattr(self, 'message_id', n.get_str_value()),
            "recipient": lambda n : setattr(self, 'recipient', n.get_str_value()),
            "sequenceIndex": lambda n : setattr(self, 'sequence_index', n.get_int_value()),
            "sessionId": lambda n : setattr(self, 'session_id', n.get_str_value()),
            "statusCode": lambda n : setattr(self, 'status_code', n.get_int_value()),
            "statusMessage": lambda n : setattr(self, 'status_message', n.get_str_value()),
        }
        return fields
    
    def serialize(self,writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        param writer: Serialization writer to use to serialize this model
        Returns: None
        """
        if writer is None:
            raise TypeError("writer cannot be null.")
        writer.write_str_value("clientReference", self.client_reference)
        writer.write_str_value("messageId", self.message_id)
        writer.write_str_value("recipient", self.recipient)
        writer.write_int_value("sequenceIndex", self.sequence_index)
        writer.write_str_value("sessionId", self.session_id)
        writer.write_int_value("statusCode", self.status_code)
        writer.write_str_value("statusMessage", self.status_message)
    

