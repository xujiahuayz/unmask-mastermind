# from os import path
# from extraction.cloudburst_tables_connection import CloudburstDataBaseConnection
# import pandas as pd
# from environ.settings import PROJECT_ROOT

"""
Query for extracting and filtering pumps from cloudburst data and saves data to disk
"""

TIME_PUMP_SIGNAL_COL_NAMES = [
    "message_text",
    "pid",
    "signal_type",
    "exchanges",
    "commodity",
    "base_commodity",
    "source_datetime",
    "source_datetime_raw",
    "entity_id",
]

SIGNALS_TIME_PUMP_QUERY = (
    "SELECT "
    + ", ".join(TIME_PUMP_SIGNAL_COL_NAMES)
    + """
from cloudburst_signals
where signal_type = 'buy'
and commodity != 'BTC'
and entry_price_range IS NULL
and target_prices IS NULL
and exchanges != '[]' and exchanges != '["Hotbit"]'
and LENGTH(message_text) < 17
ORDER BY entity_id, source_datetime desc
"""
)

# TODO Limit for testing

# if __name__ == "__main__":

#     # Connect to cloudburst database
#     time_pump_signals = CloudburstDataBaseConnection.fetch_data(SIGNALS_TIME_PUMP_QUERY)

#     df_time_pump_signals = pd.DataFrame(time_pump_signals)
#     df_time_pump_signals.to_csv(
#         path.join(PROJECT_ROOT, "data", "time_pump_signals.csv")
#     )
