from tinydb.storages import Storage


class Table:
    def __init__(
        self,
        storage: Storage,
        name: str,
        persist_empty: bool = False,
    ):
        self._storage = storage
        self.name = name
        self._next_id = None


    def insert(self, document: dict) -> int:

        doc_id = self._get_next_id()

        def updater(table: dict):
            table[doc_id] = document
            print(table)


        self._update_table(updater)
        return doc_id


    def _get_next_id(self):
        if self._next_id is not None:
            next_id = self._next_id
            self._next_id = next_id + 1
            return next_id

        table = self._read_table()
        if not table:
            next_id = 1
            self._next_id = next_id + 1
            return next_id

        max_id = max(int(i) for i in table.keys())
        next_id = max_id + 1
        self._next_id = next_id + 1
        return next_id


    def _read_table(self):
        tables = self._storage.read()
        if tables is None:
            return {}
        try:
            table = tables[self.name]
        except KeyError:
            return {}
        return table


    def _update_table(self, updater):

        tables = self._storage.read()

        if tables is None:
            tables = {}


        try:
            raw_table = tables[self.name]
        except KeyError:
            raw_table = {}


        table = {int(doc_id): doc for doc_id, doc in raw_table.items()}


        updater(table)



        tables[self.name] = {
            str(doc_id): doc
            for doc_id, doc in table.items()
        }


        self._storage.write(tables)
