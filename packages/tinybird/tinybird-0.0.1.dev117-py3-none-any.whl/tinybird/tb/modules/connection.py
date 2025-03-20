# This is a command file for our CLI. Please keep it clean.
#
# - If it makes sense and only when strictly necessary, you can create utility functions in this file.
# - But please, **do not** interleave utility functions and command definitions.

from typing import Any, Dict, List, Optional

import click
from click import Context

from tinybird.client import TinyB
from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.common import (
    DataConnectorType,
    _get_setting_value,
    coro,
    echo_safe_humanfriendly_tables_format_smart_table,
    run_aws_iamrole_connection_flow,
    validate_aws_iamrole_connection_name,
)
from tinybird.tb.modules.create import generate_aws_iamrole_connection_file
from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tb.modules.project import Project

DATA_CONNECTOR_SETTINGS: Dict[DataConnectorType, List[str]] = {
    DataConnectorType.KAFKA: [
        "kafka_bootstrap_servers",
        "kafka_sasl_plain_username",
        "kafka_sasl_plain_password",
        "cli_version",
        "endpoint",
        "kafka_security_protocol",
        "kafka_sasl_mechanism",
        "kafka_schema_registry_url",
        "kafka_ssl_ca_pem",
    ],
    DataConnectorType.GCLOUD_SCHEDULER: ["gcscheduler_region"],
    DataConnectorType.SNOWFLAKE: [
        "account",
        "username",
        "password",
        "role",
        "warehouse",
        "warehouse_size",
        "stage",
        "integration",
    ],
    DataConnectorType.BIGQUERY: ["account"],
    DataConnectorType.GCLOUD_STORAGE: [
        "gcs_private_key_id",
        "gcs_client_x509_cert_url",
        "gcs_project_id",
        "gcs_client_id",
        "gcs_client_email",
        "gcs_private_key",
    ],
    DataConnectorType.GCLOUD_STORAGE_HMAC: [
        "gcs_hmac_access_id",
        "gcs_hmac_secret",
    ],
    DataConnectorType.GCLOUD_STORAGE_SA: ["account_email"],
    DataConnectorType.AMAZON_S3: [
        "s3_access_key_id",
        "s3_secret_access_key",
        "s3_region",
    ],
    DataConnectorType.AMAZON_S3_IAMROLE: [
        "s3_iamrole_arn",
        "s3_iamrole_region",
        "s3_iamrole_external_id",
    ],
    DataConnectorType.AMAZON_DYNAMODB: [
        "dynamodb_iamrole_arn",
        "dynamodb_iamrole_region",
        "dynamodb_iamrole_external_id",
    ],
}

SENSITIVE_CONNECTOR_SETTINGS = {
    DataConnectorType.KAFKA: ["kafka_sasl_plain_password"],
    DataConnectorType.GCLOUD_SCHEDULER: [
        "gcscheduler_target_url",
        "gcscheduler_job_name",
        "gcscheduler_region",
    ],
    DataConnectorType.GCLOUD_STORAGE_HMAC: ["gcs_hmac_secret"],
    DataConnectorType.AMAZON_S3: ["s3_secret_access_key"],
    DataConnectorType.AMAZON_S3_IAMROLE: ["s3_iamrole_arn"],
    DataConnectorType.AMAZON_DYNAMODB: ["dynamodb_iamrole_arn"],
}


@cli.group()
@click.pass_context
def connection(ctx: Context) -> None:
    """Connection commands."""


@connection.command(name="ls")
@click.option("--service", help="Filter by service")
@click.pass_context
@coro
async def connection_ls(ctx: Context, service: Optional[DataConnectorType] = None) -> None:
    """List connections."""
    obj: Dict[str, Any] = ctx.ensure_object(dict)
    client: TinyB = obj["client"]

    connections = await client.connections(connector=service, skip_bigquery=True)
    columns = []
    table = []

    click.echo(FeedbackManager.info_connections())

    if not service:
        sensitive_settings = []
        columns = ["service", "name", "id", "connected_datasources"]
    else:
        sensitive_settings = SENSITIVE_CONNECTOR_SETTINGS.get(service, [])
        columns = ["service", "name", "id", "connected_datasources"]
        if connector_settings := DATA_CONNECTOR_SETTINGS.get(service):
            columns += connector_settings

    for connection in connections:
        row = [_get_setting_value(connection, setting, sensitive_settings) for setting in columns]
        table.append(row)

    column_names = [c.replace("kafka_", "") for c in columns]
    echo_safe_humanfriendly_tables_format_smart_table(table, column_names=column_names)
    click.echo("\n")


@connection.group(name="create")
@click.pass_context
def connection_create(ctx: Context) -> None:
    """Create a connection."""


@connection_create.command(name="s3", short_help="Creates a AWS S3 connection.")
@click.pass_context
@coro
async def connection_create_s3(ctx: Context) -> None:
    """
    Creates a AWS S3 connection.

    \b
    $ tb connection create s3
    """
    project: Project = ctx.ensure_object(dict)["project"]
    obj: Dict[str, Any] = ctx.ensure_object(dict)
    client: TinyB = obj["client"]
    service = DataConnectorType.AMAZON_S3
    connection_name = await validate_aws_iamrole_connection_name(client)
    role_arn, region, external_id = await run_aws_iamrole_connection_flow(
        client,
        service=service,
        policy="read",  # For now only read since we only support import from S3
    )

    await generate_aws_iamrole_connection_file(
        name=connection_name, service=service, role_arn=role_arn, region=region, folder=project.folder
    )
    if external_id:
        click.echo(
            FeedbackManager.success_s3_iam_connection_created(
                connection_name=connection_name, external_id=external_id, role_arn=role_arn
            )
        )
