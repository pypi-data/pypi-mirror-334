from __future__ import annotations

import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import gridspec
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scanpy import read_h5ad
from scipy.stats import entropy, gaussian_kde


def jensen_shannon_divergence(p, q):
    p = np.asarray(p)
    q = np.asarray(q)
    p = p / np.sum(p)
    q = q / np.sum(q)
    m = (p + q) / 2

    # JS divergence
    # JS = 0.5 * (KL(P||M) + KL(Q||M))
    divergence = 0.5 * (entropy(p, m) + entropy(q, m))

    return divergence


def prepare_data(
    full_adata_path: str, split_df_path: str, experiment_json_path: str | None = None
):
    full_adata = read_h5ad(full_adata_path)
    split_df = pd.read_csv(split_df_path, index_col=0)
    full_label_dist = full_adata.obs["y"].value_counts(normalize=True)
    label_index = full_adata.obs["y"].cat.categories
    folds = {}

    for fold_idx in split_df["cluster"].unique():
        fold = split_df[split_df["cluster"] == fold_idx]
        fold_accessions = set(fold["AC"].to_list())
        mask = full_adata.obs["accession"].isin(fold_accessions)
        fold_label_dist = (
            full_adata.obs["y"].loc[mask].value_counts(normalize=True).sort_index()
        )
        folds[fold_idx] = {
            "size": mask.sum() / len(full_adata),
            "2d": full_adata.obsm["X_tsne"][mask],
            "label_dist": fold_label_dist,
            "js_div": jensen_shannon_divergence(full_label_dist, fold_label_dist),
        }

    if experiment_json_path is not None:
        with open(experiment_json_path, "r") as f:
            exp_results = json.load(f)
        threshold = exp_results.get("threshold", "N/A")
        metric = exp_results.get("metric", "N/A")
        seed = exp_results.get("seed", "N/A")

        under_threshold = [
            round(exp_results[str(idx)].get("under_threshold", "N/A"), 3)
            if exp_results[str(idx)].get("under_threshold", "N/A") != "N/A"
            else "N/A"
            for idx in folds
        ]

        best_validation_score = [
            round(exp_results[str(idx)].get("best_validation_score", "N/A"), 3)
            if exp_results[str(idx)].get("best_validation_score", "N/A") != "N/A"
            else "N/A"
            for idx in folds
        ]

        test_score = [
            round(exp_results[str(idx)].get("test_score", "N/A"), 3)
            if exp_results[str(idx)].get("test_score", "N/A") != "N/A"
            else "N/A"
            for idx in folds
        ]
    else:
        threshold = "N/A"
        metric = "N/A"
        seed = "N/A"
        under_threshold = ["N/A"] * len(folds)
        best_validation_score = ["N/A"] * len(folds)
        test_score = ["N/A"] * len(folds)

    sizes = [round(folds[idx]["size"], 3) for idx in folds]
    js_div = [round(folds[idx]["js_div"], 3) for idx in folds]
    table_list = [
        [
            "Fold",
            "Size",
            "% < thresh\n(↑)",
            "JS div\n(↓)",
            "Valid\nScore",
            "Test\nScore",
        ],
        *zip(
            range(len(folds)),
            sizes,
            under_threshold,
            js_div,
            best_validation_score,
            test_score,
        ),
    ]
    return folds, full_label_dist, table_list, label_index, threshold, metric, seed


def create_tsne_plot(ax, folds, dataset_name, alpha, split_method):
    """Create t-SNE visualization plot."""
    for key in folds.keys():
        ax.scatter(
            folds[key]["2d"][:, 0],
            folds[key]["2d"][:, 1],
            label=f"Fold {key}",
            alpha=alpha,
        )
    ax.legend()
    ax.set_title(
        f"t-SNE visualizations of folds\nSplit by {split_method}, "
        + f"Dataset: {dataset_name}"
    )
    ax.axis("off")


def create_metrics_table(
    ax, table_list, threshold, metric, seed, table_col_widths, font_size, scale
):
    """Create metrics table."""
    table = ax.table(cellText=table_list, loc="center", colWidths=table_col_widths)
    table.auto_set_font_size(False)
    table.set_fontsize(font_size)
    table.scale(*scale)

    # Center align all cell text
    for cell in table._cells.values():
        cell.set_text_props(ha="center", va="center")

    ax.set_title(
        f"Size, similarity and label divergence metric\n\n"
        f"Threshold = {threshold}, Score = {metric}, Seed = {seed}"
    )
    ax.axis("off")

    return table


def create_distribution_plot(ax, full_label_dist, folds, label_index, bar_width, alpha):
    """Create distribution bar plot."""
    x = np.arange(len(full_label_dist))
    max_text_pos = float("-inf")

    # Plot full dataset distribution
    ax.bar(x, full_label_dist.values, bar_width, alpha=alpha, label="Full Dataset")
    for i, v in enumerate(full_label_dist.values):
        ax.text(
            x[i],
            v + 0.01,
            f"{v:.2%}",
            ha="center",
            va="bottom",
            fontsize=8,
            rotation=90,
        )
        max_text_pos = max(max_text_pos, v + 0.01)

    # Plot fold distributions
    for fold_idx in folds.keys():
        dist = folds[fold_idx]["label_dist"].values
        ax.bar(
            x + bar_width * (fold_idx + 1), dist, bar_width, label=f"Fold {fold_idx}"
        )
        # Adjust font size based on bar width
        for i, v in enumerate(dist):
            for i, v in enumerate(dist):
                color = "black" if v > 0 else "red"
                text_y = v + 0.01
                ax.text(
                    x[i] + bar_width * (fold_idx + 1),
                    v + 0.01,
                    f"{v:.2%}",
                    ha="center",
                    va="bottom",
                    fontsize=8,
                    rotation=90,
                    color=color,
                )
                max_text_pos = max(max_text_pos, text_y)

    # Set y-axis limits
    ax.set_ylim(0, max_text_pos + 0.3)

    # Set x-axis ticks and labels
    n_folds = len(folds.keys())
    tick_positions = x + bar_width * (n_folds / 2)
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(label_index, rotation=45)

    # Set labels and title
    ax.set_title("Distribution of folds")
    ax.set_xlabel("Class")
    ax.set_ylabel("Frequency")
    ax.legend(fontsize="x-small")


def visualize_fold_analysis(
    full_adata_path: str,
    split_df_path: str,
    dataset_name: str,
    split_method: str = "SAEA",
    experiment_json_path: str | None = None,
    figsize: tuple[int, int] = (14, 6),
    width_ratios: tuple[float] = (0.5, 0.5),
    scatter_alpha: float = 0.5,
    table_col_widths: tuple[float] = (0.15, 0.25, 0.3, 0.3, 0.3, 0.3),
    table_font_size: int = 12,
    table_scale: tuple[float] = (0.65, 6),
    bar_alpha: float = 0.7,
    bar_width: float = 0.25,
    dpi: int = 300,
    save_path: str | None = None,
):
    """
    Main function to create the complete visualization.

    Parameters:
    - full_adata_path (str): Path to the full AnnData object file.
    - split_df_path (str): Path to the CSV file containing split information.
    - dataset_name (str): Name of the dataset.
    - split_method (str, optional):
    Method used for splitting the dataset. Default is "SAEA".
    - experiment_json_path (str, optional):
    Path to the JSON file containing experiment results. Default is None.
    - figsize (tuple[int, int], optional):
    Size of the figure. Default is (14, 6).
    - width_ratios (tuple[float], optional):
    Width ratios for the grid layout. Default is (0.5, 0.5).
    - scatter_alpha (float, optional):
    Alpha value for scatter plot transparency. Default is 0.5.
    - table_col_widths (tuple[float], optional):
    Column widths for the metrics table. Default is (0.15, 0.25, 0.3, 0.3, 0.3, 0.3).
    - table_font_size (int, optional):
    Font size for the metrics table. Default is 12.
    - table_scale (tuple[float], optional):
    Scale for the metrics table. Default is (0.65, 6).
    - bar_alpha (float, optional):
    Alpha value for bar plot transparency. Default is 0.7.
    - bar_width (float, optional):
    Width of the bars in the distribution plot. Default is 0.25.
    - dpi (int, optional): Dots per inch for the figure. Default is 300.
    - save_path (str, optional): Path to save the figure. Default is None.

    Returns:
    - fig (Figure): The created matplotlib figure.
    """
    (
        folds,
        full_label_dist,
        table_list,
        label_index,
        threshold,
        metric,
        seed,
    ) = prepare_data(full_adata_path, split_df_path, experiment_json_path)

    # Create figure and grid
    plt.rcParams["figure.dpi"] = dpi
    fig = plt.figure(figsize=figsize)
    gs = gridspec.GridSpec(1, 2, width_ratios=width_ratios)
    gs.update(wspace=0.1, hspace=0.1)

    # Create left plot (t-SNE)
    ax_left = plt.subplot(gs[0])
    create_tsne_plot(ax_left, folds, dataset_name, scatter_alpha, split_method)

    # Create right plots (table and distribution)
    ax_right = plt.subplot(gs[1])
    create_metrics_table(
        ax_right,
        table_list,
        threshold,
        metric,
        seed,
        table_col_widths,
        table_font_size,
        table_scale,
    )

    # Create bottom right plot (distribution)
    divider = make_axes_locatable(ax_right)
    ax_bottom_right = divider.append_axes(
        "bottom", size="100%", pad=0.1, sharex=ax_right
    )
    create_distribution_plot(
        ax_bottom_right, full_label_dist, folds, label_index, bar_width, bar_alpha
    )

    if save_path is not None:
        plt.savefig(save_path, bbox_inches="tight", dpi=dpi)
    return fig


def plot_split_identities(
    split_df_paths: list[str],
    split_methods: list[str],
    test_cluster_idx: int = 1,
    threshold: float = 0.8,
    figsize: tuple[int, int] = (8, 6),
    dpi: int = 300,
    fontsize: int = 10,
):
    """
    Plot the identity distributions for different split methods.

    Parameters:
    - split_df_paths (list[str]):
    List of paths to the CSV files containing split information.
    - split_methods (list[str]): List of names of the split methods.
    - test_cluster_idx (int, optional): Index of the test cluster. Default is 1.
    - threshold (float, optional): Threshold for identity. Default is 0.8.
    - figsize (tuple[int, int], optional): Size of the figure. Default is (8, 6).
    - dpi (int, optional): Dots per inch for the figure. Default is 300.
    - fontsize (int, optional): Font size for the legend. Default is 10.

    Returns:
    - fig (Figure): The created matplotlib figure.
    - ax (Axes): The axes of the plot.
    """
    identities = {}
    for name, path in zip(split_methods, split_df_paths):
        df = pd.read_csv(path, index_col=0)
        max_identities = df.loc[
            df["cluster"] == test_cluster_idx, "max_ident_other"
        ].values
        identities[name] = max_identities

    plt.rcParams["figure.dpi"] = dpi
    fig, ax = plt.subplots(figsize=figsize)
    max_height = 0
    for name, identity in identities.items():
        _, bins, _ = ax.hist(identity, bins=30, alpha=0)
        kde = gaussian_kde(identity)
        x_range = np.linspace(min(identity), max(identity), 200)
        kde_values = kde(x_range) * len(identity) * (bins[1] - bins[0])
        max_height = max(max_height, max(kde_values))
        percentage = (identity < threshold).mean() * 100
        ax.plot(
            x_range,
            kde_values,
            linewidth=2,
            label=f"{name} ({percentage:.2f}% under {threshold * 100}% identity)",
        )

    ax.axvline(threshold, color="black", linestyle="--", label="Threshold")
    ax.legend(fontsize=fontsize)
    ax.set_title("Identity distribution")
    ax.set_xlabel("Identity")
    ax.set_ylabel("Frequency")
    return fig, ax


def plot_label_distribution(
    adata_path: str,
    split_df_paths: list[str],
    split_methods: list[str],
    dataset_name: str,
    figsize: tuple[int, int] = (12, 6),
    dpi: int = 300,
):
    """
    Plot the label distribution for the full dataset and different splits.

    Args:
        adata_path (str): Path to the AnnData object file.
        split_df_paths (list[str]):
        List of paths to the CSV files containing split information.
        split_methods (list[str]): List of names of the split methods.
        dataset_name (str): Name of the dataset.

    Returns:
        tuple: A tuple containing the created matplotlib figure and axes.
    """
    adata = read_h5ad(adata_path)
    assert "y" in adata.obs.columns, "No labels found in AnnData object"
    labels = adata.obs["y"]
    full_distribution = labels.value_counts(normalize=True)
    test_partition_idx = 1
    distributions = {"full": full_distribution}

    for name, split_path in zip(split_methods, split_df_paths):
        split = pd.read_csv(split_path)
        test_accs = set(split["AC"][split["cluster"] == test_partition_idx].to_list())
        mask = adata.obs["accession"].isin(test_accs)
        test_labels = labels[mask]
        dist = test_labels.value_counts(normalize=True)
        div = jensen_shannon_divergence(full_distribution, dist)
        key = f"{name} ({div:.3f})"
        distributions[key] = dist

    plt.rcParams["figure.dpi"] = dpi
    df = pd.DataFrame(distributions)
    fig = plt.figure(figsize=figsize)
    ax = df.plot(kind="bar", ax=fig.gca())
    plt.title(f"Comparison of label distributions for splits on {dataset_name} dataset")
    plt.xlabel("Category")
    plt.ylabel("Proportion")
    plt.legend(title="Source")
    plt.xticks(rotation=45, ha="center")
    plt.tight_layout()

    return fig, ax
