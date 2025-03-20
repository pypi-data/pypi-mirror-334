import sempy.fabric as fabric
from typing import Optional
from uuid import UUID
from sempy.fabric.exceptions import FabricHTTPException

from ._fabric_data_agent_mgmt import FabricDataAgentManagement


def create_data_agent(
    data_agent_name: str, workspace_id: Optional[UUID | str] = None
) -> FabricDataAgentManagement:
    """
    Create a new Data Agent and return an instance of FabricDataAgentAPI.

    Parameters
    ----------
    data_agent_name : str
        The name of the Data Agent to be created.
    workspace_id : Optional[UUID or str], optional
        The workspace ID. If not provided, it will be fetched automatically.

    Returns
    -------
    FabricDataAgentAPI
        An instance of FabricDataAgentAPI initialized with the created Data Agent.

    Raises
    ------
    FabricHTTPException
        If the response status code is not 200.
    """
    if not workspace_id:
        workspace_id = fabric.get_notebook_workspace_id()

    create_artifact_url = f"/metadata/workspaces/{workspace_id}/artifacts"
    # Construct the body
    create_artifact_body = {
        "artifactType": "LLMPlugin",
        "displayName": data_agent_name,
    }

    fabric_client = fabric.FabricRestClient()
    response = fabric_client.post(create_artifact_url, json=create_artifact_body)

    if response.status_code != 200:
        raise FabricHTTPException(response)

    return FabricDataAgentManagement(data_agent_name, workspace_id)


def delete_data_agent(data_agent_name_or_id: str) -> None:
    """
    Delete a Data Agent.

    Parameters
    ----------
    data_agent_name_or_id : str
        The name or ID of the Data Agent to delete.

    Raises
    ------
    FabricHTTPException
        If the response status code is not 200.
    """
    if isinstance(data_agent_name_or_id, UUID):
        data_agent_id = str(data_agent_name_or_id)
    else:
        data_agent_id = fabric.resolve_item_id(data_agent_name_or_id, "AISkill")

    artifact_url = f"/metadata/artifacts/{data_agent_id}"

    fabric_client = fabric.FabricRestClient()
    response = fabric_client.delete(artifact_url)

    if response.status_code != 200:
        raise FabricHTTPException(response)
