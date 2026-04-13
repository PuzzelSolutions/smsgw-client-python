from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .settings import Settings

@dataclass
class Message(Parsable):
    # The clientReference property
    client_reference: Optional[str] = None
    # The content property
    content: Optional[str] = None
    # The price property
    price: Optional[int] = None
    # The priceXml property
    price_xml: Optional[str] = None
    # The recipient property
    recipient: Optional[str] = None
    # The settings property
    settings: Optional[Settings] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> Message:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: Message
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return Message()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .settings import Settings

        from .settings import Settings

        fields: dict[str, Callable[[Any], None]] = {
            "clientReference": lambda n : setattr(self, 'client_reference', n.get_str_value()),
            "content": lambda n : setattr(self, 'content', n.get_str_value()),
            "price": lambda n : setattr(self, 'price', n.get_int_value()),
            "priceXml": lambda n : setattr(self, 'price_xml', n.get_str_value()),
            "recipient": lambda n : setattr(self, 'recipient', n.get_str_value()),
            "settings": lambda n : setattr(self, 'settings', n.get_object_value(Settings)),
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
        writer.write_str_value("content", self.content)
        writer.write_int_value("price", self.price)
        writer.write_str_value("priceXml", self.price_xml)
        writer.write_str_value("recipient", self.recipient)
        writer.write_object_value("settings", self.settings)
    

