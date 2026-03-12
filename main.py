import argparse

import tabulate

from action import Actions

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', dest='filenames', default=['math.csv'])
    parser.add_argument('--report', dest='action_name', default='coffee-spent')
    data = Actions.execute(**vars(parser.parse_args()))
    print(
        tabulate.tabulate(data.data, headers=data.headers)
    )
