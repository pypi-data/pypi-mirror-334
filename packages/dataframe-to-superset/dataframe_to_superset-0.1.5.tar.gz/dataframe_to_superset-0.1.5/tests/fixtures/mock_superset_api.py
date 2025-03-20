from dataframe_to_superset.SupersetApi import HTTPMethod
from typing import Any, Dict

MOCK_DATABASE_ID = 1
MOCK_DATASET_ID = 123
MOCK_DATABASE_NAME = "mock_database"
MOCK_DATASET_NAME = "mock_dataset"


class Mock_SupersetApiBase:
    def __init__(self, base_url: str, username: str, password: str, provider: str):
        self.api_url = f"{base_url}/api/v1"
        self.username = username
        self.password = password
        self.provider = provider
        self.access_token = None
        self.refresh_token = None

    def _authenticate(self) -> None:
        self.access_token = "mock_access"
        self.refresh_token = "mock_access_token"

    def _refresh(self) -> None:
        self.access_token = "mock_refreshed_access_token"
        self.refresh_token = "mock_refreshed_refresh_token"

    def _request(
        self, method: HTTPMethod, endpoint: str, **kwargs: Any
    ) -> Dict[str, Any]:
        if method == HTTPMethod.GET and endpoint == "/database/":
            return {
                "result": [
                    {"id": MOCK_DATABASE_ID, "database_name": MOCK_DATABASE_NAME}
                ]
            }
        elif method == HTTPMethod.GET and endpoint == "/dataset/":
            return {"result": [{"id": 123, "table_name": MOCK_DATASET_NAME}]}
        elif method == HTTPMethod.POST and "csv_upload" in endpoint:
            return
        else:
            return {"message": "Mock response"}


class MockSupersetApi(Mock_SupersetApiBase):
    def get_database_id(self, _database_name):
        return MOCK_DATABASE_ID

    def upload_csv_to_database(
        self, database_id, table_name, csv_data, schema, column_dates, replace
    ):
        pass

    def get_dataset_id(self, dataset_name):
        return MOCK_DATASET_ID
