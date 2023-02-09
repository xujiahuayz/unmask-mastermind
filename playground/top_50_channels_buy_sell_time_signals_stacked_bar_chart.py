from os import path
from environ.extraction.cloudburst_tables_connection import (
    CloudburstDataBaseConnection,
)
from environ.settings import PROJECT_ROOT
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# query_number_of_exchanges = (
#     """select count(distinct(exchanges)) from cloudburst_signals"""
# )
# no_exchanges = CloudburstDataBaseConnection.fetch_data(query_number_of_exchanges)[0][0]

# query_number_of_commodities = """
#     select count(distinct(exchanges)) from cloudburst_signals
#     """
# no_commodities = CloudburstDataBaseConnection.fetch_data(query_number_of_commodities)[
#     0
# ][0]

# query_number_of_channels = """
# select count(distinct(entity_id)) from cloudburst_signals

# """
# no_channels = CloudburstDataBaseConnection.fetch_data(query_number_of_channels)[0][0]

# query_number_of_signals_type = """
# SELECT signal_type, count(*)
# FROM cloudburst_signals
# GROUP BY signal_type
# """

# no_signals_type = CloudburstDataBaseConnection.fetch_data(query_number_of_signals_type)


# query_number_of_attributes_based_type = """SELECT signal_type,
#        COUNT(DISTINCT exchanges),
#        COUNT(DISTINCT commodity),
#        COUNT(DISTINCT entity_id),
# 	   COUNT(DISTINCT message_text)
# FROM cloudburst_signals
# GROUP BY signal_type;
# """

# attributes_summary = CloudburstDataBaseConnection.fetch_data(
#     query_number_of_attributes_based_type
# )
# df_attributes_summary = pd.DataFrame(
#     attributes_summary,
#     columns=["signal_type", "exchanges", "commodities", "channels", "messages"],
# )
# df_attributes_summary.to_latex("attributes_summary.tex", index=False)


query_different_signals_per_channel = """
SELECT entity_id,
       SUM(CASE WHEN signal_type = 'time' THEN 1 ELSE 0 END) as time_signals,
       SUM(CASE WHEN signal_type = 'buy' THEN 1 ELSE 0 END) as buy_signals,
       SUM(CASE WHEN signal_type = 'sell' THEN 1 ELSE 0 END) as sell_signals
FROM cloudburst_signals
GROUP BY entity_id;
"""

type_per_channel_summary = CloudburstDataBaseConnection.fetch_data(
    query_different_signals_per_channel
)

df_type_per_channel_summary = pd.DataFrame(
    type_per_channel_summary, columns=["channel", "time", "buy", "sell"]
)

df_type_per_channel_summary["sum"] = (
    df_type_per_channel_summary["time"]
    + df_type_per_channel_summary["sell"]
    + df_type_per_channel_summary["buy"]
)

df_type_per_channel_summary = df_type_per_channel_summary.sort_values(
    by="sum", ascending=False
)


df_type_per_channel_summary = df_type_per_channel_summary[:50]

fig, ax = plt.subplots()

index = np.arange(len(df_type_per_channel_summary["channel"]))

bar1 = ax.bar(index, df_type_per_channel_summary["buy"], label="Buy")
bar2 = ax.bar(
    index,
    df_type_per_channel_summary["sell"],
    bottom=df_type_per_channel_summary["buy"],
    label="Sell",
)
bar3 = ax.bar(
    index,
    df_type_per_channel_summary["time"],
    bottom=df_type_per_channel_summary["buy"] + df_type_per_channel_summary["sell"],
    label="Time",
)


ax.set_xlabel("Channels")
ax.set_ylabel("Amount")
ax.set_title("Top 50 channels buy, sell, and tIme signals stacked bar chart")
ax.set_xticks(index)

ax.set_xticklabels([])
ax.set_xticks([])


ax.legend()
plt.show()

fig.savefig(path.join(PROJECT_ROOT, "exhibit","top_50_channels_buy_sell_time_signals_stacked_bar_chart.pdf"), format="pdf")


# query_for_all_entities ="""
# select distinct(entity_id)
# from cloudburst_signals
# """

# type_per_channel_summary = CloudburstDataBaseConnection.fetch_data(
#     query_for_all_entities
# )

# df_type_per_channel_summary = pd.DataFrame(type_per_channel_summary)
# df_type_per_channel_summary.columns = ["channel"]
# df_type_per_channel_summary.to_csv("all_entities.csv", index=False)