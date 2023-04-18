"""
Download signals from cloudburst database
"""
import logging
import pandas as pd

from environ.extraction.cloudburst_database import cloudburst_connection

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

CROWD_SIGNALS_QUERY = """
    SELECT
        pid,
        entity_id,
        source_datetime,
        exchanges_array,
        commodity,
        base_commodity,
        entry_price_range,
        target_prices,
        stop_loss,
        signal_position,
        crowd_score,
        time_score,
        CASE WHEN (LENGTH(message_text) < 15 AND LENGTH(message_text) > 0) THEN 'time'
            WHEN (LENGTH(message_text) > 15) THEN 'crowd'
        END as pump_type
    FROM cloudburst_signals
    WHERE signal_type = 'buy'
    AND LENGTH(message_text) > 1
    AND commodity IS NOT NULL
    AND (crowd_score IS NOT NULL)
    """

TIME_SIGNALS_QUERY = """
    SELECT
        pid,
        entity_id,
        source_datetime,
        exchanges_array,
        commodity,
        base_commodity,
        entry_price_range,
        target_prices,
        stop_loss,
        signal_position,
        crowd_score,
        time_score,
        CASE WHEN (LENGTH(message_text) < 15 AND LENGTH(message_text) > 0) THEN 'time'
            WHEN (LENGTH(message_text) > 15) THEN 'crowd'
        END as pump_type
    FROM cloudburst_signals
    WHERE signal_type = 'buy'
    AND LENGTH(message_text) > 1
    AND commodity IS NOT NULL
    AND (LENGTH(message_text) < 15 AND LENGTH(message_text) > 0)
    AND (time_score IS NOT NULL)
    """


def get_signals(type: str):
    """
    Get signals from cloudburst database
    :return: pandas.DataFrame
    """
    if type == "time":
        logger.info("Getting time signals")
        return cloudburst_connection(TIME_SIGNALS_QUERY)
    elif type == "crowd":
        logger.info("Getting crowd signals")
        return cloudburst_connection(CROWD_SIGNALS_QUERY)
    else:
        logger.info("Specify signal type: time or crowd")
        return pd.DataFrame()
