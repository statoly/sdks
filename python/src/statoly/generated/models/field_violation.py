from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class FieldViolation(Parsable):
    # The constraint property
    constraint: Optional[str] = None
    # The expected property
    expected: Optional[str] = None
    # The field property
    field: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> FieldViolation:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: FieldViolation
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return FieldViolation()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "constraint": lambda n : setattr(self, 'constraint', n.get_str_value()),
            "expected": lambda n : setattr(self, 'expected', n.get_str_value()),
            "field": lambda n : setattr(self, 'field', n.get_str_value()),
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
        writer.write_str_value("constraint", self.constraint)
        writer.write_str_value("expected", self.expected)
        writer.write_str_value("field", self.field)
    

