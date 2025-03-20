import argparse


def main():
    parser = argparse.ArgumentParser(
        description='migration')
    parser.add_argument('migrate', help='migrate db to latest version')
    args = parser.parse_args()
    if args.migrate:
        ...


if __name__ == '__main__':
    main()
