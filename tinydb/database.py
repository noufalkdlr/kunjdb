from .storages import JSONStorage
from .table import Table


class TinyDB:
    default_storage_class = JSONStorage
    table_class = Table
    default_table_name = "_default"

    def __init__(self, *args, **kwargs) -> None:
        storage = kwargs.pop("storage", self.default_storage_class)
        self._storage = storage(*args, **kwargs)
        self._tables = {}

    def table(self, name: str, **kwargs):
        if name not in self._tables:
            table = self.table_class(self._storage, name, **kwargs)
            self._tables[name] = table

        return self._tables[name]

    def __getattr__(self, name):
        default_table = self.table(self.default_table_name)
        return getattr(default_table, name)
