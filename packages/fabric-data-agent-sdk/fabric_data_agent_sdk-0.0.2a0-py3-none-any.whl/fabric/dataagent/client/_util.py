from uuid import UUID
import typing as t
import sempy.fabric as sf
from sempy.fabric.exceptions import FabricHTTPException


def get_artifact_by_id_or_name(
    identifier: str | UUID, type: str, workspace_id: t.Optional[UUID | str] = None
) -> t.Tuple[str, UUID]:
    """
    Retrieve the artifact name and ID by its name or ID within the specified workspace.

    Parameters
    ----------
    identifier : str or UUID
        The name or ID of the artifact.
    type : str
        The type of the artifact(e.g., "Lakehouse", "AISkill").
    workspace_id : Optional[str or UUID], optional
        The workspace ID. If not provided, the current workspace ID is used.

    Returns
    -------
    tuple[str, UUID]
        A tuple containing the artifact name and its UUID.

    Raises
    ------
    ValueError
        If the workspace contains no artifacts or if the specified artifact is not found.
    KeyError
        If required columns are missing in the artifact DataFrame.
    """
    if not workspace_id:
        workspace_id = sf.get_notebook_workspace_id()

    # List all items of the specified type
    df = sf.list_items(type=type, workspace=workspace_id)
    # Check if the DataFrame is empty
    if df.empty:
        raise ValueError("Workspace contains no artifacts.")

    if isinstance(identifier, UUID):
        # Find the artifact name that matches the given ID
        artifact_row = df[df["Id"] == str(identifier)]
        if not artifact_row.empty:
            artifact_name = artifact_row["Display Name"].values[0]
            return artifact_name, identifier
        else:
            raise ValueError(f"Artifact with ID '{identifier}' not found.")
    else:
        # Find the artifact ID that matches the given name
        artifact_row = df[df["Display Name"] == identifier]
        if not artifact_row.empty:
            artifact_id = UUID(artifact_row["Id"].values[0])
            return identifier, artifact_id
        else:
            raise ValueError(f"Artifact with name '{identifier}' not found.")


def resolve_workspace_name_and_id(workspace: str | UUID | None) -> t.Tuple[str, UUID]:
    """
    Resolve the workspace name and ID based on the provided input.

    Parameters
    ----------
    workspace : str or UUID or None
        The workspace name or ID. If None, the current notebook's workspace is used.

    Returns
    -------
    tuple[str, UUID]
        A tuple containing the workspace name and its UUID.
    """
    if workspace is None:
        workspace_id = UUID(sf.get_notebook_workspace_id())
        workspace_name = sf.resolve_workspace_name(workspace_id)
    else:
        workspace_name = sf.resolve_workspace_name(workspace)
        workspace_id = UUID(sf.resolve_workspace_id(workspace))

    return workspace_name, workspace_id


def get_workspace_capacity_id(workspace_id: str | UUID) -> str:
    """
    Retrieve the capacity ID for the specified workspace.

    Parameters
    ----------
    workspace_id : str or UUID
        The ID of the workspace.

    Returns
    -------
    str
        The capacity ID associated with the workspace.

    Raises
    ------
    FabricHTTPException
        If the workspace data retrieval fails.
    ValueError
        If the capacity ID is not found in the response.
    """
    fabric_rest_client = sf.FabricRestClient()
    response = fabric_rest_client.get(f'/v1/workspaces/{workspace_id}')

    if response.status_code != 200:
        raise FabricHTTPException(
            f"Failed to retrieve workspace data: {response.status_code}, {response.text}"
        )

    content = response.json()
    capacity_id = content.get('capacityId')
    if not capacity_id:
        raise ValueError("Capacity ID not found in the response.")

    return capacity_id
