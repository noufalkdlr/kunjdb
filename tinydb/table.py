from typing import Mapping

from tinydb.storages import Storage


class Document(dict):
    def __init__(self, value: Mapping, doc_id: int):
        super().__init__(value)
        self.doc_id = doc_id


class Table:
    document_class = Document

    def __init__(
        self,
        storage: Storage,
        name: str,
        persist_empty: bool = False,
    ):
        self._storage = storage
        self.name = name
        self._next_id = None

    def insert(self, document: Mapping):

        if not isinstance(document, Mapping):
            raise ValueError("Document is not a Mapping")

        if isinstance(document, self.document_class):
            doc_id = document.doc_id

            self._next_id = None
        else:
            doc_id = self._get_next_id()

        def updater(table):
            table[doc_id] = dict(document)

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

        tables[self.name] = {str(doc_id): doc for doc_id, doc in table.items()}

        self._storage.write(tables)
