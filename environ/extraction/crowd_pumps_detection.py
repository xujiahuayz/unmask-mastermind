"""
Query for extracting and filtering pumps from cloudburst data and saves data to disk
"""

CROWD_SIGNALS_COL_NAMES = [
    "pid",
    "signal_type",
    "exchanges",
    "commodity",
    "base_commodity",
    "entry_price_range",
    "target_prices",
    "stop_loss",
    "source_datetime",
    "source_datetime_raw",
    "entity_id",
]

CROWD_PUMP_SIGNALS_QUERY = (
    "SELECT "
    + ", ".join(CROWD_SIGNALS_COL_NAMES)
    + """
FROM cloudburst_signals
WHERE signal_type = 'buy'
AND commodity IS NOT NULL
and commodity != 'BTC'
and commodity != 'ETH'
AND exchanges != '[]' and exchanges != '["Hotbit"]' and exchanges != '["BitMEX"]'
AND base_commodity IS NOT NULL
AND entry_price_range IS NOT NULL
AND target_prices IS NOT NULL
AND source_datetime < current_date - 10
ORDER BY source_datetime DESC
"""
)
# TODO DATE AND LIMIT FOR TESTING
