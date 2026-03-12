import statistics
from dataclasses import dataclass
from typing import Any

from reader import CSVAnalytics


class UnknownMethodException(Exception):
    pass


@dataclass
class ActionData:
    headers: list[str] | None
    data: list[Any]


class Actions:

    @classmethod
    def execute(cls, action_name, *args, **kwargs) -> ActionData:
        method_name = f'execute_{'_'.join(action_name.split('-'))}'
        if hasattr(cls, method_name):
            action = getattr(cls, method_name)
            return action(*args, **kwargs)
        raise UnknownMethodException(f'{method_name}. The called action does not exist.')

    @staticmethod
    def execute_coffee_spent(filenames: list[str]) -> ActionData:
        columns = ['student', 'coffee_spent']
        analytic = CSVAnalytics()
        for filename in filenames:
            analytic.load(filename)
        total_coffee_spent = analytic.aggregate(*columns, statistics.median).sort(lambda x: -x['coffee_spent'])
        return ActionData(
            headers=columns,
            data=total_coffee_spent.to_list(columns)
        )
