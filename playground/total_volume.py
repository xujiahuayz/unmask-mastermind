from os import path
import pandas as pd
from pdenv.setting import PROJECT_ROOT


# # read data into dataframe
df_time_pump = pd.read_csv(path.join(PROJECT_ROOT, "data", "processed_time_pumps.csv"))
df_crowd_pump = pd.read_csv(
    path.join(PROJECT_ROOT, "data", "processed_crowd_pumps_data.csv")
)


df_aggregated_crowd_pump = pd.DataFrame()
df_aggregated_crowd_pump["time_to_day"] = pd.to_datetime(
    df_crowd_pump["source_date_time"]
).dt.floor("d")
df_aggregated_crowd_pump["total_volume"] = df_crowd_pump["total_volume"]
df_aggregated_crowd_pump["entity_id"] = df_crowd_pump["entity_id"]
df_aggregated_crowd_pump["commodity"] = df_crowd_pump["commodity"]

# TODO aggregate time to day, commodity
df_grouped_crowd_pump = df_aggregated_crowd_pump.groupby(["time_to_day", "commodity"])
df_aggregated_crowd_pump_volumes = df_grouped_crowd_pump["total_volume"].max()


# no of pumps
no_time_pump = len(df_time_pump)
no_crowd_pump = len(df_aggregated_crowd_pump_volumes)

# Totla volume
time_pump_total = df_time_pump["total_volume"].sum()
crowd_pump_total = df_aggregated_crowd_pump_volumes.sum()

# date range
time_pump_range = pd.to_datetime(df_time_pump["source_date_time"]).sort_values(
    ascending=False
)
time_pump_days = (time_pump_range.iloc[0] - time_pump_range.iloc[-1]).days
crowd_pump_range = pd.to_datetime(df_crowd_pump["source_date_time"]).sort_values(
    ascending=False
)
crowd_pump_days = (crowd_pump_range.iloc[0] - crowd_pump_range.iloc[-1]).days

# Unique entity_id
no_time_pump_entity_id = len(df_time_pump["entity_id"].unique())
no_crowd_pump_entity_id = len(df_crowd_pump["entity_id"].unique())


# We calculate the average total volume per channel per day over
# the past 1479 days for time pump and 686 days for crowd pump
# time_pump_avg = time_pump_total_volumes / time_pump_days / no_time_pump_channels
# crowd_pump_avg = crowd_pump_totla_volumes / crowd_pump_days / no_crowd_pump_channels
annual_trascations_from_one_time_pump_channel = (
    time_pump_total / no_time_pump_entity_id / time_pump_days * 365
)
annual_trascations_from_one_crowd_pump_channel = (
    crowd_pump_total / no_crowd_pump_entity_id / crowd_pump_days * 365
)


# Total channels 300
annual_total_volumes_of_pump_and_dump = (
    annual_trascations_from_one_time_pump_channel * 19
    + annual_trascations_from_one_crowd_pump_channel * 19
)
