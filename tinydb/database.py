from .storages import JSONStorage
from .table import Table


class TinyDB:
    default_storage_class = JSONStorage
    table_class = Table

    def __init__(self, *args, **kwargs) -> None:
        storage = kwargs.pop("storage", self.default_storage_class)
        self._storage = storage(*args, **kwargs)

    def table(self, **kwargs):
        self.table_class(**kwargs)
