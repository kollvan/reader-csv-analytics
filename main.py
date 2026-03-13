import argparse
import glob

import tabulate

from action import Actions


def get_files(ext: str = 'csv') -> list[str]:
    '''Returns a list of *.csv files in the current directory.'''
    return glob.glob(f'*.{ext}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--files',
                        dest='filenames',
                        nargs='*',
                        default=get_files(),
                        help='path to the files on which the report is generated')
    parser.add_argument('--report',
                        dest='action_name',
                        choices=Actions.allow_actions,
                        default='median-coffee',
                        nargs='?',
                        help='the type of report that will be generated')
    params = vars(parser.parse_args())
    data = Actions.execute(**params)
    print(data)
    print(tabulate.tabulate(data.data, headers=data.headers))
