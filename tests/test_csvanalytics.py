import statistics

import pytest

from reader import CSVAnalytics
from tests.base import FILES_DIR


@pytest.mark.parametrize(
    ('filenames', 'number_records'),
    (
            (['physics.csv'], 3),
            (['math.csv', 'physics.csv'], 7),
    )
)
def test_load_csv(filenames, number_records):
    keys = {'student', 'date', 'coffee_spent', 'sleep_hours', 'study_hours', 'mood', 'exam'}

    analytic = CSVAnalytics()
    for filename in filenames:
        analytic.load(f'{FILES_DIR}\\{filename}')
    assert len(analytic._records) == number_records
    assert type(analytic._records[0]) is dict
    assert analytic._records[0].keys() == keys


@pytest.mark.parametrize(
    ('filename', 'exception_type'),
    (
            ('dontexist.csv', FileNotFoundError),
    )
)
def test_load_csv_with_incorrect_filename(filename, exception_type):
    with pytest.raises(exception_type):
        analytic = CSVAnalytics()
        analytic.load(f'{FILES_DIR}\\{filename}')


@pytest.fixture
def preload_analytics() -> CSVAnalytics:
    analytic = CSVAnalytics()
    analytic.load(f'{FILES_DIR}\\math.csv')
    return analytic


@pytest.mark.usefixtures('preload_analytics')
class TestWithPreloadAnalytics:

    @pytest.mark.parametrize(
        ('agr_function', 'expected_value'),
        (
                (statistics.median, 475),
                (statistics.mean, 475),
                (sum, 950)
        )
    )
    def test_aggregate_function(self, preload_analytics, agr_function, expected_value):
        group_by = 'student'
        target_field = 'coffee_spent'
        analytic = preload_analytics.aggregate(group_by, target_field, aggregation_func=agr_function)
        assert isinstance(analytic, CSVAnalytics)
        for record in analytic._records:
            if 'Алексей Смирнов' in record[group_by]:
                assert record[target_field] == expected_value

    @pytest.mark.parametrize(
        ('filter_condition', 'sorting_field', 'sorting_result'),
        (
                (lambda x: x['coffee_spent'], 'coffee_spent', ('200', '250', '450', '500')),
                (lambda x: float(x['sleep_hours']), 'sleep_hours', ('4.0', '4.5', '6.5', '7.0'))
        )
    )
    def test_sort_function(self, preload_analytics, filter_condition, sorting_field, sorting_result):
        analytic = preload_analytics.sort(key=filter_condition)
        assert analytic is preload_analytics
        for i, record in enumerate(preload_analytics._records):
            assert record[sorting_field] == sorting_result[i]
