class VIDManager:
    """Manage VID mappings from various source identifiers.

    Maintains mappings between MacID, idTag, VIN, phone numbers and an
    internally generated VID (Vehicle Identifier). Multiple identifiers can
    map to the same VID by requesting the VID through :meth:`get_or_create_vid`.
    """

    def __init__(self):
        # Maps (source_type, source_value) -> VID
        self._source_to_vid = {}
        # Reverse mapping VID -> {source_type: source_value}
        self._vid_to_sources = {}
        self._counter = 1

    def get_or_create_vid(self, source_type: str, source_value: str) -> int:
        """Return an existing VID for the source or create a new one.

        Parameters
        ----------
        source_type: str
            Identifier type such as 'mac', 'id_tag', 'vin' or 'phone'.
        source_value: str
            The identifier value.

        Returns
        -------
        int
            The VID corresponding to the given identifier.
        """
        key = (source_type, source_value)
        if key in self._source_to_vid:
            return self._source_to_vid[key]

        vid = self._counter
        self._counter += 1
        self._source_to_vid[key] = vid
        self._vid_to_sources.setdefault(vid, {})[source_type] = source_value
        return vid