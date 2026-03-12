import argparse
import glob

import tabulate

from action import Actions


def get_files(ext: str = 'csv') -> list[str]:
    return glob.glob(f'*.{ext}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', dest='filenames', nargs='*')
    parser.add_argument('--report', dest='action_name', default='median-coffee', nargs='?')
    params = vars(parser.parse_args())
    if not params['filenames']:
        params['filenames'] = get_files()
    data = Actions.execute(**params)
    print(
        tabulate.tabulate(data.data, headers=data.headers)
    )
