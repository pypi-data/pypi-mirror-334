import click

# TODO this two arguments could be replaced by using the
#      get_target_dir_option from mantik/cli/_options.py
#      and something similar for source

SOURCE = click.argument(
    "source",
    type=str,
    nargs=1,
    required=True,
)
TARGET = click.argument(
    "target",
    type=str,
    nargs=1,
    required=True,
)
