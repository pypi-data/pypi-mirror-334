import pytest
import unittest
from unittest.mock import MagicMock
from fabric.dataagent.client._fabric_data_agent_mgmt import Datasource
from fabric.dataagent.client._fabric_data_agent_api import FabricDataAgentAPI
from fabric.dataagent.client._tagged_value import TaggedValue


class TestDatasource(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock(spec=FabricDataAgentAPI)
        self.datasource_id = "test_datasource_id"
        self.datasource = Datasource(self.mock_client, self.datasource_id)

    def test_init(self):
        self.assertEqual(self.datasource._client, self.mock_client)
        self.assertEqual(self.datasource._id, self.datasource_id)

    def test_repr(self):
        expected_repr = f"Datasource({self.datasource_id})"
        self.assertEqual(repr(self.datasource), expected_repr)

    def test_pretty_print(self):
        self.mock_client.get_datasource.return_value = TaggedValue(
            {
                "elements": [
                    {
                        "display_name": "Element1",
                        "type": "semantic_model.table",
                        "is_selected": True,
                        "children": [],
                    },
                    {
                        "display_name": "Element2",
                        "type": "semantic_model.table",
                        "is_selected": False,
                        "children": [],
                    },
                ]
            },
            "etag",
        )
        self.datasource.pretty_print(include_type=True)

    def test_get_fewshots(self):
        self.mock_client.get_datasource_fewshots.return_value = TaggedValue(
            {
                "fewShots": [
                    {
                        "id": "1",
                        "question": "Q1",
                        "query": "Query1",
                        "state": "State1",
                        "embedding": "Embedding1",
                    },
                    {
                        "id": "2",
                        "question": "Q2",
                        "query": "Query2",
                        "state": "State2",
                        "embedding": "Embedding2",
                    },
                ]
            },
            "etag",
        )
        fewshots = self.datasource.get_fewshots()
        self.assertEqual(len(fewshots), 2)

    def test_add_fewshot(self):
        self.mock_client.get_datasource_fewshots.return_value = TaggedValue(
            {"fewShots": []}, "etag"
        )
        self.datasource.add_fewshot("Q1", "Query1")
        self.mock_client.set_datasource_fewshots.assert_called_once()

    def test_remove_fewshot(self):
        self.mock_client.get_datasource_fewshots.return_value = TaggedValue(
            {
                "fewShots": [
                    {
                        "id": "1",
                        "question": "Q1",
                        "query": "Query1",
                        "state": "State1",
                        "embedding": "Embedding1",
                    }
                ]
            },
            "etag",
        )
        self.datasource.remove_fewshot("1")
        self.mock_client.set_datasource_fewshots.assert_called_once()

    def test_update_configuration(self):
        self.mock_client.get_datasource.return_value = TaggedValue({}, "etag")
        self.datasource.update_configuration(
            instructions="New instructions",
            schema_mode="New schema mode",
            user_description="New description",
        )
        self.mock_client.set_datasource.assert_called_once()

    def test_select0(self):
        # Case 1: 0 items selected
        self.mock_client.get_datasource.return_value = TaggedValue(
            {
                "id": self.datasource_id,
                "elements": [
                    {
                        "display_name": "Element1",
                        "is_selected": False,
                        "type": "semantic_model.table",
                        "children": []
                    }
                ],
            },
            "etag",
        )
        self.datasource.select("Element1")
        self.mock_client.set_datasource.assert_called_once()

    def test_select1(self):
        # Case 2: Path with 3 levels
        self.mock_client.get_datasource.return_value = TaggedValue(
            {
                "id": self.datasource_id,
                "elements": [
                    {
                        "display_name": "Level1",
                        "is_selected": False,
                        "children": [
                            {
                                "display_name": "Level2",
                                "is_selected": False,
                                "children": [
                                    {
                                        "display_name": "Level3",
                                        "type": "warehouse_tables.table",
                                        "is_selected": False,
                                        "children": [],
                                    }
                                ],
                            }
                        ],
                    }
                ],
            },
            "etag",
        )
        self.datasource.select("Level1", "Level2", "Level3")

        # Extract the actual call arguments
        actual_args = self.mock_client.set_datasource.call_args[0][0].value

        expected_args = {
            "id": self.datasource_id,
            "elements": [
                {
                    "display_name": "Level1",
                    "is_selected": False,
                    "children": [
                        {
                            "display_name": "Level2",
                            "is_selected": False,
                            "children": [
                                {
                                    "display_name": "Level3",
                                    "type": "warehouse_tables.table",
                                    "is_selected": True,
                                    "children": [],
                                }
                            ],
                        }
                    ],
                }
            ],
        }

        self.assertEqual(actual_args, expected_args)

    def test_unselect(self):
        self.mock_client.get_datasource.return_value = TaggedValue(
            {
                "elements": [
                    {
                        "display_name": "Element1",
                        "is_selected": True,
                        "children": [],
                        "type": "lakehouse_tables.table"
                    }
                ]
            },
            "etag",
        )
        self.datasource.unselect("Element1")
        self.mock_client.set_datasource.assert_called_once()

    def test_select_parent(self):
        # Case: Selecting a parent element should mark all child elements as selected
        self.mock_client.get_datasource.return_value = TaggedValue(
            {
                "id": self.datasource_id,
                "elements": [
                    {
                        "display_name": "dbo",
                        "is_selected": False,
                        "children": [
                            {
                                "display_name": "table1",
                                "type": "kusto.table",
                                "is_selected": False,
                                "children": [
                                    {
                                        "display_name": "col1",
                                        "is_selected": True,
                                        "children": [],
                                    },
                                    {
                                        "display_name": "col2",
                                        "is_selected": False,
                                        "children": [],
                                    },
                                    {
                                        "display_name": "col3",
                                        "is_selected": False,
                                        "children": [],
                                    },
                                ],
                            }
                        ],
                    }
                ],
            },
            "etag",
        )
        self.datasource.select("dbo", "table1")

        # Extract the actual call arguments
        actual_args = self.mock_client.set_datasource.call_args[0][0].value

        expected_args = {
            "id": self.datasource_id,
            "elements": [
                {
                    "display_name": "dbo",
                    "is_selected": False,
                    "children": [
                        {
                            "display_name": "table1",
                            "type": "kusto.table",
                            "is_selected": True,
                            "children": [
                                {
                                    "display_name": "col1",
                                    "is_selected": True,
                                    "children": [],
                                },
                                {
                                    "display_name": "col2",
                                    "is_selected": False,
                                    "children": [],
                                },
                                {
                                    "display_name": "col3",
                                    "is_selected": False,
                                    "children": [],
                                },
                            ],
                        }
                    ],
                }
            ],
        }

        self.assertEqual(actual_args, expected_args)

    def test_select_column(self):
        # Case 1: 0 items selected
        self.mock_client.get_datasource.return_value = TaggedValue(
            {
                "id": self.datasource_id,
                "elements": [
                    {
                        "display_name": "Element1",
                        "is_selected": False,
                        "type": "semantic_model.column",
                        "children": []
                    }
                ],
            },
            "etag",
        )

        with pytest.raises(ValueError):
            self.datasource.select("Element1")