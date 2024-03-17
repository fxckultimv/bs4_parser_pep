import csv
import datetime as dt
import logging

from prettytable import PrettyTable

from constants import (
  BASE_DIR, DATETIME_FORMAT, RESULTS_DIR,
  DOWNLOAD_RESULT, FILE_FORMAT
)


def control_output(results, cli_args):
    output = cli_args.output
    output_functions = {
        'pretty': pretty_output,
        'file': file_output,
    }
    output_function = output_functions.get(output, default_output)
    output_function(results, cli_args)


def default_output(results):
    for row in results:
        print(*row)


def pretty_output(results):
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
