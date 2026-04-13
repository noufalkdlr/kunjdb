from .storages import JSONStorage
from .table import Table


class TinyDB:
    default_storage_class = JSONStorage
    table_class = Table

    def __init__(self, *args, **kwargs) -> None:
        storage = kwargs.pop("storage", self.default_storage_class)
        self._storage = storage(*args, **kwargs)
        self._tables = {}

    def table(self, name: str, **kwargs):
        if not name in self._tables:
            table = self.table_class(self._storage, name, **kwargs)
            self._tables[name]= table
        
        return self._tables[name]