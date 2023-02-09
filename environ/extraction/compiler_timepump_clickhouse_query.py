"""
This script compiles SQL query for time pump all processing
"""
from extraction.time_pumps_detection import (
    TIME_PUMP_SIGNAL_COL_NAMES,
)

# from scripts_extraction.hist_data_clickhouse_query import (
#     HIST_PRICES_COL_NAMES_CLICKHOUSE,
# )

TIMESTAMP_24_HOURS = 60 * 60 * 24
TIMESTAMP_30_MINUTES = 30 * 60


def compile_timepump_query(
    time_pump_signals: list[tuple],
) -> str:
    """
    This function write specific SQL query to extract time pump data
    (specific to commodity and time range)
    ----Input----
    time_pump_signals: time pump signals from various channels
    ----Output----
    specific query to extract data for time pump all processing
    """
    list_conditioned_query = []
    for i in time_pump_signals[1:]:
        list_conditioned_query.append(
            """
    OR (commodity = '%s' and timestamp >= %s and timestamp <= %s)"""
            % (
                i[TIME_PUMP_SIGNAL_COL_NAMES.index("commodity")],
                int(
                    i[TIME_PUMP_SIGNAL_COL_NAMES.index("source_datetime_raw")]
                    - TIMESTAMP_24_HOURS
                ),
                int(
                    i[TIME_PUMP_SIGNAL_COL_NAMES.index("source_datetime_raw")]
                    + TIMESTAMP_30_MINUTES
                ),
            )
        )

    query_conditioned = str(
        "SELECT Distinct toUnixTimestamp(timestamp) as timestamp, exchange, commodity, base_commodity, open, close, low, high, volume_from, volume_to"
        + """
    FROM cryptocompare.cryptocompare_minute_by_minute"""
        + """
    WHERE (commodity = '%s' and timestamp >= %s and timestamp <= %s)"""
        % (
            time_pump_signals[0][TIME_PUMP_SIGNAL_COL_NAMES.index("commodity")],
            int(
                time_pump_signals[0][
                    TIME_PUMP_SIGNAL_COL_NAMES.index("source_datetime_raw")
                ]
                - TIMESTAMP_24_HOURS
            ),
            int(
                time_pump_signals[0][
                    TIME_PUMP_SIGNAL_COL_NAMES.index("source_datetime_raw")
                ]
                + TIMESTAMP_30_MINUTES
            ),
        )
        + "".join(list_conditioned_query)
        + """
            ORDER BY timestamp
            """
    )

    return query_conditioned
