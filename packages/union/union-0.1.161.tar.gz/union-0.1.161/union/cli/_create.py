import logging
import os
import re
import time
import typing
from pathlib import Path
from typing import Optional

import rich_click as click
from flytekit import Labels, WorkflowExecutionPhase
from flytekit.configuration import (
    AuthType,
    Config,
    ImageConfig,
    PlatformConfig,
    SerializationSettings,
)
from flytekit.models.core.execution import TaskExecutionPhase
from flytekit.models.filters import ValueIn
from flytekit.remote import FlyteTask, FlyteWorkflowExecution, remote_fs
from flytekit.remote.remote import MOST_RECENT_FIRST
from flytekit.tools.translator import Options
from grpc import RpcError
from rich.console import Console

from union import Artifact
from union._config import (
    AppClientCredentials,
    _encode_app_client_credentials,
    _get_config_obj,
    _get_endpoint_for_login,
    _get_user_handle,
    _is_serverless_endpoint,
    _write_config_to_path,
)
from union._utils import _sanitize_label
from union.cli._artifact_create_common import ArtifactCreateCommand
from union.cli._common import _get_channel_with_org, _validate_key_value_pairs
from union.cli._option import MutuallyExclusiveArgument, MutuallyExclusiveOption
from union.internal.identity.app_payload_pb2 import CreateAppRequest
from union.internal.identity.app_service_pb2_grpc import AppsServiceStub
from union.internal.identity.enums_pb2 import (
    ConsentMethod,
    GrantTypes,
    ResponseTypes,
    TokenEndpointAuthMethod,
)
from union.internal.secret.definition_pb2 import SecretIdentifier, SecretSpec
from union.internal.secret.payload_pb2 import CreateSecretRequest
from union.internal.secret.secret_pb2_grpc import SecretServiceStub
from union.remote import UnionRemote
from union.workspace._vscode import (
    _DEFAULT_CONFIG_YAML_FOR_BASE_IMAGE,
    _DEFAULT_CONFIG_YAML_FOR_IMAGE_SPEC,
    WorkspaceConfig,
    resolver,
)
from union.workspace._vscode_remote import VSCODE_DEBUGGER_LOG_NAME, _generate_workspace_name, _get_workspace_executions

UNION_WORKSPACE_LABEL_KEY = "union_workspace"
ENABLE_WORKSPACE_DEFINITION_REGISTRATION = os.getenv("ENABLE_WORKSPACE_DEFINITION_REGISTRATION", "0") == "1"

logger = logging.getLogger("union.cli._create")


@click.group()
def create():
    """Create a resource."""


@create.command()
@click.argument(
    "name",
    required=False,
    cls=MutuallyExclusiveArgument,
    mutually_exclusive=["name_option"],
    error_msg="Please pass --name once: `union create secret --name NAME`",
)
@click.option(
    "--name",
    "name_option",
    help="Secret name",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["name"],
    error_msg="Please pass --name once: `union create secret --name NAME`",
)
@click.option(
    "--value",
    help="Secret value",
    prompt="Enter secret value",
    hide_input=True,
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["value_file"],
)
@click.option(
    "-f",
    "--value-file",
    help="Path to file containing the secret",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True, allow_dash=True),
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["value"],
)
@click.option("--project", help="Project name")
@click.option("--domain", help="Domain name")
def secret(
    name: Optional[str],
    name_option: Optional[str],
    value: str,
    value_file: str,
    project: Optional[str],
    domain: Optional[str],
):
    """Create a secret with NAME."""
    name = name or name_option

    platform_obj = _get_config_obj().platform
    channel, org = _get_channel_with_org(platform_obj)

    if value_file:
        with open(value_file, "rb") as f:
            secret_spec = SecretSpec(binary_value=f.read())
    else:
        secret_spec = SecretSpec(string_value=value)

    stub = SecretServiceStub(channel)
    request = CreateSecretRequest(
        id=SecretIdentifier(name=name, domain=domain, project=project, organization=org),
        secret_spec=secret_spec,
    )
    try:
        stub.CreateSecret(request)
        click.echo(f"Created secret with name: {name}")
    except RpcError as e:
        raise click.ClickException(f"Unable to create secret with name: {name}\n{e}") from e


@create.group("api-key")
def api_key():
    """Manage API keys."""


@api_key.command("admin")
@click.option("--name", type=str, help="Name for API key", required=True)
def admin(name: str):
    """Create an api key."""
    platform_obj = _get_config_obj().platform
    normalized_client_name = re.sub("[^0-9a-zA-Z]+", "-", name.lower())
    if _is_serverless_endpoint(platform_obj.endpoint):
        userhandle = _get_user_handle(platform_obj)
        tenant = platform_obj.endpoint.split(".")[0]
        client_id = f"{tenant}-{userhandle}-{normalized_client_name}"
    else:
        client_id = normalized_client_name
    channel, org = _get_channel_with_org(platform_obj)

    stub = AppsServiceStub(channel)
    request = CreateAppRequest(
        organization=org,
        client_id=client_id,
        client_name=client_id,
        grant_types=[GrantTypes.CLIENT_CREDENTIALS, GrantTypes.AUTHORIZATION_CODE],
        redirect_uris=["http://localhost:8080/authorization-code/callback"],
        response_types=[ResponseTypes.CODE],
        token_endpoint_auth_method=TokenEndpointAuthMethod.CLIENT_SECRET_BASIC,
        consent_method=ConsentMethod.CONSENT_METHOD_REQUIRED,
    )

    try:
        response = stub.Create(request)
    except RpcError as e:
        raise click.ClickException(f"Unable to create api-key with name: {name}\n{e}") from e

    click.echo(f"Client ID: {response.app.client_id}")
    click.echo("The following API key will only be shown once. Be sure to keep it safe!")
    click.echo("Configure your headless CLI by setting the following environment variable:")
    click.echo()

    union_api_key = _encode_app_client_credentials(
        AppClientCredentials(
            endpoint=platform_obj.endpoint,
            client_id=response.app.client_id,
            client_secret=response.app.client_secret,
            org=org,
        )
    )
    click.echo(f'export UNION_API_KEY="{union_api_key}"')


@create.command()
@click.option(
    "--auth",
    type=click.Choice(["device-flow", "pkce"]),
    default="pkce",
    help="Authorization method to ues",
)
@click.option(
    "--host", default=None, help="Host to connect to.", cls=MutuallyExclusiveOption, mutually_exclusive=["serverless"]
)
@click.option(
    "--serverless",
    default=False,
    is_flag=True,
    help="Connect to serverless.",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["host"],
)
def login(auth: str, host: Optional[str], serverless: bool):
    """Log into Union

    - On Union Serverless run: `union create login --serverless`

    - On Union BYOC run: `union create login --host UNION_TENANT`
    """
    endpoint = _get_endpoint_for_login(host=host, serverless=serverless)

    if auth == "pkce":
        auth_mode = AuthType.PKCE
    else:
        auth_mode = AuthType.DEVICEFLOW

    config = Config.auto().with_params(
        platform=PlatformConfig(
            endpoint=endpoint,
            insecure=False,
            auth_mode=auth_mode,
        )
    )

    console = Console()
    try:
        path = _write_config_to_path(endpoint, auth_mode.value)
        console.print(f"🔐 [yellow]Configuration saved to {path}[/yellow]")

        # Accessing the client will trigger authentication
        remote = UnionRemote(config=config)
        remote._user_info()  # noqa
        ep = "serverless" if serverless else endpoint
        console.print(f"Login successful into [green][bold]{ep}[/bold][/green]")

    except Exception as e:
        raise click.ClickException(f"Unable to login.\n{e}") from e


@create.command()
@click.pass_context
@click.argument("config_file", type=click.Path(path_type=Path))
def workspace(ctx: click.Context, config_file: Path):
    """Create workspace."""
    config_content = config_file.read_text()
    workspace_config = WorkspaceConfig.from_yaml(config_content)

    remote = UnionRemote(default_domain=workspace_config.domain, default_project=workspace_config.project)
    logger.debug(f"Workspace config: {workspace_config}")
    logger.debug(f"Remote: {remote.__dict__}")
    _create_workspace(remote, workspace_config, config_content)


@click.command()
@click.pass_context
@click.argument("config_file", type=click.Path(path_type=Path))
def workspace_definition(ctx: click.Context, config_file: Path):
    """Create a workspace task definition."""
    config_content = config_file.read_text()
    workspace_config = WorkspaceConfig.from_yaml(config_content)

    remote = UnionRemote(default_domain=workspace_config.domain, default_project=workspace_config.project)
    logger.debug(f"Workspace config: {workspace_config}")
    logger.debug(f"Remote: {remote.__dict__}")

    remote_task = _create_workspace_definition(remote, workspace_config)

    console_url = remote.generate_console_url(remote_task)
    console = Console()
    console.print(f"🚀 Created workspace definition {console_url}")


if ENABLE_WORKSPACE_DEFINITION_REGISTRATION:
    create.add_command(workspace_definition)


@create.command("workspace-config")
@click.argument("config_file", type=click.Path(path_type=Path))
@click.option("--init", type=click.Choice(["base_image"]), required=True)
def workspace_config(config_file: Path, init: str):
    """Create workspace config at CONFIG_FILE."""
    if config_file.exists():
        raise click.ClickException(f"{config_file} already exists")

    click.echo(f"Writing workspace configuration to {config_file}")
    if init == "base_image":
        config_file.write_text(_DEFAULT_CONFIG_YAML_FOR_BASE_IMAGE)
    else:
        config_file.write_text(_DEFAULT_CONFIG_YAML_FOR_IMAGE_SPEC)


def _create_workspace_definition(remote: UnionRemote, ws_config: WorkspaceConfig) -> FlyteTask:
    name = ws_config.name
    project = ws_config.project
    domain = ws_config.domain

    task = resolver.get_task_for_workspace(ws_config)
    console = Console()
    console.print("✨ Creating workspace definition...")

    try:
        source_root = task.container_image.source_root
    except AttributeError:
        source_root = None

    return remote.register_task(
        task,
        serialization_settings=SerializationSettings(
            project=project, domain=domain, image_config=ImageConfig.auto_default_image(), source_root=source_root
        ),
        version=_generate_workspace_name(name),
    )


def _get_previous_workspace_state_dir(
    remote: UnionRemote,
    ws_config: WorkspaceConfig,
) -> Optional[str]:
    executions, _ = remote.client.list_executions_paginated(
        project=ws_config.project,
        domain=ws_config.domain,
        limit=1,
        filters=[
            ValueIn("execution_tag.key", [UNION_WORKSPACE_LABEL_KEY]),
            ValueIn("execution_tag.value", [_sanitize_label(ws_config.name)]),
            ValueIn("phase", ["SUCCEEDED"]),
        ],
        sort_by=MOST_RECENT_FIRST,
    )
    if len(executions) == 0:
        return None

    ex = remote.sync_execution(
        FlyteWorkflowExecution.promote_from_model(executions[0]),
    )
    return ex.outputs.literals["state_dir"].scalar.blob.uri


def _create_workspace(remote: UnionRemote, ws_config: WorkspaceConfig, config_content: str):
    project = ws_config.project
    domain = ws_config.domain
    name = ws_config.name

    executions = _get_workspace_executions(remote, project, domain)

    for _, ex_name in executions:
        if ex_name == name:
            raise click.ClickException(f"Workspace with name: {name} already exists.")

    remote_task = _create_workspace_definition(remote=remote, ws_config=ws_config)

    prev_state_dir = _get_previous_workspace_state_dir(remote, ws_config)
    console_http_domain = remote.generate_console_http_domain()

    execution = remote.execute(
        remote_task,
        inputs={
            "config_content": config_content,
            "host": remote.config.platform.endpoint,
            "console_http_domain": console_http_domain,
            "state_dir": prev_state_dir,
        },
        options=Options(
            labels=Labels(values={UNION_WORKSPACE_LABEL_KEY: _sanitize_label(ws_config.name)}),
        ),
        project=project,
        domain=domain,
    )

    vscode_count = 0
    console = Console()
    with console.status("✨ Starting workspace...") as status:
        status.update(status="🚀 Starting workspace...")
        while True:
            time.sleep(5)
            execution = remote.sync_execution(execution, sync_nodes=True)
            if execution.is_done:
                url = remote.generate_console_url(execution)
                raise click.ClickException(f"Workspace failed to launch. See {url} for details.")

            if execution.closure.phase != WorkflowExecutionPhase.RUNNING:
                continue

            status.update(status="⏳ Waiting for node to spin up...")
            if not execution.node_executions:
                continue

            all_keys = [e for e in execution.node_executions if e != "start-node"]
            if not all_keys:
                continue

            vscode_key = all_keys[0]
            vscode_node = execution.node_executions[vscode_key]

            if vscode_node.closure.phase != TaskExecutionPhase.RUNNING or not vscode_node.task_executions:
                continue

            task_execution = vscode_node.task_executions[-1]
            if task_execution.closure.phase != TaskExecutionPhase.RUNNING:
                continue

            for log in task_execution.closure.logs:
                if VSCODE_DEBUGGER_LOG_NAME in log.name:
                    status.update(status="⏳ Waiting for VSCode to start...")
                    resolve_uri = remote.generate_console_http_domain() + log.uri
                    vscode_count += 1
                    if vscode_count == 3:
                        # Make sure execution did not fail before showing dynamic log link
                        execution = remote.sync_execution(execution, sync_nodes=True)
                        if execution.is_done:
                            url = remote.generate_console_url(execution)
                            raise click.ClickException(f"Workspace failed to launch. See {url} for details.")

                        click.echo(f"\n🚀 Open Workspace at:\n{resolve_uri}")
                        return


@create.command("artifact", cls=ArtifactCreateCommand)
@click.argument("name")
@click.option("--version", type=str, required=True, help="Version of the artifact")
@click.option(
    "--partitions", "-p", callback=_validate_key_value_pairs, help="Partitions for the artifact", multiple=True
)
@click.option("--short-description", help="Short description of the artifact")
def artifact(
    name: str,
    project: str,
    domain: str,
    version: Optional[str],
    partitions: Optional[typing.List[str]],
    short_description: Optional[str],
    **kwargs,
):
    """Create an artifact with NAME."""
    remote = UnionRemote(
        default_domain=domain, default_project=project, data_upload_location=remote_fs.REMOTE_PLACEHOLDER
    )
    lit, lt = ArtifactCreateCommand.get_literal_from_args(remote.context, kwargs)
    a = Artifact(
        project=project,
        domain=domain,
        name=name,
        version=version,
        partitions=partitions,
        short_description=short_description,
        literal=lit,
        literal_type=lt,
    )
    remote.create_artifact(artifact=a)
    url = remote.generate_console_url(a)
    Console().print(f"[green]Created artifact with name: [bold][link={url}]{name}:{version}[/link][/bold][/green]")
