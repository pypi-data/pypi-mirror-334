"""
@description: Repository layer for fetching Equities data from BigQuery.
@author: Rithwik Babu
"""
import logging
from typing import Iterator, List

from google.cloud import bigquery

from hawk_sdk.core.common.utils import get_bigquery_client


class EquitiesRepository:
    """Repository for accessing Equities raw data."""

    def __init__(self, environment: str) -> None:
        """Initializes the repository with a BigQuery client.

        :param environment: The environment to fetch data from (e.g., 'production', 'development').
        """
        self.bq_client = get_bigquery_client()
        self.environment = environment

    def fetch_adjusted_ohlc(self, start_date: str, end_date: str, interval: str, hawk_ids: List[int]) -> Iterator[dict]:
        """Fetches raw adjusted OHLC data from BigQuery for the given date range and hawk_ids using query parameters."""
        query = f"""
        WITH records_data AS (
          SELECT 
            r.record_timestamp AS date,
            hi.value AS ticker,
            MAX(CASE WHEN f.field_name = @open_field THEN r.double_value END) AS open,
            MAX(CASE WHEN f.field_name = @high_field THEN r.double_value END) AS high,
            MAX(CASE WHEN f.field_name = @low_field THEN r.double_value END) AS low,
            MAX(CASE WHEN f.field_name = @close_field THEN r.double_value END) AS close
          FROM 
            `wsb-hc-qasap-ae2e.{self.environment}.records` AS r
          JOIN 
            `wsb-hc-qasap-ae2e.{self.environment}.fields` AS f
            ON r.field_id = f.field_id
          JOIN 
            `wsb-hc-qasap-ae2e.{self.environment}.hawk_identifiers` AS hi
            ON r.hawk_id = hi.hawk_id
          WHERE 
            r.hawk_id IN UNNEST(@hawk_ids)
            AND f.field_name IN (@open_field, @high_field, @low_field, @close_field)
            AND r.record_timestamp BETWEEN @start_date AND @end_date
          GROUP BY 
            date, ticker
        )
        SELECT DISTINCT
          date,
          ticker,
          open,
          high,
          low,
          close,
        FROM 
          records_data
        ORDER BY 
          date;
        """

        query_params = [
            bigquery.ArrayQueryParameter("hawk_ids", "INT64", hawk_ids),
            bigquery.ScalarQueryParameter("start_date", "STRING", start_date),
            bigquery.ScalarQueryParameter("end_date", "STRING", end_date),
            bigquery.ScalarQueryParameter("open_field", "STRING", f"adjusted_open_{interval}"),
            bigquery.ScalarQueryParameter("high_field", "STRING", f"adjusted_high_{interval}"),
            bigquery.ScalarQueryParameter("low_field", "STRING", f"adjusted_low_{interval}"),
            bigquery.ScalarQueryParameter("close_field", "STRING", f"adjusted_close_{interval}")
        ]

        job_config = bigquery.QueryJobConfig(query_parameters=query_params)

        try:
            query_job = self.bq_client.query(query, job_config=job_config)
            return query_job.result()
        except Exception as e:
            logging.error(f"Failed to fetch OHLC data: {e}")
            raise
