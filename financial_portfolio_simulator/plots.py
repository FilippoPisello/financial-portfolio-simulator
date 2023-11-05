import seaborn as sns
from matplotlib import pyplot as plt

from financial_portfolio_simulator import OUTPUT_DIR
from financial_portfolio_simulator.returns import Returns


def make_plot_roi_distribution(returns: list[Returns]) -> None:
    fig, ax = plt.subplots()
    closing_rois = [result.closing_roi for result in returns]
    sns.histplot(
        closing_rois,
        ax=ax,
        alpha=0.6,
        stat="probability",
        edgecolor="none",
        bins=60,
    )
    ax.set_title("ROI distribution")
    ax.set_xlabel("ROI")
    ax.set_ylabel("Probability density")
    # X ticks every 1
    ax.set_xticks(range(0, int(max(closing_rois)) + 1, 1))
    # Y ticks every 0.05
    ax.set_yticks([0, 0.05, 0.1])
    fig.savefig(OUTPUT_DIR / "roi_distribution.png")
