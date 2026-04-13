from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .gas_settings import GasSettings
    from .originator_settings import OriginatorSettings
    from .parameter import Parameter
    from .send_window import SendWindow

@dataclass
class Settings(Parsable):
    # The age property
    age: Optional[int] = None
    # The autoDetectEncoding property
    auto_detect_encoding: Optional[bool] = None
    # The differentiator property
    differentiator: Optional[str] = None
    # The gasSettings property
    gas_settings: Optional[GasSettings] = None
    # The invoiceNode property
    invoice_node: Optional[str] = None
    # The newSession property
    new_session: Optional[bool] = None
    # The originatorSettings property
    originator_settings: Optional[OriginatorSettings] = None
    # The parameter property
    parameter: Optional[list[Parameter]] = None
    # The priority property
    priority: Optional[int] = None
    # The sendWindow property
    send_window: Optional[SendWindow] = None
    # The sessionId property
    session_id: Optional[str] = None
    # The validity property
    validity: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> Settings:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: Settings
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return Settings()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .gas_settings import GasSettings
        from .originator_settings import OriginatorSettings
        from .parameter import Parameter
        from .send_window import SendWindow

        from .gas_settings import GasSettings
        from .originator_settings import OriginatorSettings
        from .parameter import Parameter
        from .send_window import SendWindow

        fields: dict[str, Callable[[Any], None]] = {
            "age": lambda n : setattr(self, 'age', n.get_int_value()),
            "autoDetectEncoding": lambda n : setattr(self, 'auto_detect_encoding', n.get_bool_value()),
            "differentiator": lambda n : setattr(self, 'differentiator', n.get_str_value()),
            "gasSettings": lambda n : setattr(self, 'gas_settings', n.get_object_value(GasSettings)),
            "invoiceNode": lambda n : setattr(self, 'invoice_node', n.get_str_value()),
            "newSession": lambda n : setattr(self, 'new_session', n.get_bool_value()),
            "originatorSettings": lambda n : setattr(self, 'originator_settings', n.get_object_value(OriginatorSettings)),
            "parameter": lambda n : setattr(self, 'parameter', n.get_collection_of_object_values(Parameter)),
            "priority": lambda n : setattr(self, 'priority', n.get_int_value()),
            "sendWindow": lambda n : setattr(self, 'send_window', n.get_object_value(SendWindow)),
            "sessionId": lambda n : setattr(self, 'session_id', n.get_str_value()),
            "validity": lambda n : setattr(self, 'validity', n.get_int_value()),
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
        writer.write_int_value("age", self.age)
        writer.write_bool_value("autoDetectEncoding", self.auto_detect_encoding)
        writer.write_str_value("differentiator", self.differentiator)
        writer.write_object_value("gasSettings", self.gas_settings)
        writer.write_str_value("invoiceNode", self.invoice_node)
        writer.write_bool_value("newSession", self.new_session)
        writer.write_object_value("originatorSettings", self.originator_settings)
        writer.write_collection_of_object_values("parameter", self.parameter)
        writer.write_int_value("priority", self.priority)
        writer.write_object_value("sendWindow", self.send_window)
        writer.write_str_value("sessionId", self.session_id)
        writer.write_int_value("validity", self.validity)
    

