# outputs.py
from prettytable import PrettyTable
from prettytable.colortable import ColorTable, Themes


def control_output(results, cli_args):
    if cli_args.pretty:
        pretty_output(results)
    else:
        default_output(results)


def default_output(results):
    for row in results:
        print(*row)


def pretty_output(results):
    table = PrettyTable()
    table = ColorTable(theme=Themes.OCEAN)

    table.field_names = results[0]
    table.align = 'l'
    table.align['Версия'] = 'c'
    table.align['Статус'] = 'c'
    table.add_rows(results[1:])

    print(table)
