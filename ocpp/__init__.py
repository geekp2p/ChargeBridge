"""Core OCPP abstractions used by both JSON and SOAP transports."""

from .domain import (
    BootNotificationRequest,
    BootNotificationResponse,
    StatusNotificationRequest,
    StatusNotificationResponse,
)
from .service import ChargePointService

__all__ = [
    "BootNotificationRequest",
    "BootNotificationResponse",
    "StatusNotificationRequest",
    "StatusNotificationResponse",
    "ChargePointService",
]