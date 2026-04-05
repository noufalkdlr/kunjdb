class JSONStorage(Storage):
    def __init__(
        self, path: str, create_dirs=False, encoding=None, access_mode="r+", **kwargs
    ):

        super().__init__()

        self._mode = access_mode
        self.kwargs = kwargs

        if access_mode not in ("r", "rb", "r+", "rb+"):
            warnings.warn(
                "Using an `access_mode` other than 'r', 'rb', 'r+' "
                "or 'rb+' can cause data loss or corruption"
            )

        if any([character in self._mode for character in ("+", "w", "a")]):
            touch(path, create_dirs=create_dirs)

        self._handle = open(path, mode=self._mode, encoding=encoding)

    def close(self) -> None:
        self._handle.close()

    def read(self) -> Optional[Dict[str, Dict[str, Any]]]:
        self._handle.seek(0, os.SEEK_END)
        size = self._handle.tell()

        if not size:
            return None
        else:
            self._handle.seek(0)

            return json.load(self._handle)

    def write(self, data: Dict[str, Dict[str, Any]]):
        self._handle.seek(0)

        serialized = json.dumps(data, **self.kwargs)

        try:
            self._handle.write(serialized)
        except io.UnsupportedOperation:
            raise IOError(
                'Cannot write to the database. Access mode is "{0}"'.format(self._mode)
            )

        self._handle.flush()
        os.fsync(self._handle.fileno())

        self._handle.truncate()
