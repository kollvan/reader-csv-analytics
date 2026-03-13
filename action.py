import statistics
from dataclasses import dataclass
from typing import Any, Iterable

from reader import CSVAnalytics


class UnknownMethodException(Exception):
    pass


@dataclass
class ActionData:
    headers: list[str] | None
    data: list[Any]


class Actions:
    allow_actions: list[str] = ['median-coffee']

    @classmethod
    def execute(cls, action_name: str, *args, **kwargs) -> ActionData:
        '''Execute an action with the "execute_" prefix by action_name.'''
        method_name = f'execute_{'_'.join(action_name.split('-'))}'
        if hasattr(cls, method_name):
            action = getattr(cls, method_name)
            return action(*args, **kwargs)
        raise UnknownMethodException(f'{method_name}. The called action does not exist.', cls.allow_actions)

    @classmethod
    def execute_median_coffee(cls, filenames: Iterable[str]) -> ActionData:
        '''Executing the action to generate the median_coffee report'''
        columns = ['student', 'coffee_spent']
        analytic = CSVAnalytics()
        for filename in filenames:
            analytic.load(filename)
        total_coffee_spent = analytic.aggregate(
            *columns,
            aggregation_func=statistics.median
        ).sort(lambda x: -x['coffee_spent'])
        return ActionData(
            headers=['student', 'median_coffee'],
            data=total_coffee_spent.to_list(columns)
        )
