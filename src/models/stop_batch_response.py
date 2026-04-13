from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .stopped_message_response import StoppedMessageResponse

@dataclass
class StopBatchResponse(Parsable):
    # The clientBatchReference property
    client_batch_reference: Optional[str] = None
    # The serviceId property
    service_id: Optional[int] = None
    # The stoppedMessages property
    stopped_messages: Optional[list[StoppedMessageResponse]] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> StopBatchResponse:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: StopBatchResponse
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return StopBatchResponse()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .stopped_message_response import StoppedMessageResponse

        from .stopped_message_response import StoppedMessageResponse

        fields: dict[str, Callable[[Any], None]] = {
            "clientBatchReference": lambda n : setattr(self, 'client_batch_reference', n.get_str_value()),
            "serviceId": lambda n : setattr(self, 'service_id', n.get_int_value()),
            "stoppedMessages": lambda n : setattr(self, 'stopped_messages', n.get_collection_of_object_values(StoppedMessageResponse)),
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
        writer.write_str_value("clientBatchReference", self.client_batch_reference)
        writer.write_int_value("serviceId", self.service_id)
        writer.write_collection_of_object_values("stoppedMessages", self.stopped_messages)
    

