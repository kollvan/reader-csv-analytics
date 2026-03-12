import csv
from typing import Callable


class CSVAnalytics:
    def __init__(self, data: list[dict[any]] | None = None):
        self._records = data if data else []

    def load(self, filename: str):
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for record in reader:
                self._records.append(record)

    def aggregate(self, primary_field, agr_field, agg: Callable, type_agr_field: Callable = int):
        agr_fields = {}
        for record in self._records:
            agr_fields.setdefault(record[primary_field], []).append(type_agr_field(record[agr_field]))
        return CSVAnalytics([{primary_field: name, agr_field: agg(agr_fields[name])} for name in agr_fields])

    def sort(self, key):
        self._records.sort(key=key)
        return self

    def to_list(self, fields: list[str]):
        lst = []
        for record in self._records:
            lst_record = []
            for field in fields:
                lst_record.append(record[field])
            lst.append(lst_record)
        return lst
