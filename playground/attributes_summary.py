from os import path
from environ.extraction.cloudburst_tables_connection import (
    CloudburstDataBaseConnection,
)
from environ.settings import PROJECT_ROOT
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# Could be modified to include more exchanges
query_number_of_exchanges = (
    """select count(distinct(exchanges)) from cloudburst_signals"""
)
no_exchanges = CloudburstDataBaseConnection.fetch_data(query_number_of_exchanges)[0][0]

query_number_of_commodities = """
    select count(distinct(commodity)) from cloudburst_signals
    """
no_commodities = CloudburstDataBaseConnection.fetch_data(query_number_of_commodities)[
    0
][0]

query_number_of_channels = """
select count(distinct(entity_id)) from cloudburst_signals

"""
no_channels = CloudburstDataBaseConnection.fetch_data(query_number_of_channels)[0][0]

query_number_of_signals_type = """
SELECT signal_type, count(*)
FROM cloudburst_signals
GROUP BY signal_type
"""

no_signals_type = CloudburstDataBaseConnection.fetch_data(query_number_of_signals_type)
df_no_signals_type = pd.DataFrame(no_signals_type, columns=["signal_type", "count"])
df_no_signals_type["count"] = df_no_signals_type["count"].astype(int)
no_signals = df_no_signals_type["count"].sum()


print(
    f"The total number of exchanges is {no_exchanges}, the total number of commodities is {no_commodities}, the total number of channels is {no_channels} and the total number of signals is {no_signals}"
)


query_number_of_attributes_based_type = """SELECT signal_type,
       COUNT(DISTINCT exchanges),
       COUNT(DISTINCT commodity),
       COUNT(DISTINCT entity_id),
	   COUNT(DISTINCT message_text)
FROM cloudburst_signals
GROUP BY signal_type;
"""

attributes_summary = CloudburstDataBaseConnection.fetch_data(
    query_number_of_attributes_based_type
)
df_attributes_summary = pd.DataFrame(
    attributes_summary,
    columns=["signal_type", "exchanges", "commodities", "channels", "messages"],
)
df_attributes_summary.to_latex(
    path.join(PROJECT_ROOT, "exhibit", "attributes_summary.tex"), index=False
)
