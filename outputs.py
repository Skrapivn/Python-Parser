# outputs.py
from prettytable import PrettyTable
from prettytable.colortable import ColorTable, Themes


def control_output(results, cli_args):
    output = cli_args.output
    if output == 'pretty':
        pretty_output(results)
    elif output == 'file':
        file_output(results, cli_args)
    else:
        default_output(results)


def default_output(results):
    for row in results:
        print(*row)


def pretty_output(results):
    table = PrettyTable()
    table = ColorTable(theme=Themes.OCEAN)

    table.field_names = results[0]
    table.align = 'c'
    table.add_rows(results[1:])

    print(table)


def file_output(results, cli_args):
    # Сформируйте путь до директории results.
    results_dir = ...
    # Создайте директорию.
