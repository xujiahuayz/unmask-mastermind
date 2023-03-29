from os import path
from environ.settings import PROJECT_ROOT
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

mixed_score_time = pd.read_csv(
        path.join(PROJECT_ROOT, "data", "regression_score_time.csv")
    )


bay_score_time = pd.read_csv(
        path.join(PROJECT_ROOT, "data", "bayesian_regression_score_time.csv")
    )



time_bay_vs_re = pd.merge(mixed_score_time, bay_score_time, on="entity_id")
time_ranked_bay_vs_re = time_bay_vs_re.sort_values(by="bayesian_scores")




# Plot thje time ranked bayesian vs regression scores
colors = {}
colors[-1001546300553] = "#d9c8ae"
colors[-1001625691880] = "#ecb5c9"
colors[-1001342400398] = "#57c7e3"
colors[-1001751272520] = "#4c8eda"
colors[-1001147810456] = "#ffb987"
colors[-1001700314832] = "#d9c8ae"
colors[-1001630627066] = "#ffe081"
colors[-1001237041098] = "#ffc454"
colors[-1001715951472] = "#f16667"
colors[-1001647563514] = "#8dcc93"
colors[-1001593186486] = "#da7194"
colors[-1001644378771] = "#f79767"
colors[-1001258049399] = "#7febff"
colors[-1001219293084] = "#c990c0"
colors[-1001690548530] = "#edb2e3"

fig, ax = plt.subplots()
for i, entity_id in enumerate(time_ranked_bay_vs_re["entity_id"]):
        entity_df = time_ranked_bay_vs_re[
            time_ranked_bay_vs_re["entity_id"] == entity_id
        ]
        ax.scatter(
            entity_df["bayesian_scores"],
            entity_df["regression_rep_score"],
            c=colors[entity_id],
            s=500,
            label=str(entity_id),
        )

laber = ["A", "B", "C"]
for (j, (i, row)) in zip(
        range(len(time_ranked_bay_vs_re[:3])),
        enumerate(time_ranked_bay_vs_re[:3].iterrows()),
    ):
        ax.annotate(
            str(laber[j]),
            (row[1]["bayesian_scores"], row[1]["regression_rep_score"]),
            xytext=(40 + 5 * j * 6, 20 + 5 * j * 10),
            textcoords="offset points",
            arrowprops=dict(arrowstyle="->"),
        )

# Add labels to the x and y axes
ax.set_xlabel("Bayesian scores")
ax.set_ylabel("Mixed effect score")
ax.set_title("Time pump Bayesian vs mixed effect scores comparison")

# Create a side bar to store the entity_id labels
# box = ax.get_position()
# ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
# ax.legend(loc="center left", bbox_to_anchor=(1, 0.5), title="entity_id")
fig.savefig(path.join(PROJECT_ROOT, "assets","Bayesian_vs_maix_score_comparison_time.pdf"), format="pdf")

# Show the plot
plt.show()




