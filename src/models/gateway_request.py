from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .message import Message

@dataclass
class GatewayRequest(Parsable):
    # The batchReference property
    batch_reference: Optional[str] = None
    # The message property
    message: Optional[list[Message]] = None
    # The password property
    password: Optional[str] = None
    # The serviceId property
    service_id: Optional[int] = None
    # The username property
    username: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> GatewayRequest:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: GatewayRequest
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return GatewayRequest()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .message import Message

        from .message import Message

        fields: dict[str, Callable[[Any], None]] = {
            "batchReference": lambda n : setattr(self, 'batch_reference', n.get_str_value()),
            "message": lambda n : setattr(self, 'message', n.get_collection_of_object_values(Message)),
            "password": lambda n : setattr(self, 'password', n.get_str_value()),
            "serviceId": lambda n : setattr(self, 'service_id', n.get_int_value()),
            "username": lambda n : setattr(self, 'username', n.get_str_value()),
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
        writer.write_str_value("batchReference", self.batch_reference)
        writer.write_collection_of_object_values("message", self.message)
        writer.write_str_value("password", self.password)
        writer.write_int_value("serviceId", self.service_id)
        writer.write_str_value("username", self.username)
    

