import argparse
import os
from datetime import datetime, timedelta
from log_to_gor_converter import LogToGorConverter

GOR_DIRECTORY_PATH = "/home/vahid/gor_files/"

def convert_traffic(days_ago):
    yesterday = (datetime.today() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
    print(yesterday)

    if not os.path.exists(f"{GOR_DIRECTORY_PATH}{yesterday}.gor"):
        print(f"converting {GOR_DIRECTORY_PATH}{yesterday} to .gor")
        converter = LogToGorConverter(f"{GOR_DIRECTORY_PATH}{yesterday}.log", f"{GOR_DIRECTORY_PATH}{yesterday}.gor")
        converter.convert()

        print(f"removing {GOR_DIRECTORY_PATH}{yesterday}.log")
        os.remove(f"{GOR_DIRECTORY_PATH}{yesterday}.log")
    else:
        print(f"file {GOR_DIRECTORY_PATH}{yesterday}.gor already exists")

def main():
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("-d", "--days_ago",
                                 type=int,
                                 help="1 (yesterday), 2 (2 days ago), ...",
                                 default=1)
    args = argument_parser.parse_args()
    print(f"args.days_ago = {args.days_ago}")
    convert_traffic(args.days_ago)

if __name__ == '__main__':
    main()