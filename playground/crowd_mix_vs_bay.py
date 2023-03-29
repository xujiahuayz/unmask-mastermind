from os import path
from environ.settings import PROJECT_ROOT
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

mixed_score_crowd = pd.read_csv(path.join(PROJECT_ROOT, "data", "regression_score_crowd.csv"))

bay_score_crowd = pd.read_csv(
    path.join(PROJECT_ROOT, "data", "bayesian_regression_score_crowd.csv")
)


crowd_bay_vs_re = pd.merge(mixed_score_crowd, bay_score_crowd, on="entity_id")
crowd_ranked_bay_vs_re = crowd_bay_vs_re.sort_values(by="bayesian_scores")


# Plot thje time ranked bayesian vs regression scores
colors = {}
colors[-1001652601224] = "#da7194"
colors[-1001495281876] = "#7febff"
colors[-1001498984863] = "#ff8987"
colors[-1001545919293] = "#fdebd1"
colors[-1001674306258] = "#57c7e3"
colors[-1001619333749] = "#ffb987"
colors[-1001369513842] = "#ffffa3"
colors[-1001583172969] = "#8dcc93"
colors[-1001628956682] = "#4c8eda"
colors[-1001164308989] = "#f16667"
colors[-1001395566862] = "#ffe081"
colors[-1001555625124] = "#ecb5c9"
colors[-1001656921849] = "#d9c8ae"
colors[-1001313911314] = "#f79767"
colors[-1001509948336] = "#edb2e3"
colors[-1001436907930] = "#ffc454"
colors[-1001695857773] = "#aff0b5"
colors[-1001291335731] = "#c990c0"

fig, ax = plt.subplots()
for i, entity_id in enumerate(crowd_ranked_bay_vs_re["entity_id"]):
    entity_df = crowd_ranked_bay_vs_re[crowd_ranked_bay_vs_re["entity_id"] == entity_id]
    ax.scatter(
        entity_df["bayesian_scores"],
        entity_df["regression_rep_score"],
        c=colors[entity_id],
        s=500,
        label=str(entity_id),
    )

laber = ["A", "B", "C", "D", "E", "F", "G"]
# Add labels to the first 7 rows
for (j, (i, row)) in zip(
    range(len(crowd_ranked_bay_vs_re[12:-1])),
    enumerate(crowd_ranked_bay_vs_re[12:-1].iterrows()),
):
    ax.annotate(
        str(laber[j]),
        (row[1]["bayesian_scores"], row[1]["regression_rep_score"]),
        xytext=(-20 - 5 * j * 2, -20 - 5 * j * 10),
        textcoords="offset points",
        arrowprops=dict(arrowstyle="->"),
    )

# Add labels to the x and y axes
ax.set_xlabel("Bayesian scores")
ax.set_ylabel("Mixed effect score")
ax.set_title("Crowd pump Bayesian vs mixed effect scores comparison")

# Create a side bar to store the entity_id labels
# box = ax.get_position()
# ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
# ax.legend(loc="center left", bbox_to_anchor=(1, 0.5), title="entity_id")
fig.savefig(
    path.join(PROJECT_ROOT, "assets", "Bayesian_vs_maix_score_comparison_crowd.pdf"),
    format="pdf",
)

# Show the plot
plt.show()
