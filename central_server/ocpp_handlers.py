"""Handlers for converting external identifiers to internal VIDs."""

from services.vid_manager import VIDManager

vid_manager = VIDManager()


def to_vid(source_type: str, source_value: str) -> int:
    """Convert incoming identifier to a VID using :class:`VIDManager`.

    Parameters
    ----------
    source_type: str
        Type of the identifier, e.g. 'mac', 'id_tag', 'vin', 'phone'.
    source_value: str
        Value of the identifier.

    Returns
    -------
    int
        The VID associated with the identifier.
    """
    return vid_manager.get_or_create_vid(source_type, source_value)


async def on_data_transfer(request, session_context):
    """Handle a :class:`~ocpp.v16.datatransfer.DataTransfer` request.

    Extracts the ``vendor_id`` and ``data`` fields from the incoming request
    and, when the vendor id indicates a Mac identifier (``"MacID"``), resolves
    the provided MacID to a VID. The resulting VID is stored temporarily in the
    supplied ``session_context`` for later use during Authorize or
    StartTransaction calls.

    Parameters
    ----------
    request:
        DataTransfer request object containing ``vendor_id`` and ``data``.
    session_context: dict
        Mutable mapping used to keep per-session state.

    Returns
    -------
    dict
        Empty dictionary acknowledging the DataTransfer.
    """
    vendor_id = getattr(request, "vendor_id", None)
    data = getattr(request, "data", None)

    if vendor_id == "MacID" and data:
        vid = vid_manager.get_or_create_vid("mac", data)
        session_context["vid"] = vid

    return {}