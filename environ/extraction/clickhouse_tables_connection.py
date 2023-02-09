"""
Script for connecting with clickhouse data
"""
import time
from clickhouse_driver import Client
from environ.config import (
    CLICKHOUSE_URL,
    CLICKHOUSE_USER,
    CLICKHOUSE_PASSWORD,
    CLICKHOUSE_DATABASE,
)


def import_clickhouse_connection(query: str) -> list[tuple]:
    """
    For running this function we only need check that env variables
    adn provide a query appropriate to clickhouse
    """
    client = Client(
        host=CLICKHOUSE_URL,
        port=9000,
        user=CLICKHOUSE_USER,
        password=CLICKHOUSE_PASSWORD,
        database=CLICKHOUSE_DATABASE,
    )

    start = time.time()
    clickhouse_data = client.execute(query)
    end = time.time()
    print("Clickhouse data extraction duration: " + str(end - start))
    return clickhouse_data


if __name__ == "__main__":
    # Implementation example
    import_clickhouse_connection("show databases")
