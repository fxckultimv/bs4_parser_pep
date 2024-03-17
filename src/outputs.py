import csv
import datetime as dt
import logging

from prettytable import PrettyTable

from constants import (
  BASE_DIR, DATETIME_FORMAT, RESULTS_DIR,
  DOWNLOAD_RESULT, FILE_FORMAT, OUTPUT_FILE, OUTPUT_PRETTY
)


def default_output(results, cli_args=''):
    for row in results:
        print(*row)


def pretty_output(results, cli_args=''):
    table = PrettyTable()
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)


def file_output(results, cli_args):
    results_dir = BASE_DIR / RESULTS_DIR
    results_dir.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    now_formatted = dt.datetime.now().strftime(DATETIME_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.{FILE_FORMAT}'
    file_path = results_dir / file_name
    with open(file_path, 'w', encoding='utf-8') as file:
        csv.writer(
            file, dialect=csv.unix_dialect
        ).writerows(results)
    logging.info(DOWNLOAD_RESULT.format(path=file_path))


OUTPUT_FUNCTIONS = {
        OUTPUT_PRETTY: pretty_output,
        OUTPUT_FILE: file_output,
        None: default_output
    }


def control_output(results, cli_args):
    OUTPUT_FUNCTIONS[cli_args.output](results, cli_args)
