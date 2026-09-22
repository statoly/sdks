from __future__ import annotations
import datetime
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union
from uuid import UUID

if TYPE_CHECKING:
    from .metadata import Metadata
    from .monitor_status import Monitor_status
    from .monitor_type import Monitor_type

@dataclass
class Monitor(Parsable):
    # Whether the owner has the monitor switched on
    active: Optional[bool] = None
    # The createdAt property
    created_at: Optional[datetime.datetime] = None
    # Monitor identifier
    id: Optional[UUID] = None
    # User-defined key/value pairs
    metadata: Optional[list[Metadata]] = None
    # Result of the latest check, absent until the monitor has run
    status: Optional[Monitor_status] = None
    # Set while the billing sync holds the monitor because the organization has no entitlement. Independent of active, which stays the owner's own choice.
    suspended_at: Optional[datetime.datetime] = None
    # Display name
    title: Optional[str] = None
    # What the monitor checks
    type: Optional[Monitor_type] = None
    # The updatedAt property
    updated_at: Optional[datetime.datetime] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> Monitor:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: Monitor
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return Monitor()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .metadata import Metadata
        from .monitor_status import Monitor_status
        from .monitor_type import Monitor_type

        from .metadata import Metadata
        from .monitor_status import Monitor_status
        from .monitor_type import Monitor_type

        fields: dict[str, Callable[[Any], None]] = {
            "active": lambda n : setattr(self, 'active', n.get_bool_value()),
            "createdAt": lambda n : setattr(self, 'created_at', n.get_datetime_value()),
            "id": lambda n : setattr(self, 'id', n.get_uuid_value()),
            "metadata": lambda n : setattr(self, 'metadata', n.get_collection_of_object_values(Metadata)),
            "status": lambda n : setattr(self, 'status', n.get_enum_value(Monitor_status)),
            "suspendedAt": lambda n : setattr(self, 'suspended_at', n.get_datetime_value()),
            "title": lambda n : setattr(self, 'title', n.get_str_value()),
            "type": lambda n : setattr(self, 'type', n.get_enum_value(Monitor_type)),
            "updatedAt": lambda n : setattr(self, 'updated_at', n.get_datetime_value()),
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
        writer.write_bool_value("active", self.active)
        writer.write_datetime_value("createdAt", self.created_at)
        writer.write_uuid_value("id", self.id)
        writer.write_collection_of_object_values("metadata", self.metadata)
        writer.write_enum_value("status", self.status)
        writer.write_datetime_value("suspendedAt", self.suspended_at)
        writer.write_str_value("title", self.title)
        writer.write_enum_value("type", self.type)
        writer.write_datetime_value("updatedAt", self.updated_at)
    

