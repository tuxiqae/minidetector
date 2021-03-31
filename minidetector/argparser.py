import argparse
import logging


def argparse_init() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='minidetector is an example tool '
                    'for detecting network identities and inserting them into a PostgreSQL database')
    parser.add_argument("--clean", const=True, default=False, nargs='?', help="prune the existing data before starting")
    parser.add_argument("--debug", const=True, default=False, nargs='?', help="enable debug logging")
    args = parser.parse_args()
    logging.root.setLevel(logging.DEBUG if args.debug else logging.INFO)

    return args
