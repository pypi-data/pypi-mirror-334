from ._fabric_data_agent_api import FabricDataAgentAPI
import typing as t
import pandas as pd
from uuid import uuid4
from ._tagged_value import TaggedValue
import warnings


# The list of selectable element types (e.g. columns, measures are not selectable since the UX doesn't support it)
SELECTABLE_ELEMENT_TYPES = ["semantic_model.table", "lakehouse_tables.table", "warehouse_tables.table", "kusto.table"]


class Datasource:
    """
    Represents a datasource within an DataAgent.

    Attributes
    ----------
    _client : FabricDataAgentAPI
        The FabricDataAgentAPI client instance.
    _id : str
        The unique identifier of the datasource.
    """

    _client: FabricDataAgentAPI
    _id: str

    def __init__(self, client: FabricDataAgentAPI, id: str) -> None:
        """
        Initialize a Datasource instance.

        Parameters
        ----------
        client : FabricDataAgentAPI
            The FabricDataAgentAPI client to interact with the datasource.
        id : str
            The unique identifier of the datasource.
        """
        self._client = client
        self._id = id

    def __repr__(self):
        """
        Return a string representation of the Datasource.

        Returns
        -------
        str
            The string representation including the datasource ID.
        """
        return f"Datasource({self._id})"

    def pretty_print(self, include_type: t.Optional[bool] = False) -> None:
        """
        Pretty print the datasource configuration.

        Parameters
        ----------
        include_type : bool, optional
            Whether to include the type of the element in the output. Defaults to False.
        """
        config = self._client.get_datasource(self._id)

        def render_children(elements, level):
            if elements is None or len(elements) == 0:
                return

            indent = ' ' * 2

            for elem in elements:
                msg = f"{indent}|" * level + f' {elem["display_name"]}'

                if include_type:
                    msg += f' ({elem["type"]})'

                if elem.get("type") in SELECTABLE_ELEMENT_TYPES and elem["is_selected"]:
                    msg += " *"

                print(msg)
                render_children(elem["children"], level + 1)

        render_children(config.value.get("elements", []), 0)

    def get_fewshots(self) -> pd.DataFrame:
        """
        Get the fewshots for the datasource.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing the fewshots (Id, Question, Query, State, Embedding).
        """
        data = self._client.get_datasource_fewshots(self._id)

        return pd.DataFrame(
            [
                {
                    "Id": f["id"],
                    "Question": f["question"],
                    "Query": f["query"],
                    "State": f["state"],
                    "Embedding": f["embedding"],
                }
                for f in data.value.get("fewShots", [])
            ],
            columns=["Id", "Question", "Query", "State", "Embedding"],
        )

    def add_fewshot(self, question: str, query: str) -> None:
        """
        Add a fewshot to the datasource.

        Parameters
        ----------
        question : str
            The question.
        query : str
            The query.
        """
        fewshots = self._client.get_datasource_fewshots(self._id)

        data = fewshots.value.get("fewShots", [])

        data.append(
            {
                "Id": str(uuid4()),
                "Index": len(data),
                "Question": question,
                "Query": query,
            }
        )

        parentId = fewshots.value.get("parentId")
        if not parentId:
            fewshots.value["parentId"] = self._id

        fewshots.value["fewShots"] = data

        self._client.set_datasource_fewshots(self._id, fewshots)

    def remove_fewshot(self, fewshot_id: str) -> None:
        """
        Remove a fewshot from the datasource.

        Parameters
        ----------
        fewshot_id : str
            The ID of the fewshot to remove.
        """
        fewshots = self._client.get_datasource_fewshots(self._id)

        data = fewshots.value.get("fewShots", [])

        # remove the fewshot
        data = [f for f in data if f["id"] != fewshot_id]

        fewshots.value["fewShots"] = data

        self._client.set_datasource_fewshots(self._id, fewshots)

    def get_configuration(self) -> dict:
        """
        Get the configuration of the datasource.

        Returns
        -------
        dict
            The configuration of the datasource.
        """
        return self._client.get_datasource(self._id).value

    def update_configuration(
        self,
        instructions: str | None = None,
        schema_mode: str | None = None,
        user_description: str | None = None,
    ) -> None:
        """
        Update the configuration of the datasource.

        Parameters
        ----------
        instructions : str, optional
            Additional instructions for the datasource.
        schema_mode : str, optional
            The schema mode.
        user_description : str, optional
            The user description.
        """
        config = self._client.get_datasource(self._id)

        if instructions:
            config.value["additional_instructions"] = instructions

        if schema_mode:
            config.value["schema_mode"] = schema_mode

        if user_description:
            config.value["user_description"] = user_description

        self._client.set_datasource(config)

    def _set_is_selected(self, selected: bool, *path: str) -> TaggedValue:
        """
        Set the selection status of a specific path in the datasource.

        Parameters
        ----------
        selected : bool
            The selection status to set.
        *path : str
            The path to set the selection status for.

        Returns
        -------
        TaggedValue
            The updated configuration.
        """
        config = self._client.get_datasource(self._id)

        # recursive function to set the selection status
        def recurse(l_path: t.List[str], elements: t.List[dict] | None):
            if l_path is None or len(l_path) == 0 or elements is None:
                return

            for elem in elements:
                if elem["display_name"] == l_path[0]:
                    if len(l_path) == 1:
                        elem_type = elem.get("type")
                        if elem_type not in SELECTABLE_ELEMENT_TYPES:
                            raise ValueError(f"Only table elements can be selected: '{elem_type}'")

                        elem["is_selected"] = selected
                    else:
                        recurse(l_path[1:], elem["children"])

                    return

            warnings.warn(f"Path {path} not found in datasource")

        recurse(list(path), config.value.get("elements"))

        return config

    def _set_is_selected_all(self, selected: bool) -> TaggedValue:
        """
        Set the selection status for all elements in the datasource.

        Parameters
        ----------
        selected : bool
            The selection status to set.

        Returns
        -------
        TaggedValue
            The updated configuration.
        """
        config = self._client.get_datasource(self._id)

        def set_selected(elements):
            for elem in elements:
                if elem.get("type") in SELECTABLE_ELEMENT_TYPES:
                    elem["is_selected"] = selected

                set_selected(elem["children"])

        set_selected(config.value["elements"])

        return config

    def _select(self, is_selected: bool, *path: str) -> None:
        """
        Select or unselect elements in the datasource.

        Parameters
        ----------
        is_selected : bool
            Whether to select or unselect the elements.
        *path : str
            The path to select or unselect. e.g. self._select(True, "dbo", "table1", "col1").
        """
        if len(path) == 0:
            config = self._set_is_selected_all(is_selected)
        else:
            config = self._set_is_selected(is_selected, *path)

        self._client.set_datasource(config)

    def select(self, *path: str) -> None:
        """
        Select elements in the datasource.

        Parameters
        ----------
        *path : str
            The path to select.
        """
        self._select(True, *path)

    def unselect(self, *path: str) -> None:
        """
        Unselect elements in the datasource.

        Parameters
        ----------
        *path : str
            The path to unselect.
        """
        self._select(False, *path)
