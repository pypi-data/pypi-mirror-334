import json
import os

from google.cloud import bigquery
from google.oauth2 import service_account

from hawk_sdk.core.common.constants import PROJECT_ID


def get_bigquery_client() -> bigquery.Client:
    if 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ:
        # Initialize the client using the json file in the environment variable
        return bigquery.Client(project=PROJECT_ID)

    else:
        # Load the service account credentials from the JSON string
        service_account_json = os.environ.get('SERVICE_ACCOUNT_JSON')
        credentials = service_account.Credentials.from_service_account_info(
            json.loads(service_account_json)
        )
        return bigquery.Client(project=PROJECT_ID, credentials=credentials)
