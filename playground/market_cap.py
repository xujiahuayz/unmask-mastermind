from collections import OrderedDict
from os import path
import pickle
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde


from environ.settings import PROJECT_ROOT
from environ.extraction.crowd_pumps_detection import (
    CROWD_PUMP_SIGNALS_QUERY,
    CROWD_SIGNALS_COL_NAMES,
)
from environ.extraction.time_pumps_detection import (
    SIGNALS_TIME_PUMP_QUERY,
    TIME_PUMP_SIGNAL_COL_NAMES,
)
from environ.extraction.cloudburst_tables_connection import CloudburstDataBaseConnection


with open(path.join(PROJECT_ROOT, "data", "coin_cap.pkl"), "rb") as f:
    coin_cap = pickle.load(f)

crowd_pump_signals = CloudburstDataBaseConnection.fetch_data(CROWD_PUMP_SIGNALS_QUERY)
time_pump_signals = CloudburstDataBaseConnection.fetch_data(SIGNALS_TIME_PUMP_QUERY)


data = [i for i in list(coin_cap.values()) if i is not None]
log_data = [i for i in np.log(data) if i > 1]


selected_data = [data[i] for i in range(len(log_data)) if log_data[i] > 1]
data_density = [
    len([j for j in selected_data if 10**i < j < 10 ** (i + 1)]) for i in range(13)
]
# count the number of coins with market cap interval [10^i, 10^(i+1)]
# for i in range(13):
#     print(i, len([j for j in selected_data if 10**i < j < 10 ** (i + 1)]))


crowd_pump_cap = []
for i in crowd_pump_signals:
    try:
        crowd_pump_cap.append(coin_cap[i[CROWD_SIGNALS_COL_NAMES.index("commodity")]])
    except:
        continue
data_crowd = [i for i in crowd_pump_cap if i is not None]
crowd_log_data = np.log(data_crowd)


# for i in range(13):
#     print(
#         i, len([j for j in data_crowd if 10**i < j < 10**(i+1)])
#         )

crowd_density = [
    len([j for j in data_crowd if 10**i < j < 10 ** (i + 1)]) for i in range(13)
]


non_duplicate_data_crowd = list(OrderedDict.fromkeys(data_crowd))

time_pump_cap = []
for i in time_pump_signals:
    try:
        time_pump_cap.append(coin_cap[i[TIME_PUMP_SIGNAL_COL_NAMES.index("commodity")]])
    except:
        continue
data_time = [i for i in time_pump_cap if i is not None]
time_log_data = np.log(data_time)

time_density = [
    len([j for j in data_time if 10**i < j < 10 ** (i + 1)]) for i in range(13)
]


non_duplicate_data_time = list(OrderedDict.fromkeys(data_time))


# Draw the probability desity graph

kde_cloudburst = gaussian_kde(
    data_density,
    bw_method=0.2,
)
plt.plot(range(len(data_density)), kde_cloudburst, lw=2, color="crimson", label="kde")

# density_cloudburst = gaussian_kde(data_density)
density_time = gaussian_kde(time_density)
density_crowd = gaussian_kde(crowd_density)


def plot_loghist(x, bins, label_name):
    hist, bins = np.histogram(x, bins=bins)
    logbins = np.logspace(np.log10(bins[0]), np.log10(bins[-1]), len(bins))
    plt.hist(x, bins=logbins, label=label_name, alpha=0.3, density=True)
    plt.xscale("log")


def plot_hist(x, bins, label_name):
    hist, bins = np.histogram(x, bins=bins)
    plt.hist(x, label=label_name, alpha=0.3, density=True)
    plt.xscale("log")


# plot the probability density graph
plt.plot(range(13), density_cloudburst, label="Cloudburst Available Coin")
plt.plot(density_crowd, label="Crowd Pump Target Coin")
plt.plot(density_time, label="Time Pump Target Coin")

# plot_loghist(selected_data, 50, "Cloudburst Available Coin")
# plot_loghist(non_duplicate_data_crowd, 50, "Crowd Pump Target Coin")
# plot_loghist(non_duplicate_data_time, 50, "Time Pump Target Coin")

# plot_hist(log_data, 1000, "Cloudburst Available Coin")
# plot_hist(crowd_log_data, 1000, "Crowd Pump Target Coin")
# plot_hist(time_log_data, 1000, "Time Pump Target Coin")


# plt.xlabel("Market Capitalization (USD)")
# plt.ylabel("Frequency")
# plt.title("Market Capitalization Distribution of Cryptocurrencies")
# plt.legend()

# plt.savefig(
#     path.join(PROJECT_ROOT, "exhibit", "market_capitalization_distribution.pdf"),
#     format="pdf",
# )

# plt.show()

# Draw the probability desity graph
