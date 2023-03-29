from os import path
import pandas as pd
from environ.settings import PROJECT_ROOT


# Read the data from twitter_data
opensea_twitter_handler_wallet = pd.read_csv(
    path.join(PROJECT_ROOT, "data_twitter/opensea_twitter_handler_wallet.csv")
)

twitter_hexagon_cleaned_wallet = pd.read_csv(
    path.join(PROJECT_ROOT, "data_twitter/twitter_hexagon_cleaned_wallet.csv")
)
