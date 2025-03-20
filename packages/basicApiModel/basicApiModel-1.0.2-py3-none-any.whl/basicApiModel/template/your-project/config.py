import json
import base64
import logging
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnviromentSettings(BaseSettings):
    DEBUG: bool = False

    # External variables

    # Big Query service accounts
    BIGQUERY_SERVICE_ACCOUNT: str

    # Logger table
    LOG_DATASET_ERROR: str

    model_config = SettingsConfigDict(
        env_file=".env",
    )


env_settings = EnviromentSettings()

service_account_json = base64.b64decode(
    env_settings.BIGQUERY_SERVICE_ACCOUNT).decode("utf-8")
service_account = json.loads(service_account_json)

if env_settings.DEBUG:
    logging.basicConfig(level=logging.DEBUG,
                        format="%(levelname)s: %(message)s")
else:
    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s: %(message)s")
