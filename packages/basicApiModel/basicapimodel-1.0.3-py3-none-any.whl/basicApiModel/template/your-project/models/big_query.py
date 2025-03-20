import json
import logging

from google.cloud.bigquery import Client
from google.oauth2.service_account import Credentials


class BigQueryApi:
    """
    A class that provides methods to interact with BigQuery.

    Args:
        service_account (json): Big Query service account to access project

    Attributes:
        __credentials (bigquery.Credentials): The Big Query Credentials
        __client (bigquery.Client): The Big Query Client
    """

    def __init__(self, service_account: json) -> None:
        self.__credentials = Credentials.from_service_account_info(
            service_account
            )
        self.__client = Client(
            credentials=self.__credentials,
            project=self.__credentials.project_id
        )

    def insert_row(self, row: list, table: str) -> None:
        errors = self.__client.insert_rows_json(table=table, json_rows=row)

        if errors:
            logging.error(f"BigQuery exception: {errors}")
            raise Exception(f"BigQuery exception: {errors}")
        logging.info(f"Inserted row: {row}")
