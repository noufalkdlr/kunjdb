from tinydb.storages import Storage


class Table:
    def __init__(
        self,
        storage: Storage,
        name: str,
        persist_empty: bool = False,
    ):
        self._storage = storage
        self._name = name
        print(f'{self._name} table is ready')
