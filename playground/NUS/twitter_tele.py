from os import path
import re
import pandas as pd
from environ.settings import PROJECT_ROOT


# Read the data from twitter_data
twitter_pump_and_dump_group_pump = pd.read_csv(
    path.join(
        PROJECT_ROOT,
        "data_twitter/https___twitter.com_search_q=crypto pump_src=typed_query_f=user.csv",
    )
)

twitter_pump_and_dump_group_signal = pd.read_csv(
    path.join(
        PROJECT_ROOT,
        "data_twitter/https___twitter.com_search_q=crypto signal_src=typed_query_f=user.csv",
    )
)


def extract_links(df):
    # Extract the links using regular expressions
    df["links1"] = df["css4rbku5_链接"].apply(
        lambda x: re.findall(r"(http(s)?://(t\.co|t\.me)/\w+)", str(x))
    )
    df["links2"] = df["css4rbku5"].apply(
        lambda x: re.findall(r"(http(s)?://(t\.co|t\.me)/\w+)", str(x))
    )

    # Extract the telegram link and t.co link separately
    df["telegram_link1"] = df["links1"].apply(
        lambda x: [link[0] for link in x if "t.me" in link[0]][0]
        if any("t.me" in link[0] for link in x)
        else ""
    )
    df["tco_link1"] = df["links1"].apply(
        lambda x: [link[0] for link in x if "t.co" in link[0]][0]
        if any("t.co" in link[0] for link in x)
        else ""
    )

    df["telegram_link2"] = df["links2"].apply(
        lambda x: [link[0] for link in x if "t.me" in link[0]][0]
        if any("t.me" in link[0] for link in x)
        else ""
    )
    df["tco_link2"] = df["links2"].apply(
        lambda x: [link[0] for link in x if "t.co" in link[0]][0]
        if any("t.co" in link[0] for link in x)
        else ""
    )

    # Filter rows with empty tco_links
    df = df[df["tco_link1"] != ""]

    new_df = df[["标题链接", "tco_link1"]]
    new_df.columns = ["twitter_link", "telegram_link"]

    # reindex the new_df dataframe
    new_df = new_df.reset_index(drop=True)

    # Return the dataframe with extracted links and filtered rows
    return new_df


# Extract links and filter rows with empty tco_links
pump_key_twitter_and_group_pump = extract_links(twitter_pump_and_dump_group_pump)
pump_key_twitter_and_group_signal = extract_links(twitter_pump_and_dump_group_signal)

# Concatenate pump_key_twitter_and_group_pump and pump_key_twitter_and_group_signal
pump_key_twitter_and_group = pd.concat(
    [pump_key_twitter_and_group_pump, pump_key_twitter_and_group_signal],
    ignore_index=True,
)
