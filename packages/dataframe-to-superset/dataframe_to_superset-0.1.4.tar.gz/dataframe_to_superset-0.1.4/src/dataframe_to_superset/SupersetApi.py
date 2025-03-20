import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from http import HTTPMethod
from threading import Lock
from typing import Any, Dict, List, Tuple, Union

import requests

log = logging.getLogger()


class _SupersetApiBase:
    """
    Base class for interacting with the Superset API.

    Handles authentication, token refresh, and making requests.
    """

    def __init__(self, base_url: str, username: str, password: str, provider: str):
        """
        Initializes the Superset API base class.

        Args:
            base_url (str): The base URL of the Superset instance.
            username (str): The username for authentication.
            password (str): The password for authentication.
            provider (str): The authentication provider.
        """
        self.api_url = f"{base_url}/api/v1"
        self.username = username
        self.password = password
        self.provider = provider
        self.access_token = None
        self.refresh_token = None
        self.lock = Lock()
        self._authenticate()

    def _authenticate(self) -> None:
        """
        Authenticates with the Superset API and obtains access and refresh tokens.
        """
        payload = {
            "username": self.username,
            "password": self.password,
            "provider": self.provider,
            "refresh": True,
        }
        try:
            response = requests.post(f"{self.api_url}/security/login", json=payload)
            response.raise_for_status()
            tokens = response.json()
            self.access_token = tokens["access_token"]
            self.refresh_token = tokens["refresh_token"]
            log.debug("Authentication successful")
        except requests.RequestException as e:
            log.error(f"Authentication failed: {e}")
            raise

    def _refresh(self) -> None:
        """
        Refreshes the access token using the refresh token.
        """
        payload = {"refresh_token": self.refresh_token}
        try:
            response = requests.post(f"{self.api_url}/security/refresh", json=payload)
            if response.status_code == 401:
                self._authenticate()
            else:
                response.raise_for_status()
                tokens = response.json()
                self.access_token = tokens["access_token"]
                self.refresh_token = tokens["refresh_token"]
                log.info("Token refresh successful")
        except requests.RequestException as e:
            log.error(f"Token refresh failed: {e}")
            raise

    def _request(
        self, method: HTTPMethod, endpoint: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """
        Makes a request to the Superset API.

        Args:
            method (HTTPMethod): The HTTP method to use for the request.
            endpoint (str): The API endpoint to request.
            kwargs (Any): Additional arguments to pass to the request.

        Returns:
            dict: The JSON response from the API.

        Raises:
            requests.RequestException: If the request fails.
        """
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {self.access_token}"
        try:
            response = requests.request(
                method, f"{self.api_url}{endpoint}", headers=headers, **kwargs
            )
            if response.status_code == 401:
                with self.lock:
                    self._refresh()
                    headers["Authorization"] = f"Bearer {self.access_token}"
                    response = requests.request(
                        method, f"{self.api_url}{endpoint}", headers=headers, **kwargs
                    )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            log.error(f"Request to {endpoint} failed: {e}")
            raise

    def _parallel_requests(
        self, requests_list: List[Tuple[HTTPMethod, str, Dict[str, Any]]]
    ) -> List[Dict[str, Any]]:
        """
        Makes multiple requests to the Superset API in parallel.

        Args:
            requests_list (List[Tuple[HTTPMethod, str, Dict[str, Any]]]): A list of tuples containing the HTTP method,
                                                                          endpoint, and arguments for each request.

        Returns:
            List[dict]: A list of JSON responses from the API.
        """
        results = []
        with ThreadPoolExecutor() as executor:
            future_to_request = {
                executor.submit(self.request, *request): request
                for request in requests_list
            }
            for future in as_completed(future_to_request):
                request = future_to_request[future]
                try:
                    results.append(future.result())
                except Exception as e:
                    log.error(f"Request {request} failed: {e}")
        return results


class SupersetApi(_SupersetApiBase):
    """
    Class for interacting with the Superset API.

    Provides methods for making requests and performing common operations.
    """

    def request(
        self, method: HTTPMethod, endpoint: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """
        Makes a request to the Superset API.

        Args:
            method (HTTPMethod): The HTTP method to use for the request.
            endpoint (str): The API endpoint to request.
            kwargs (Any): Additional arguments to pass to the request.

        Returns:
            dict: The JSON response from the API.
        """
        return self._request(method, endpoint, **kwargs)

    def parallel_requests(
        self, requests_list: List[Tuple[HTTPMethod, str, Dict[str, Any]]]
    ) -> List[Dict[str, Any]]:
        """
        Makes multiple requests to the Superset API in parallel.

        Args:
            requests_list (List[Tuple[HTTPMethod, str, Dict[str, Any]]]): A list of tuples containing the HTTP method,
                                                                          endpoint, and arguments for each request.

        Returns:
            List[dict]: A list of JSON responses from the API.
        """
        return self._parallel_requests(requests_list)

    def get_database_id(self, database_name: str) -> Union[int, None]:
        """
        Retrieves the ID of a database by its name.

        Args:
            database_name (str): The name of the database.

        Returns:
            int or None: The ID of the database, or None if not found.
        """
        try:
            response = self.request(HTTPMethod.GET, "/database/")
            databases = response["result"]
            for db in databases:
                if db.get("database_name") == database_name:
                    return db.get("id")
        except Exception as e:
            log.error(f"Failed to get database ID for {database_name}: {e}")
        return None

    def upload_csv_to_database(
        self,
        database_id: int,
        table_name: str,
        csv_data: str,
        schema: str = "public",
        column_dates: List[str] = None,
        overwrite: bool = True,
    ) -> Dict[str, Any]:
        """
        Uploads a CSV file to a database.

        Args:
            database_id (int): The ID of the database.
            table_name (str): The name of the table to create or overwrite.
            csv_data (str): The CSV data to upload.
            schema (str, optional): The schema of the table. Defaults to "public".
            column_dates (List[str], optional): A list of columns to treat as dates. Defaults to None.
            overwrite (bool, optional): Whether to overwrite the table if it already exists. Defaults to True.

        Returns:
            dict: The JSON response from the API.

        Raises:
            Exception: If the upload fails.
        """
        files = {
            "already_exists": (None, "replace" if overwrite else "fail"),
            "table_name": (None, table_name),
            "schema": (None, schema),
            "file": ("data.csv", csv_data),
        }

        if column_dates:
            files["column_dates"] = (None, ",".join(column_dates))

        try:
            return self.request(
                HTTPMethod.POST, f"/database/{database_id}/csv_upload/", files=files
            )
        except Exception as e:
            log.error(f"Failed to upload CSV to database {database_id}: {e}")
            raise

    def get_dataset_id(self, dataset_name: str) -> Union[int, None]:
        """
        Retrieves the ID of a dataset by its name.

        Args:
            dataset_name (str): The name of the dataset.

        Returns:
            int or None: The ID of the dataset, or None if not found.
        """
        try:
            response = self.request(HTTPMethod.GET, "/dataset/")
            datasets = response["result"]
            for dataset in datasets:
                if dataset.get("table_name") == dataset_name:
                    return dataset.get("id")
        except Exception as e:
            log.error(f"Failed to get dataset ID for {dataset_name}: {e}")
        return None

    def create_dataset(
        self,
        database_id: int,
        table_name: str,
        schema: str,
        owners: List[int],
        sql: str = None,
    ) -> Dict[str, Any]:
        """
        Creates a new dataset.

        Args:
            database_id (int): The ID of the database.
            table_name (str): The name of the table.
            schema (str): The schema of the table.
            owners (List[int]): A list of owner IDs.
            sql (str, optional): The SQL query to use for the dataset. Defaults to None.

        Returns:
            dict: The JSON response from the API.

        Raises:
            Exception: If the dataset creation fails.
        """
        if sql is None:
            sql = f"SELECT * FROM {schema}.{table_name}"
        payload = {
            "always_filter_main_dttm": False,
            "catalog": "",
            "database": database_id,
            "external_url": "",
            "is_managed_externally": True,
            "normalize_columns": False,
            "owners": owners,
            "schema": schema,
            "sql": sql,
            "table_name": table_name,
        }
        try:
            return self.request(HTTPMethod.POST, "/dataset/", json=payload)
        except Exception as e:
            log.error(f"Failed to create dataset for table {table_name}: {e}")
            raise
