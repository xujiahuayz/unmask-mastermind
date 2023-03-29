from collections import OrderedDict
from os import path
import pickle
import numpy as np
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde


# Define the tick formatter function
def format_ticks(value, pos):
    if value >= 1e9:
        return "{:.0f}B".format(value / 1e9)
    elif value >= 1e6:
        return "{:.0f}M".format(value / 1e6)
    elif value >= 1e3:
        return "{:.0f}K".format(value / 1e3)
    else:
        return int(value)


from environ.settings import PROJECT_ROOT
from environ.extraction.crowd_pumps_detection import (
    CROWD_PUMP_SIGNALS_QUERY,
    CROWD_SIGNALS_COL_NAMES,
)
from environ.extraction.time_pumps_detection import (
    SIGNALS_TIME_PUMP_QUERY,
    TIME_PUMP_SIGNAL_COL_NAMES,
)
from environ.extraction.cloudburst_connection import cloudburst_connection

with open(path.join(PROJECT_ROOT, "data", "coin_cap.pkl"), "rb") as f:
    coin_cap = pickle.load(f)

crowd_pump_signals = cloudburst_connection(CROWD_PUMP_SIGNALS_QUERY)
time_pump_signals = cloudburst_connection(SIGNALS_TIME_PUMP_QUERY)


data = [i for i in list(coin_cap.values()) if i is not None]

log_data = [i for i in np.log10(data) if i > 3]
selected_data = [i for i in data if np.log10(i) > 3]


crowd_pump_cap = []
for i in crowd_pump_signals:
    try:
        crowd_pump_cap.append(coin_cap[i[CROWD_SIGNALS_COL_NAMES.index("commodity")]])
    except:
        continue
data_crowd = [i for i in crowd_pump_cap if i is not None]


non_duplicate_data_crowd = list(OrderedDict.fromkeys(data_crowd))
non_duplicate_log_data_crowd = np.log10(non_duplicate_data_crowd)


time_pump_cap = []
for i in time_pump_signals:
    try:
        time_pump_cap.append(coin_cap[i[TIME_PUMP_SIGNAL_COL_NAMES.index("commodity")]])
    except:
        continue
data_time = [i for i in time_pump_cap if i is not None]


non_duplicate_data_time = list(OrderedDict.fromkeys(data_time))
non_duplicate_log_data_time = np.log10(non_duplicate_data_time)


kde = gaussian_kde(log_data)
x_eval = np.logspace(
    np.log10(np.min(selected_data)), np.log10(np.max(selected_data)), len(selected_data)
)
kde_vals = kde(np.log10(x_eval))

kde_time = gaussian_kde(non_duplicate_log_data_time)
kde_vals_time = kde_time(np.log10(x_eval))

kde_crowd = gaussian_kde(non_duplicate_log_data_crowd)
kde_vals_crowd = kde_crowd(np.log10(x_eval))





# Create the plot
fig, ax = plt.subplots()
ax.fill_between(x_eval, kde_vals, alpha=0.5)
ax.plot(x_eval, kde_vals, label="Market Cap Available Coin")

ax.fill_between(x_eval, kde_vals_time, alpha=0.5)
ax.plot(x_eval, kde_vals_time, label="Time Pump Target Coin")

ax.fill_between(x_eval, kde_vals_crowd, alpha=0.5)
ax.plot(x_eval, kde_vals_crowd, label="Crowd Pump Target Coin")

ax.legend()

# Set x-axis to logarithmic scale
ax.set_xscale("log")

# Define the tick formatter function
def format_ticks(value, pos):
    if value >= 1e12:
        return '{:.0f}T'.format(value/1e12)
    elif value >= 1e9:
        return '{:.0f}B'.format(value/1e9)
    elif value >= 1e6:
        return '{:.0f}M'.format(value/1e6)
    elif value >= 1e3:
        return '{:.0f}K'.format(value/1e3)
    else:
        return int(value)

# Set the tick formatter
ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_ticks))

# Set axis labels and save the plot
ax.set_xlabel("Market Capitalization (USD)")
ax.set_ylabel("Density")
plt.savefig(path.join(PROJECT_ROOT, "exhibit", "market_cap.pdf"))

# Show the plot
plt.show()







# plt.fill_between(x_eval, kde_vals, alpha=0.5)
# plt.plot(x_eval, kde_vals, label="Market Cap Available Coin")


# plt.fill_between(x_eval, kde_vals_time, alpha=0.5)
# plt.plot(x_eval, kde_vals_time, label="Time Pump Target Coin")


# plt.fill_between(x_eval, kde_vals_crowd, alpha=0.5)
# plt.plot(x_eval, kde_vals_crowd, label="Crowd Pump Target Coin")

# plt.legend()


# # Set the tick formatter
# plt.xticks(ticker.FuncFormatter(format_ticks))


# plt.xscale("log")
# plt.xlabel("Unlogged Scale")
# plt.ylabel("Density")
# plt.savefig(path.join(PROJECT_ROOT, "exhibit", "market_cap.pdf"))

# plt.show()
