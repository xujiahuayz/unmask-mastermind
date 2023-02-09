"""
Query for importing cryptocompare table from clickhouse
"""

HIST_PRICES_COL_NAMES_CLICKHOUSE = [
    "timestamp",
    "exchange",
    "commodity",
    "base_commodity",
    "open",
    "close",
    "low",
    "high",
    "volume_from",
    "volume_to",
]

HIST_PRICES_COL_NAMES_CLICKHOUSE_QUERY = HIST_PRICES_COL_NAMES_CLICKHOUSE.copy()
HIST_PRICES_COL_NAMES_CLICKHOUSE_QUERY[
    HIST_PRICES_COL_NAMES_CLICKHOUSE.index("timestamp")
] = "toUnixTimestamp(timestamp)"


# TODO LIMIT FOR TESTING
HIST_PRICES_QUERY_CLICKHOUSE = (
    "SELECT "
    # replace a strig with another in a list and join to the query
    + ", ".join(HIST_PRICES_COL_NAMES_CLICKHOUSE_QUERY)
    + """
FROM cryptocompare.cryptocompare_minute_by_minute ORDER BY timestamp desc 
"""
)
