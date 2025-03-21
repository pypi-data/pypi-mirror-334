import click

from montecarlodata.data_exports.data_exports import DataExportService
from montecarlodata.data_exports.fields import (
    ALL_ALERTS_DATA_EXPORT_NAME,
    ALL_ASSETS_DATA_EXPORT_NAME,
    ALL_EVENTS_DATA_EXPORT_NAME,
    ALL_MONITORS_DATA_EXPORT_NAME,
    FILE_SCHEME,
    S3_SCHEME,
    SCHEME_DELIM,
)
from montecarlodata.tools import add_common_options

# Shared command verbiage
GET_VERBIAGE = f"""
\b\n
DESTINATION is the path where the Data Export will be written to.

Supported schemes:\n
    '{FILE_SCHEME}{SCHEME_DELIM}' - save Data Export locally.\n
    '{S3_SCHEME}{SCHEME_DELIM}' - save Data Export to S3.

Notice - Will overwrite a file if it exists in the path and create any missing directories or prefixes.
"""  # noqa: E501

# Options shared across commands
MINIMAL_GET_OPTIONS = [
    click.option(
        "--aws-profile",
        required=False,
        help="AWS profile to be used when uploading to S3.",
    ),
    click.option(
        "--dry",
        required=False,
        is_flag=True,
        help="Echo temporary presigned URL for the Data Export and quit.",
    ),
]

GET_OPTIONS = [click.argument("destination", required=True), *MINIMAL_GET_OPTIONS]


@click.group(help="Export your data.")
def export():
    """
    Group for any Data Export related subcommands
    """
    pass


@export.command(help="List Data Export details and availability.", name="list")
@click.pass_obj
def list_data_exports(ctx):
    DataExportService(
        config=ctx["config"],
        command_name="export list_data_exports",
    ).echo_data_exports()


@export.command(help=f"Get All Monitors Data Export. {GET_VERBIAGE}")
@add_common_options(GET_OPTIONS)
@click.pass_obj
def get_all_monitors(ctx, **kwargs):
    DataExportService(
        config=ctx["config"],
        command_name="export get_all_monitors",
    ).get_data_export(data_export=ALL_MONITORS_DATA_EXPORT_NAME, **kwargs)


@export.command(help=f"Get All Assets Data Export. {GET_VERBIAGE}")
@add_common_options(GET_OPTIONS)
@click.pass_obj
def get_all_assets(ctx, **kwargs):
    DataExportService(
        config=ctx["config"],
        command_name="export get_all_assets",
    ).get_data_export(data_export=ALL_ASSETS_DATA_EXPORT_NAME, **kwargs)


@export.command(help=f"Get All Alerts Data Export. {GET_VERBIAGE}")
@add_common_options(GET_OPTIONS)
@click.pass_obj
def get_all_alerts(ctx, **kwargs):
    DataExportService(
        config=ctx["config"],
        command_name="export get_all_alerts",
    ).get_data_export(data_export=ALL_ALERTS_DATA_EXPORT_NAME, **kwargs)


@export.command(help=f"Get All Events Data Export. {GET_VERBIAGE}")
@add_common_options(GET_OPTIONS)
@click.pass_obj
def get_all_events(ctx, **kwargs):
    DataExportService(
        config=ctx["config"],
        command_name="export get_all_events",
    ).get_data_export(data_export=ALL_EVENTS_DATA_EXPORT_NAME, **kwargs)


@export.command(help=f"Get an arbitrary Data Export. {GET_VERBIAGE}")
@add_common_options(MINIMAL_GET_OPTIONS)
@click.option(
    "--name",
    help="Name of the Data Export to retrieve. Data Export names can be found "
    'via the list command (e.g. `ALL_MONITORS` from "All monitors (ALL_MONITORS)")',
    required=True,
)
@click.option(
    "--destination",
    help="Destination location to save Data Export.",
    required=True,
)
@click.pass_obj
def get(ctx, name, **kwargs):
    DataExportService(
        config=ctx["config"],
        command_name="export get",
    ).get_data_export(data_export=name, **kwargs)
