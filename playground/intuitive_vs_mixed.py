
    colors = {}
    for i, entity_id in enumerate(time_ranked_bay_vs_re["entity_id"]):
        colors[entity_id] = "#{:06x}".format(hash(str(entity_id)) % 2**24)

    fig, ax = plt.subplots(2, 1, figsize=(16, 16))
    for i, entity_id in enumerate(time_ranked_in_vs_re["entity_id"]):
        entity_df = time_ranked_in_vs_re[time_ranked_in_vs_re["entity_id"] == entity_id]
        ax[0].scatter(
            entity_df["rep_score"],
            entity_df["regression_rep_score"],
            c=colors[entity_id],
            s=500,
            label=str(entity_id),
        )

    # Add labels to the x and y axes
    ax[0].set_xlabel("Intuitive scores", fontsize=27)
    ax[0].set_ylabel("Mix effect scores", fontsize=27)
    ax[0].set_title(
        "Time pump intuitive and mixed effect scores comparison", fontsize=27
    )

    font = matplotlib.font_manager.FontProperties(size=27)
    ax[0].xaxis.set_ticklabels(ax[0].xaxis.get_ticklabels(), fontproperties=font)
    ax[0].yaxis.set_ticklabels(ax[0].yaxis.get_ticklabels(), fontproperties=font)

    colors = {}
    for i, entity_id in enumerate(crowd_ranked_in_vs_re["entity_id"]):
        colors[entity_id] = "#{:06x}".format(hash(str(entity_id)) % 2**24)

    for i, entity_id in enumerate(crowd_ranked_in_vs_re["entity_id"]):
        entity_df = crowd_ranked_in_vs_re[
            crowd_ranked_in_vs_re["entity_id"] == entity_id
        ]
        ax[1].scatter(
            entity_df["rep_score"],
            entity_df["regression_rep_score"],
            c=colors[entity_id],
            s=500,
            label=str(entity_id),
        )

    # Add labels to the x and y axes
    ax[1].set_xlabel("Intuitive scores", fontsize=27)
    ax[1].set_ylabel("Mix effect scores", fontsize=27)
    ax[1].set_title(
        "Crowd pump intuitive and mixed effect scores comparison", fontsize=27
    )

    font = matplotlib.font_manager.FontProperties(size=27)
    ax[1].xaxis.set_ticklabels(ax[1].xaxis.get_ticklabels(), fontproperties=font)
    ax[1].yaxis.set_ticklabels(ax[1].yaxis.get_ticklabels(), fontproperties=font)

    fig.subplots_adjust(hspace=0.4)

    plt.show()
    fig.savefig("score_comparison.pdf", format="pdf")


