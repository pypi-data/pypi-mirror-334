"""ServiceState model for tracking service execution states."""

from typing import Optional

from sqlalchemy import JSON, Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel
from .enums import ServiceState


class ServiceStateModel(BaseModel):
    """Model for tracking service execution states."""

    __abstract__ = False

    # Base identifiers
    service_name: Mapped[str] = mapped_column(
        String(length=100),
        nullable=False,
        comment="Name of the service",
    )
    instance_id: Mapped[str] = mapped_column(
        String(length=100),
        nullable=False,
        comment="Instance identifier for the service run",
    )

    # State tracking
    service_state: Mapped[ServiceState] = mapped_column(
        Enum(ServiceState),
        nullable=False,
        default=ServiceState.PENDING,
        comment="Current state of the service",
    )
    error_message: Mapped[Optional[str]] = mapped_column(
        String(length=1000), nullable=True, comment="Error message if service failed"
    )
    service_result: Mapped[Optional[dict]] = mapped_column(
        JSON, nullable=True, comment="Result data from the service execution"
    )

    def __repr__(self) -> str:
        """String representation of the ServiceState."""
        return (
            f"<ServiceState(service={self.service_name}, "
            f"instance={self.instance_id}, "
            f"state={self.service_state.value})>"
        )
