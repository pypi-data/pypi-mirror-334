import logging
import uuid
import pandas as pd
from typing import Literal, Dict, Any, Union
from .SupersetApi import SupersetApi

# Configure logging for the module
log = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@pd.api.extensions.register_dataframe_accessor("superset")
class SupersetAccessor:
    """
    A pandas DataFrame accessor for uploading data to Superset.

    This accessor allows users to configure a connection to a Superset instance
    and upload pandas DataFrames as datasets to a specified database in Superset.
    """

    _superset_api = None
    _superset_schema = "public"
    _superset_database_name = None
    _superset_base_url = None

    def __init__(self, pandas_obj: pd.DataFrame):
        """
        Initializes the SupersetAccessor with a pandas DataFrame.

        Args:
            pandas_obj (pd.DataFrame): The pandas DataFrame to which this accessor is attached.
        """
        self._obj = pandas_obj

    @classmethod
    def configure(
        cls,
        base_url: str,
        username: str,
        password: str,
        provider: Literal["ldap", "db"],
        database_name: str,
        schema: str = "public",
    ) -> None:
        """
        Configures the class-level Superset API and shared settings.

        This method must be called once before using the accessor. It sets up the
        connection to the Superset instance and specifies the target database and schema.

        Args:
            base_url (str): The base URL of the Superset instance.
            username (str): The username for Superset authentication.
            password (str): The password for Superset authentication.
            provider (Literal["ldap", "db"]): The authentication provider.
            database_name (str): The name of the database in Superset.
            schema (str, optional): The schema name in the database. Defaults to "public".
        """
        cls._superset_api = SupersetApi(base_url, username, password, provider)
        cls._superset_schema = schema
        cls._superset_database_name = database_name
        cls._superset_base_url = base_url
        log.info("SupersetAccessor configured successfully")

    @staticmethod
    def _validate(obj: pd.DataFrame) -> None:
        """
        Validates the DataFrame to ensure required columns are present.

        Args:
            obj (pd.DataFrame): The DataFrame to validate.

        Raises:
            AttributeError: If required columns are missing.
        """
        if "latitude" not in obj.columns or "longitude" not in obj.columns:
            raise AttributeError(
                "The DataFrame must contain 'latitude' and 'longitude' columns."
            )

    def as_datasource(
        self, dataset_name: str = None, verbose_return: bool = False
    ) -> Union[Dict[str, Any], str]:
        """
        Uploads the DataFrame to Superset as a dataset.

        Converts the DataFrame to a CSV format and uploads it to the configured
        Superset instance. The dataset is stored in the specified database and schema.

        Args:
            dataset_name (str, optional): The name of the dataset in Superset. If not provided,
                                          a unique name is generated automatically.
            verbose_return (bool, optional): If True, returns detailed information
                                             about the uploaded dataset. Defaults to False.

        Returns:
            Union[Dict[str, Any], str]: If `verbose_return` is True, returns a dictionary with detailed
                                        information (dataset ID, name, and URL). Otherwise, returns the
                                        dataset URL as a string.

        Raises:
            ValueError: If the dataset ID cannot be retrieved after uploading.
        """
        if not self._superset_api or not self._superset_database_name:
            raise ValueError(
                "SupersetAccessor is not configured. Call `SupersetAccessor.configure()` first."
            )

        dataset_name = dataset_name or f"generated_dataset_{uuid.uuid4().hex}"
        csv_data = self._obj.to_csv(index=False)

        date_columns = [
            col
            for col in self._obj.columns
            if pd.api.types.is_datetime64_any_dtype(self._obj[col])
        ]

        try:
            database_id = self._superset_api.get_database_id(
                self._superset_database_name
            )
            if database_id is None:
                raise ValueError(
                    f"Database '{self._superset_database_name}' not found in Superset"
                )

            self._superset_api.upload_csv_to_database(
                database_id=database_id,
                table_name=dataset_name,
                csv_data=csv_data,
                schema=self._superset_schema,
                column_dates=date_columns,
            )

            dataset_id = self._superset_api.get_dataset_id(dataset_name)
            if dataset_id is None:
                raise ValueError(f"Failed to retrieve dataset ID for '{dataset_name}'")

            url = f"{self._superset_base_url}/explore/?datasource_type=table&datasource_id={dataset_id}"
            log.info(f"Dataset '{dataset_name}' uploaded successfully to Superset")

            return (
                {"dataset_id": dataset_id, "name": dataset_name, "url": url}
                if verbose_return
                else url
            )
        except Exception as e:
            log.error(f"Failed to upload dataset '{dataset_name}' to Superset: {e}")
            raise
