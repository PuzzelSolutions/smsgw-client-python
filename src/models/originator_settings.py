from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .originator_type import OriginatorType

@dataclass
class OriginatorSettings(Parsable):
    # The originator property
    originator: Optional[str] = None
    # The originatorType property
    originator_type: Optional[OriginatorType] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> OriginatorSettings:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: OriginatorSettings
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return OriginatorSettings()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .originator_type import OriginatorType

        from .originator_type import OriginatorType

        fields: dict[str, Callable[[Any], None]] = {
            "originator": lambda n : setattr(self, 'originator', n.get_str_value()),
            "originatorType": lambda n : setattr(self, 'originator_type', n.get_enum_value(OriginatorType)),
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
        writer.write_str_value("originator", self.originator)
        writer.write_enum_value("originatorType", self.originator_type)
    

