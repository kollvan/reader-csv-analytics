import statistics

import pytest
from pytest_mock import mocker

from action import Actions, ActionData, UnknownMethodException
from reader import CSVAnalytics


@pytest.fixture
def preload_mock_analytic(request, mocker):
    data = request.param
    mock_analytic = mocker.Mock(spec=CSVAnalytics)
    mock_aggregate_result = mocker.Mock(spec=CSVAnalytics)

    mock_analytic.aggregate.return_value = mock_aggregate_result
    mock_aggregate_result.sort.return_value = mock_aggregate_result
    mock_aggregate_result.to_list.return_value = data

    return {'mock': mock_analytic, 'data': data}


@pytest.mark.parametrize(
    ('filenames', 'preload_mock_analytic'),
    (
            (('math.csv',), [['Алексей Смирнов', 475], ['Дарья Петрова', 225]]),
            (('physics.csv',), [['Алексей Смирнов', 580], ['Дарья Петрова', 280], ['Мария Соколова', 140]]),
            (('math.csv', 'physics.csv'), [['Алексей Смирнов', 500], ['Дарья Петрова', 250], ['Мария Соколова', 140]])
    ),
    indirect=['preload_mock_analytic']
)
def test_execute_median_coffee(preload_mock_analytic, mocker, filenames):
    preload_mock = preload_mock_analytic['mock']
    data = preload_mock_analytic['data']
    headers = ['student', 'median_coffee']
    mocker.patch('action.CSVAnalytics', return_value=preload_mock)

    result = Actions.execute_median_coffee(filenames)

    assert preload_mock.load.call_count == len(filenames)

    preload_mock.aggregate.assert_called_once_with(
        'student',
        'coffee_spent',
        aggregation_func=statistics.median
    )

    mock_aggregate_result = preload_mock.aggregate.return_value

    mock_aggregate_result.sort.assert_called_once()

    mock_aggregate_result.to_list.assert_called_once_with(
        ['student', 'coffee_spent']
    )

    assert isinstance(result, ActionData)
    assert result.data == data
    assert result.headers == headers


@pytest.fixture
def preload_mock_execute_actions(request, mocker):
    action_name = '_'.join(request.param.split('-'))
    mock_action = mocker.Mock(return_value=ActionData(headers=['student'], data=[]))
    mocker.patch.object(Actions, f'execute_{action_name}', mock_action)
    return {
        'action_name': action_name,
        'mock': mock_action,
        '*args': [1, 2, 3],
        '**kwargs': {'name': 'name'}
    }


@pytest.mark.parametrize(
    ('preload_mock_execute_actions',),
    (
            ('median-coffee',),
    ),
    indirect=['preload_mock_execute_actions']
)
def test_execute_function(preload_mock_execute_actions, mocker):
    action_name = preload_mock_execute_actions['action_name']
    params_lst = preload_mock_execute_actions['*args']
    params_dict = preload_mock_execute_actions['**kwargs']
    mock_action = preload_mock_execute_actions['mock']
    result = Actions.execute(action_name, *params_lst, **params_dict)

    mock_action.assert_called_once_with(*params_lst, **params_dict)
    assert result is mock_action.return_value


@pytest.mark.parametrize(
    ('action_name',),
    (
            ('median-coffee2',),
    ),
)
def test_execute_incorrect_function(action_name):
    with pytest.raises(UnknownMethodException):
        Actions.execute(action_name)
