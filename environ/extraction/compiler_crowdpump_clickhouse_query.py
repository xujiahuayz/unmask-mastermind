"""
This script compiles SQL query for time pump all processing
"""
from extraction.crowd_pumps_detection import (
    CROWD_SIGNALS_COL_NAMES,
)
from extraction.hist_data_clickhouse_query import (
    HIST_PRICES_COL_NAMES_CLICKHOUSE,
)

TIMESTAMP_24_HOURS = 60 * 60 * 24
TIMESTAMP_15_DAYS = 15 * 24 * 60 * 60


def compile_crowdpump_query(
    crowd_pump_signals: list[tuple],
) -> str:
    """
    This function write specific SQL query to extract crowd pump data
    (specific to commodity and time range)
    ----Input----
    time_pump_signals: time pump signals from various channels
    ----Output----
    specific query to extract data for time pump all processing
    """
    list_conditioned_query = []
    for i in crowd_pump_signals[1:]:
        list_conditioned_query.append(
            """
    OR (commodity = '%s' and timestamp >= %s and timestamp <= %s)"""
            % (
                i[CROWD_SIGNALS_COL_NAMES.index("commodity")],
                int(
                    i[CROWD_SIGNALS_COL_NAMES.index("source_datetime_raw")]
                    - TIMESTAMP_24_HOURS
                ),
                int(
                    i[CROWD_SIGNALS_COL_NAMES.index("source_datetime_raw")]
                    + TIMESTAMP_15_DAYS
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
            crowd_pump_signals[0][CROWD_SIGNALS_COL_NAMES.index("commodity")],
            int(
                crowd_pump_signals[0][
                    CROWD_SIGNALS_COL_NAMES.index("source_datetime_raw")
                ]
                - TIMESTAMP_24_HOURS
            ),
            int(
                crowd_pump_signals[0][
                    CROWD_SIGNALS_COL_NAMES.index("source_datetime_raw")
                ]
                + TIMESTAMP_15_DAYS
            ),
        )
        + "".join(list_conditioned_query)
        + """
            ORDER BY timestamp
            """
    )

    return query_conditioned
