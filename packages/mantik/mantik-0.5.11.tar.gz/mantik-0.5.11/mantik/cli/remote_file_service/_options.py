import uuid

import click


DATA_REPOSITORY_NAME = click.option(
    "--name",
    required=False,
    default=None,
    type=str,
    help="Data repository name, displayed in Mantik. "
    "When not passed the TARGET is passed as name.",
)

# TODO this will probably in the future need to be refactored
#      to look more similar to the similar options in mantik/cli/_options.py
#      to have more cohesion in the api

DATA_REPOSITORY_ID = click.option(
    "--id",
    required=False,
    default=None,
    type=uuid.UUID,
    help="Data repository ID.",
)

DATA_REPOSITORY_DESCRIPTION = click.option(
    "--description",
    required=False,
    default=None,
    type=str,
    help="Data repository description, displayed in Mantik.",
)
