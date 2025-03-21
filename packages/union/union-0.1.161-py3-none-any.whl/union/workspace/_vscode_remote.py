import logging
import random
import string
import uuid
import weakref
from typing import AsyncGenerator, List, Optional

import grpc
from flyteidl.core import tasks_pb2 as _tasks_pb2
from flytekit import WorkflowExecutionPhase
from flytekit.configuration import Config
from flytekit.models.core.execution import TaskExecutionPhase
from flytekit.models.execution import Execution
from flytekit.models.filters import Equal, ValueIn

from union.cli._common import _get_channel_with_org
from union.internal.workspace.workspace_definition_payload_pb2 import (
    CreateWorkspaceDefinitionRequest,
    CreateWorkspaceDefinitionResponse,
)
from union.internal.workspace.workspace_definition_pb2 import (
    WorkspaceDefinitionIdentifier,
    WorkspaceDefinitionSpec,
)
from union.internal.workspace.workspace_definition_service_pb2_grpc import WorkspaceRegistryServiceStub
from union.internal.workspace.workspace_instance_payload_pb2 import (
    GetWorkspaceInstanceRequest,
    GetWorkspaceInstanceResponse,
    WatchWorkspaceInstancesRequest,
    WatchWorkspaceInstancesResponse,
)
from union.internal.workspace.workspace_instance_pb2 import (
    WorkspaceInstanceIdentifier,
    WorkspaceInstanceStatus,
)
from union.internal.workspace.workspace_instance_service_pb2_grpc import WorkspaceInstanceServiceStub
from union.remote import UnionRemote

VERSION_STRING_LENGTH = 20
VSCODE_DEBUGGER_LOG_NAME = "VS Code Debugger"

_logger = logging.getLogger(__name__)


class WorkspaceRemote:
    def __init__(
        self,
        default_project: str,
        default_domain: str,
        config: Optional[Config] = None,
        union_remote: Optional[UnionRemote] = None,
    ):
        if union_remote is None:
            union_remote = UnionRemote(config=config, default_domain=default_domain, default_project=default_project)
            self._union_remote = union_remote
            self._union_remote_ref = weakref.ref(self._union_remote)
        else:
            # Union remote is passed in directly. We assume that the caller will have a reference to `AppRemote`.
            self._union_remote_ref = weakref.ref(union_remote)

        self.config = union_remote.config
        self.default_project = union_remote.default_project
        self.default_domain = union_remote.default_domain

    @property
    def union_remote(self) -> UnionRemote:
        union_remote = self._union_remote_ref()
        if union_remote is None:
            raise ValueError("Unable to find union remote")
        return union_remote

    def get_workspace_definition_id(
        self,
        workspace_definition_name: str,
        project: Optional[str] = None,
        domain: Optional[str] = None,
        version: Optional[str] = None,
    ) -> WorkspaceDefinitionIdentifier:
        return WorkspaceDefinitionIdentifier(
            org=self.org,
            project=project or self.default_project,
            domain=domain or self.default_domain,
            name=workspace_definition_name,
            version=version or str(uuid.uuid4()),
        )

    def get_workspace_instance_id(
        self,
        workspace_instance_name: str,
        project: Optional[str] = None,
        domain: Optional[str] = None,
    ) -> WorkspaceInstanceIdentifier:
        return WorkspaceInstanceIdentifier(
            org=self.org,
            project=project or self.default_project,
            domain=domain or self.default_domain,
            name=workspace_instance_name,
            host=self.org,
        )

    async def workspace_instance_is_stopping(
        self,
        workspace_instance_name: str,
        project: Optional[str] = None,
        domain: Optional[str] = None,
        logger: Optional[logging.Logger] = _logger,
    ) -> bool:
        """
        Check if the workspace instance is terminated or terminating.
        """
        workspace_instance_id = self.get_workspace_instance_id(
            workspace_instance_name=workspace_instance_name,
            project=project or self.default_project,
            domain=domain or self.default_domain,
        )
        logger.info(f"GetWorkspaceInstance {workspace_instance_id}")
        response: GetWorkspaceInstanceResponse = await self.instance_async_client.GetWorkspaceInstance(
            GetWorkspaceInstanceRequest(id=workspace_instance_id)
        )
        return response.workspace_instance.spec.status.phase in (
            WorkspaceInstanceStatus.WorkspaceInstancePhase.WORKSPACE_INSTANCE_PHASE_TERMINATING,
            WorkspaceInstanceStatus.WorkspaceInstancePhase.WORKSPACE_INSTANCE_PHASE_TERMINATED,
        )

    async def watch_workspace_instance(
        self,
        workspace_instance_name: str,
        project: Optional[str] = None,
        domain: Optional[str] = None,
        logger: Optional[logging.Logger] = _logger,
    ) -> AsyncGenerator[bool, None]:
        """
        Watch the workspace instance for stopping event.
        """

        logger.info(f"Watching workspace instance {workspace_instance_name} in project {project} and domain {domain}")

        workspace_instance_id = self.get_workspace_instance_id(
            workspace_instance_name=workspace_instance_name,
            project=project or self.default_project,
            domain=domain or self.default_domain,
        )
        watch_request = WatchWorkspaceInstancesRequest(workspace_instance_id=workspace_instance_id)

        response: WatchWorkspaceInstancesResponse
        logger.info(f"WatchWorkspaceInstances request {watch_request}")

        stream = self.instance_async_client.WatchWorkspaceInstances(watch_request)
        while True:
            try:
                async for response in stream:
                    logger.info(f"WatchWorkspaceInstances response {response}")
                    is_stopping = response.stopping_event is not None
                    logger.info(f"Workspace instance is stopping: {is_stopping}")
                    yield is_stopping
                    if is_stopping:
                        return
            except (grpc.RpcError, Exception) as exc:
                logger.info(f"Error watching workspace instance {exc}, resetting stream")
                stream = self.instance_async_client.WatchWorkspaceInstances(watch_request)
                continue

    async def create_workspace_definition(
        self,
        workspace_definition_name: str,
        project: Optional[str] = None,
        domain: Optional[str] = None,
        version: Optional[str] = None,
        on_startup: Optional[List[str]] = None,
    ) -> CreateWorkspaceDefinitionResponse:
        """
        Create a workspace definition.
        """

        workspace_definition_id = self.get_workspace_definition_id(
            workspace_definition_name=workspace_definition_name,
            project=project,
            domain=domain,
            version=version,
        )

        kwargs = {
            "resources": _tasks_pb2.Resources(
                requests=[
                    _tasks_pb2.Resources.ResourceEntry(name=_tasks_pb2.Resources.ResourceName.CPU, value="4"),
                    _tasks_pb2.Resources.ResourceEntry(name=_tasks_pb2.Resources.ResourceName.MEMORY, value="4Gi"),
                ],
            )
        }
        if on_startup is not None:
            kwargs["on_startup"] = on_startup

        workspace_definition_spec = WorkspaceDefinitionSpec(**kwargs)
        create_request = CreateWorkspaceDefinitionRequest(
            id=workspace_definition_id,
            workspace_spec=workspace_definition_spec,
        )
        response: CreateWorkspaceDefinitionResponse = await self.definition_async_client.CreateWorkspaceDefinition(
            create_request
        )
        return response

    @property
    def instance_async_client(self) -> WorkspaceInstanceServiceStub:
        try:
            return self._instance_async_client
        except AttributeError:
            self._instance_async_client = WorkspaceInstanceServiceStub(self.async_channel)
            return self._instance_async_client

    @property
    def definition_async_client(self) -> WorkspaceRegistryServiceStub:
        try:
            return self._definition_async_client
        except AttributeError:
            self._definition_async_client = WorkspaceRegistryServiceStub(self.async_channel)
            return self._definition_async_client

    @property
    def sync_channel(self) -> grpc.Channel:
        try:
            return self._sync_channel
        except AttributeError:
            self._sync_channel, self._org = _get_channel_with_org(self.config.platform)
            return self._sync_channel

    @property
    def async_channel(self) -> grpc.aio.Channel:
        from union.filesystems._endpoint import _create_secure_channel_from_config

        try:
            return self._async_channel
        except AttributeError:
            self._async_channel = _create_secure_channel_from_config(self.config.platform, self.sync_channel)
            return self._async_channel

    @property
    def org(self) -> Optional[str]:
        try:
            return self._org
        except AttributeError:
            self._sync_channel, self._org = _get_channel_with_org(self.config.platform)
            if self._org is None or self._org == "":
                self._org = self.config.platform.endpoint.split(".")[0]
            return self._org


def _generate_random_str(N: int):
    items = string.ascii_letters + string.digits
    return "".join(random.choice(items) for _ in range(N))


def _generate_workspace_name(name: str):
    """Generate workspace name prefixed by name."""
    return f"{name}-{_generate_random_str(VERSION_STRING_LENGTH)}"


def _get_workspace_name(version):
    return version[: -(VERSION_STRING_LENGTH + 1)]


def _get_workspace_executions(remote: UnionRemote, project: str, domain: str):
    executions, _ = remote.client.list_executions_paginated(
        project=project,
        domain=domain,
        limit=1000,
        filters=[
            Equal("task.name", "union.workspace._vscode.workspace"),
            ValueIn("phase", ["RUNNING", "QUEUED"]),
        ],
    )
    return [(e, _get_workspace_name(e.spec.launch_plan.version)) for e in executions]


def _get_vscode_link(remote: UnionRemote, execution: Execution) -> str:
    if execution.closure.phase != WorkflowExecutionPhase.RUNNING:
        return "Unavailable"

    workflow_execution = remote.fetch_execution(
        project=execution.id.project,
        domain=execution.id.domain,
        name=execution.id.name,
    )
    workflow_execution = remote.sync_execution(workflow_execution, sync_nodes=True)

    if not workflow_execution.node_executions:
        return "Unavailable"

    all_keys = [e for e in workflow_execution.node_executions if e != "start-node"]
    if not all_keys:
        return "Unavailable"

    vscode_key = all_keys[0]
    vscode_node = workflow_execution.node_executions[vscode_key]

    if vscode_node.closure.phase != TaskExecutionPhase.RUNNING or not vscode_node.task_executions:
        return "Unavailable"

    task_execution = vscode_node.task_executions[-1]
    if task_execution.closure.phase != TaskExecutionPhase.RUNNING:
        return "Unavailable"

    for log in task_execution.closure.logs:
        if VSCODE_DEBUGGER_LOG_NAME in log.name:
            return remote.generate_console_http_domain() + log.uri
