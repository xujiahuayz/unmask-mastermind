import psycopg2
from environ.config import (
    CLOUDBURST_HOST,
    CLOUDBURST_USERNAME,
    CLOUDBURST_PASS,
)


def cloudburst_connection(
    sql_query: str,
    db_username=CLOUDBURST_USERNAME,
    db_password=CLOUDBURST_PASS,
    db_host=CLOUDBURST_HOST,
    db_port=25060,
) -> list[tuple]:
    """
    Establish connection with cloudburst database
    """
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        user=db_username,
        password=db_password,
        database="cloudburst",
    )

    cursor = conn.cursor()
    cursor.execute(sql_query)
    return cursor.fetchall()
