from os import path
from environ.extraction.cloudburst_tables_connection import (
    CloudburstDataBaseConnection,
)
from environ.settings import PROJECT_ROOT
import pandas as pd
import matplotlib.pyplot as plt



query_hourly_messages = """SELECT 
    EXTRACT(hour from source_datetime) AS HourOfDay, 
    COUNT(*) AS message_text
FROM 
    cloudburst_signals
GROUP BY 
    HourOfDay
"""


hourly_messages = CloudburstDataBaseConnection.fetch_data(query_hourly_messages)

df_hourly_messages = pd.DataFrame(
    hourly_messages, columns=["Hour of day", "message text"]
)

df_hourly_messages = df_hourly_messages.sort_values(by="Hour of day", ascending=True)


fig = plt.bar(df_hourly_messages["Hour of day"], df_hourly_messages["message text"])
plt.xticks(df_hourly_messages["Hour of day"])
plt.xlabel("Hour of Day")
plt.ylabel("Message Count")
plt.title("Message Counts by Hour of Day")
plt.savefig(path.join(PROJECT_ROOT, "exhibit", "message_counts_by_hour_of_day.pdf"))
plt.show()
