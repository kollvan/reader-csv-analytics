from __future__ import annotations

import csv
from typing import Callable, Self, Iterable, Any


class CSVAnalytics:
    def __init__(self, data: list[dict[str, Any]] | None = None):
        self._records: list[dict[str, Any]] = data.copy() if data else []

    def load(self, filename: str):
        '''Loads a csv file into memory.'''
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for record in reader:
                self._records.append(record)

    def aggregate(
            self,
            group_by_column: str,
            target_field: str,
            *,
            aggregation_func: Callable[[Iterable[Any]], Any],
            data_type: Callable = int
    ) -> CSVAnalytics:
        '''
        Groups records by the specified column and applies an aggregation function to the target field.
        Parameters
        ----------
        group_by_column : str
            The name of the column for grouping records. Must exist in the data.
        target_field : str
            The name of the column whose values will be aggregated. Must exist in the data.
        aggregation_func : Callable[[Iterable[Any]], Any]
            Function for aggregating values within a group.
        data_type : Callable, default=int
            Function for converting data types before aggregation.
        '''
        agr_fields = {}
        for record in self._records:
            agr_fields.setdefault(record[group_by_column], []).append(data_type(record[target_field]))
        return CSVAnalytics(
            [{group_by_column: name, target_field: aggregation_func(agr_fields[name])} for name in agr_fields]
        )

    def sort(self, key: Callable) -> Self:
        '''Sorts records according to the key function.'''

        self._records.sort(key=key)
        return self

    def to_list(self, fields: list[str]) -> list[list[str]]:
        '''Returns a list of records. The fields parameter specifies which record fields are returned in the list.'''
        lst = []
        for record in self._records:
            lst_record = []
            for field in fields:
                lst_record.append(record[field])
            lst.append(lst_record)
        return lst
