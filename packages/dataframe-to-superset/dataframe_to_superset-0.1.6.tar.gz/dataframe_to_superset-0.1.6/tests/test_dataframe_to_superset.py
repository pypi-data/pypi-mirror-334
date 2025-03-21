import re
from unittest.mock import patch

import pandas as pd
import pytest

from dataframe_to_superset import SupersetAccessor
from tests.fixtures.mock_superset_api import MockSupersetApi

DEFAULT_DATA = {"name": ["Alice", "Bob"], "age": [25, 30]}


@pytest.fixture
def mock_configure():
    with patch("dataframe_to_superset.SupersetApi", MockSupersetApi):
        SupersetAccessor.configure(
            base_url="http://mock-superset",
            username="mock_user",
            password="mock_password",
            provider="db",
            database_name="mock_database",
            schema="public",
        )


def test_as_dataset_success(mock_configure):
    df = pd.DataFrame(DEFAULT_DATA)
    url = df.superset.as_dataset("test_dataset")

    assert (
        url == "http://mock-superset/explore/?datasource_type=table&datasource_id=123"
    )


def test_as_dataset_verbose_return(mock_configure):
    df = pd.DataFrame(DEFAULT_DATA)
    result = df.superset.as_dataset("test_dataset", verbose_return=True)

    assert result == {
        "dataset_id": 123,
        "name": "test_dataset",
        "url": "http://mock-superset/explore/?datasource_type=table&datasource_id=123",
    }


def test_as_dataset_missing_configuration(mock_configure):
    df = pd.DataFrame(DEFAULT_DATA)
    SupersetAccessor._superset_api = None

    # keep re.escape to escape characters in error message, else it fails
    with pytest.raises(
        ValueError,
        match=re.escape(
            "SupersetAccessor is not configured. Call `SupersetAccessor.configure()` first."
        ),
    ):
        df.superset.as_dataset("test_dataset")


def test_as_dataset_missing_database(mock_configure):
    df = pd.DataFrame(DEFAULT_DATA)

    with patch.object(MockSupersetApi, "get_database_id", return_value=None):
        with pytest.raises(
            ValueError, match="Database 'mock_database' not found in Superset"
        ):
            df.superset.as_dataset("test_dataset")


def test_as_dataset_upload_failure(mock_configure):
    df = pd.DataFrame(DEFAULT_DATA)

    # keep re.escape to escape characters in error message, else it fails
    with patch.object(
        MockSupersetApi,
        "upload_csv_to_database",
        side_effect=Exception("Upload failed"),
    ):
        with pytest.raises(Exception, match=re.escape("Upload failed")):
            df.superset.as_dataset("test_dataset")
