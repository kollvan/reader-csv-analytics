import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', dest='filenames')
    parser.add_argument('--report', dest='report', default='coffee-spent')
    print(parser.parse_args())
