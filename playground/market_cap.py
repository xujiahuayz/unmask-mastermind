from collections import OrderedDict
from os import path
import pickle
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KernelDensity
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
from environ.extraction.cloudburst_connection import cloudburst_connection

with open(path.join(PROJECT_ROOT, "data", "coin_cap.pkl"), "rb") as f:
    coin_cap = pickle.load(f)

crowd_pump_signals = cloudburst_connection(CROWD_PUMP_SIGNALS_QUERY)
time_pump_signals = cloudburst_connection(SIGNALS_TIME_PUMP_QUERY)


data = [i for i in list(coin_cap.values()) if i is not None]


log_data = [i for i in np.log10(data) if i > 3]
selected_data = [i for i in data if np.log10(i) > 3]


# selected_data = [data[i] for i in range(len(log_data)) if log_data[i] > 1]
# data_density = [
#     len([j for j in selected_data if 10**i < j < 10 ** (i + 1)]) for i in range(13)
# ]
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
non_duplicate_log_data_crowd = np.log(non_duplicate_data_crowd)


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


# # generate some data
# data = np.random.normal(size=100)
# # log_data = np.log(data)

# # fit the KDE to the log-transformed data
# kde = gaussian_kde(log_data)

# # plot the KDE
# x_eval = np.linspace(np.min(log_data), np.max(log_data), num=1000)
# kde_vals = kde(x_eval)

# plt.plot(np.exp(x_eval), kde_vals)
# plt.xscale('log')
# plt.xlabel('True Scale')
# plt.ylabel('Density')
# plt.show()

# generate some data
# data = np.random.normal(size=100)
# log_data = np.log(data)

# fit the KDE to the log-transformed data


# kde1 = gaussian_kde(crowd_log_data)
# x_eval = np.logspace(np.log10(np.min()))


# def plot_kde(data):
#     log_data = np.log(data)
#     kde = gaussian_kde(log_data)
#     x_eval = np.logspace(np.log10(np.min(data)), np.log10(np.max(data)), len(data))
#     kde_vals = kde(np.log10(x_eval))

#     plt.fill_between(x_eval, kde_vals, alpha=0.5)
#     plt.plot(x_eval, kde_vals)
#     plt.xscale("log")
#     plt.xlabel("Unlogged Scale")
#     plt.ylabel("Density")
# plt.show()


# plot_kde(selected_data)
# plot_kde(data_crowd)
# plot_kde(data_time)


# # generate some random market cap data
# # np.random.seed(0)
# # market_cap = np.random.normal(100, 10, 100)

# # log transform the market cap data
# log_market_cap = np.log(selected_data)

# # fit a kernel density estimate on the log transformed data
# kde = KernelDensity(kernel='gaussian', bandwidth=0.5).fit(log_market_cap[:, np.newaxis])

# # evaluate the kernel density estimate on a grid of points
# x_grid = np.linspace(np.log10(1e2), np.log10(1e13), 1000)
# log_dens = kde.score_samples(x_grid[:, np.newaxis])

# # plot the log transformed data and the estimated density on the log scale
# plt.hist(log_market_cap, bins=200, density=True, alpha=0.5)
# plt.plot(x_grid, np.exp(log_dens), '-', color='red')
# plt.xlim(np.log10(1e2), np.log10(1e13))
# plt.xscale('log')

# # create a second axis with the real scale
# ax2 = plt.gca().twiny()
# ax2.xaxis.set_ticks_position("bottom")
# ax2.xaxis.set_label_position("bottom")
# ax2.spines["bottom"].set_position(("axes", -0.1))
# ax2.set_xlim(1e2, 1e13)
# ax2.set_xscale('log')
# ax2.set_xlabel("Market Cap (Real Scale)")

# plt.show()


# Draw the probability desity graph

# kde_cloudburst = gaussian_kde(
#     data_density,
#     bw_method=0.2,
# )
# plt.bar(1, kde_cloudburst, lw=2)

# # density_cloudburst = gaussian_kde(data_density)
# density_time = gaussian_kde(time_density)
# density_crowd = gaussian_kde(crowd_density)


# def plot_loghist(x, bins, label_name):
#     hist, bins = np.histogram(x, bins=bins)
#     logbins = np.logspace(np.log10(bins[0]), np.log10(bins[-1]), len(bins))
#     plt.hist(x, bins=logbins, label=label_name, alpha=0.3, density=True)
#     plt.xscale("log")


# def plot_hist(x, bins, label_name):
#     hist, bins = np.histogram(x, bins=bins)
#     plt.hist(x, label=label_name, alpha=0.3, density=True)
#     plt.xscale("log")


# plot the probability density graph
# plt.plot(range(13), density_cloudburst, label="Cloudburst Available Coin")
# plt.plot(density_crowd, label="Crowd Pump Target Coin")
# plt.plot(density_time, label="Time Pump Target Coin")

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


kde = gaussian_kde(log_data)
x_eval = np.logspace(
    np.log10(np.min(selected_data)), np.log10(np.max(selected_data)), len(selected_data)
)
kde_vals = kde(np.log10(x_eval))
plt.fill_between(x_eval, kde_vals, alpha=0.5)
plt.plot(x_eval, kde_vals)
plt.xscale("log")
plt.xlabel("Unlogged Scale")
plt.ylabel("Density")
plt.show()


kde1 = gaussian_kde(non_duplicate_log_data_crowd)
x_eval1 = np.logspace(
    np.log10(np.min(non_duplicate_data_crowd)),
    np.log10(np.max(non_duplicate_data_crowd)),
    len(non_duplicate_data_crowd),
)


x_eval1 = np.logspace(
    np.log10(
        np.min(non_duplicate_data_crowd), np.log10(np.max(non_duplicate_data_crowd))
    )
)
