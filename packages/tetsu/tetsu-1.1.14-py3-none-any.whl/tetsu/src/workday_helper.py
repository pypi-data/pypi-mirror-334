from __future__ import annotations

import ast
import datetime as dt
import json
import os

import importlib_resources
import pandas as pd
import requests

from tetsu.src import cloudant_helper


def workday_extraction(input_date: dt.datetime | str,
                       cloudant_doc: dict = None) -> str:
    """Extracts the workday from the epm workday calendar.
    Example:
        today = dt.datetime.now()
        wd = workday_extraction(today)

    :param input_date (str or timestamp): expects a date as string or timestamp
    :param cloudant_doc: Cloudant document for credentials retrieval

    :returns: workday
    """

    if cloudant_doc is None:
        cloudant_doc = ast.literal_eval(os.getenv("cloudant_document"))

    try:
        # ---- Extract JSON ----------------------------------------------------------------------------#
        creds = cloudant_helper.get_credentials(doc=cloudant_doc, creds={"api_key": ["workday_calendar_api_key"]})

        # Extract date
        input_year = input_date.year
        input_month = str(input_date.month).zfill(2)
        input_day = str(input_date.day).zfill(2)

        custom_dates_url = 'https://production.epm-web-platform.dal.app.cirrus.ibm.com/api/calendar/queryCustomDatesByDate?date='  # noqa: E501
        resources = importlib_resources.files("tetsu")

        raw_json = requests.get(
            custom_dates_url + f"{input_year}%2F{input_month}%2F{input_day}&key=" + creds["api_key"],
            timeout=600,
            verify=resources.joinpath("config", "root.pem"))

        try:
            # ---- Convert JSON to Dataframe ---------------------------------------------------------------#
            data = json.loads(raw_json.content)
            df = pd.DataFrame(data)
            # Convert String to Timestamp and Normalize time component
            workday = df['customDateName'].iloc[0]

        except Exception:
            workday = None

        return workday

    except Exception as e:
        print('Workday Calendar Failed\n')
        raise e
