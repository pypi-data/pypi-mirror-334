from PROJECT_NAME.models.big_query import BigQueryApi
from PROJECT_NAME.services import date
from PROJECT_NAME.config import (env_settings as env,
                                 service_account)


class Logger:
    """
    A class that provides methods to create log for BigQuery.

    Attributes:
        __bigquery_api (BigQueryApi): BigQueryApi instance
        __table (str): table id for insert logs
    """
    __bigquery_api = None
    __table = env.LOG_DATASET_ERROR

    def __init__(self) -> None:
        if Logger.__bigquery_api is None:
            Logger.__bigquery_api = BigQueryApi(
                service_account)

    def create_log(self, user: str, owner: str,
                   status: str, detail: str, plataform: str) -> None:

        row = [{"datetime": date.now_datetime(),
                "user": user,
                "owner": owner,
                "status": status,
                "detail": detail,
                "plataform": plataform}]

        Logger.__bigquery_api.insert_row(
            row=row,
            table=Logger.__table
            )
