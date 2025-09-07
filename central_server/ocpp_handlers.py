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