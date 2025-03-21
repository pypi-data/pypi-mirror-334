from __future__ import annotations

import warnings
from collections import defaultdict
from typing import Literal

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from scanpy import AnnData
from sklearn.cluster import DBSCAN, KMeans
from sklearn.metrics import pairwise_distances
from tqdm import tqdm


def process_dbscan(labels):
    adjusted_labels = []
    max_label = max(labels)
    for i in range(len(labels)):
        if labels[i] == -1:
            adjusted_labels.append(max_label + 1)
            max_label += 1
        else:
            adjusted_labels.append(labels[i])
    return np.array(adjusted_labels)


def perform_clustering(
    cluster_method: Literal["KMeans", "DBSCAN"], adata: AnnData, **cluster_args
):
    """
    Perform clustering on the given AnnData object using the specified
    clustering method.

    Parameters:
    - cluster_method (Literal['KMeans', 'DBSCAN']):
    The clustering method to use. Must be either 'KMeans' or 'DBSCAN'.
    - adata (AnnData): The annotated data matrix.
    - **cluster_args: Additional arguments to pass to the clustering algorithm.

    Returns:
    - np.ndarray: An array of cluster assignments for each data point.
    """
    if cluster_args is None:
        cluster_args = {}
    if cluster_method == "KMeans":
        assert (
            "n_clusters" in cluster_args
        ), "Must specify k_cluster in the cluster_args for KMeans"
        kmeans = KMeans(**cluster_args).fit(adata.X)
        cluster_assignments = kmeans.labels_
    else:
        dbscan = DBSCAN(**cluster_args).fit(adata.X)
        cluster_assignments = process_dbscan(dbscan.labels_)
    return cluster_assignments


def plot_clusters(
    cluster_assignments: np.ndarray,
    two_d_embedding: np.ndarray,
    singleton_size: float = 5,
    normal_size: float = 8,
    highlight_singletons: bool = False,
    text: Literal["cluster_idx", "dist", "no_text"] = "cluster_idx",
    fontsize: int = 10,
    dists: np.ndarray | None = None,
    title: str | None = None,
    figsize: tuple[int, int] = (8, 6),
    dpi: int = 300,
):
    """
    Plot clusters on a 2D embedding.

    Parameters:
    - cluster_assignments (np.ndarray):
    Array of cluster assignments for each data point.
    - two_d_embedding (np.ndarray): 2D embedding of the data points.
    - singleton_size (float): Size of the markers for singletons. Default is 5.
    - normal_size (float): Size of the markers for normal points. Default is 8.
    - highlight_singletons (bool): Whether to highlight singleton clusters.
    Default is False.
    - text (Literal['cluster_idx', 'dist', 'no_text']):
    Type of text to display on the plot. Default is 'cluster_idx'.
    - fontsize (int): Font size for the text. Default is 10.
    - dists (np.ndarray | None): Array of distances for each cluster. Default is None.
    - title (str | None): Title of the plot. Default is None.
    - figsize (tuple[int, int]): Size of the figure. Default is (8, 6).
    - dpi (int): Dots per inch for the figure. Default is 300.

    Returns:
    - fig, ax: The figure and axis of the plot.
    """
    plt.rcParams["figure.dpi"] = dpi
    fig, ax = plt.subplots(figsize=figsize)

    text_singletons = highlight_singletons
    count = np.bincount(cluster_assignments)
    unique_clusters = np.unique(cluster_assignments)

    if dists is not None:
        assert len(dists) == len(
            unique_clusters
        ), "Length of dists must match number of unique clusters"

    for i in unique_clusters:
        x = two_d_embedding[cluster_assignments == i, 0]
        y = two_d_embedding[cluster_assignments == i, 1]
        if count[i] <= 2:  # Singletons
            if not highlight_singletons:
                ax.scatter(
                    x,
                    y,
                    s=singleton_size,
                    facecolors="none",
                    edgecolors="r",
                    label="Singletons",
                )
                highlight_singletons = True
            else:
                ax.scatter(x, y, s=singleton_size, facecolors="none", edgecolors="r")
            if not text_singletons:
                continue
        else:
            ax.scatter(x, y, s=normal_size)

        if text == "cluster_idx":  # Label cluster index
            ax.text(np.mean(x), np.mean(y), str(i), fontsize=fontsize)
        elif text == "dist" and dists is not None:
            ax.text(np.mean(x), np.mean(y), round(dists[i], 2), fontsize=fontsize)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        ax.legend()

    if title is not None:
        ax.set_title(title)
    ax.axis("off")

    return fig, ax


def intra_cluster_distance(
    cluster_assignments: np.ndarray, adata: AnnData
) -> np.ndarray:
    dists = []
    for i in np.unique(cluster_assignments):
        cluster = adata.X[cluster_assignments == i]
        dists.append(pairwise_distances(cluster, metric="euclidean").mean())
    return np.array(dists)


def min_inter_cluster_distances(
    cluster_assignments: np.ndarray, adata: AnnData, skip_singletons: bool = True
):
    dists = []
    for i in tqdm(np.unique(cluster_assignments)):
        cluster_i = adata.X[cluster_assignments == i]
        if len(cluster_i) == 1 and skip_singletons:
            dists.append(0)
            continue
        min_dist_to_other_clusters = float("inf")
        for j in np.unique(cluster_assignments):
            if i != j:
                cluster_j = adata.X[cluster_assignments == j]
                min_dist_to_other_clusters = min(
                    min_dist_to_other_clusters,
                    pairwise_distances(cluster_i, cluster_j, metric="euclidean").mean(),
                )
        dists.append(min_dist_to_other_clusters)
    return np.array(dists)


def plot_clusters_with_distances(
    two_d_embedding: np.ndarray,
    cluster_assignments: np.ndarray,
    dists: np.ndarray,
    title: str | None = None,
    scale: float = 1,
    skip_singletons: bool = True,
    text_threshold: int = 40,
    figsize: tuple[int, int] = (8, 6),
    dpi: int = 300,
):
    plt.rcParams["figure.dpi"] = dpi
    fig, ax = plt.subplots(figsize=figsize)

    cmap = plt.cm.coolwarm
    vmin, vmax = min(dists), max(dists)
    vmid = np.median(dists)
    norm = Normalize(vmin=vmin, vmax=vmax)

    # Plot each cluster
    count = np.bincount(cluster_assignments)
    text = len(count) < text_threshold
    for i in np.unique(cluster_assignments):
        if count[i] <= 2 and skip_singletons:
            continue
        cluster_points = two_d_embedding[cluster_assignments == i]
        cluster_center = np.mean(cluster_points, axis=0)
        color = cmap(norm(dists[i]) * scale)
        ax.scatter(cluster_points[:, 0], cluster_points[:, 1], c=[color], s=20)
        if text:
            ax.text(cluster_center[0], cluster_center[1], f"{i}", fontsize=5)

    ax.axis("off")

    # Add a colorbar
    sm = ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, pad=0.02, aspect=30)
    cbar.set_label(title, fontsize=12)
    cbar.ax.tick_params(labelsize=10)

    # Add colorbar ticks for min, median, and max values
    cbar.set_ticks([vmin, vmid, vmax])
    cbar.set_ticklabels([f"{vmin:.2f}", f"{vmid:.2f}", f"{vmax:.2f}"])

    plt.tight_layout()
    return fig, ax


def plot_intra_cluster_distance(
    adata: AnnData,
    cluster_assignments: np.ndarray,
    title: str | None = None,
    skip_singletons: bool = True,
    scale: float = 1,
    use_2d: Literal["X_umap", "X_tsne", "X_pca"] = "X_tsne",
    text_threshold: int = 40,
    figsize: tuple[int, int] = (8, 6),
    dpi: int = 300,
):
    """
    Plot intra-cluster distances on a 2D embedding.

    Parameters:
    - adata (AnnData): The annotated data object.
    - cluster_assignments (np.ndarray):
    Array of cluster assignments for each data point.
    - title (str | None): Title of the plot. Default is None.
    - skip_singletons (bool): Whether to skip singleton clusters. Default is True.
    - scale (float): Scaling factor for the color intensity. Default is 1.
    - use_2d (Literal['X_umap', 'X_tsne', 'X_pca']):
    The 2D embedding to use. Default is 'X_tsne'.
    - text_threshold (int):
    If # clusters > threshold, no text will be displayed. Default is 40.
    - figsize (tuple[int, int]): Size of the figure. Default is (8, 6).
    - dpi (int): Dots per inch for the figure. Default is 300.

    Returns:
    - fig, ax: The figure and axis of the plot.
    """
    dists = intra_cluster_distance(cluster_assignments, adata)
    return plot_clusters_with_distances(
        adata.obsm[use_2d],
        cluster_assignments,
        dists,
        title=title,
        scale=scale,
        skip_singletons=skip_singletons,
        text_threshold=text_threshold,
        figsize=figsize,
        dpi=dpi,
    )


def plot_min_inter_cluster_distances(
    adata: AnnData,
    cluster_assignments: np.ndarray,
    title: str | None = None,
    skip_singletons: bool = True,
    scale: float = 1,
    use_2d: Literal["X_umap", "X_tsne", "X_pca"] = "X_tsne",
    text_threshold: int = 40,
    figsize: tuple[int, int] = (8, 6),
    dpi: int = 300,
):
    """
    Plot minimum inter-cluster distances on a 2D embedding.

    Parameters:
    - adata (AnnData): The annotated data object.
    - cluster_assignments (np.ndarray):
    Array of cluster assignments for each data point.
    - title (str | None): Title of the plot. Default is None.
    - skip_singletons (bool): Whether to skip singleton clusters. Default is True.
    - scale (float): Scaling factor for the color intensity. Default is 1.
    - use_2d (Literal['X_umap', 'X_tsne', 'X_pca']):
    The 2D embedding to use. Default is 'X_tsne'.
    - text_threshold (int): If # clusters > threshold,
    no text will be displayed. Default is 40.
    - figsize (tuple[int, int]): Size of the figure. Default is (8, 6).
    - dpi (int): Dots per inch for the figure. Default is 300.

    Returns:
    - fig, ax: The figure and axis of the plot.
    """
    dists = min_inter_cluster_distances(
        cluster_assignments, adata, skip_singletons=skip_singletons
    )
    return plot_clusters_with_distances(
        adata.obsm[use_2d],
        cluster_assignments,
        dists,
        title=title,
        scale=scale,
        skip_singletons=skip_singletons,
        text_threshold=text_threshold,
        figsize=figsize,
        dpi=dpi,
    )


def plot_dataset_label_distribution(
    adata: AnnData,
    use_2d: Literal["X_umap", "X_tsne", "X_pca"] = "X_tsne",
    title: str | None = None,
    point_size: float = 8,
    alpha: float = 0.5,
    figsize: tuple[int, int] = (8, 6),
    dpi: int = 300,
    fontsize: int = 10,
):
    """
    Plot the distribution of dataset labels on a 2D embedding.

    Parameters:
    - adata (AnnData): The annotated data object.
    - use_2d (Literal['X_umap', 'X_tsne', 'X_pca']):
    The 2D embedding to use. Default is 'X_tsne'.
    - title (str | None): Title of the plot. Default is None.
    - point_size (float): Size of the points. Default is 8.
    - alpha (float): Transparency level of the points. Default is 0.5.
    - figsize (tuple[int, int]): Size of the figure. Default is (8, 6).
    - dpi (int): Dots per inch for the figure. Default is 300.
    - fontsize (int): Font size for the legend. Default is 10.

    Returns:
    - fig, ax: The figure and axis of the plot.
    """
    assert "y" in adata.obs.columns, "Must have 'y' column in adata.obs"

    plt.rcParams["figure.dpi"] = dpi
    two_d_embedding = adata.obsm[use_2d]
    fig, ax = plt.subplots(figsize=figsize)

    unique_labels = np.unique(adata.obs["y"])
    for label in unique_labels:
        x = two_d_embedding[adata.obs["y"] == label, 0]
        y = two_d_embedding[adata.obs["y"] == label, 1]
        fig_label = f"{label} ({len(y)})"
        ax.scatter(x, y, label=fig_label, alpha=alpha, s=point_size)

    plt.legend(fontsize=fontsize)
    plt.axis("off")
    if title is not None:
        plt.title(title)

    return fig, ax


def plot_split(
    adata: AnnData,
    split_path: str,
    use_2d: Literal["X_umap", "X_tsne", "X_pca"] = "X_tsne",
    title: str | None = None,
    point_size: float = 8,
    alpha: float = 0.5,
    figsize: tuple[int, int] = (8, 6),
    dpi: int = 300,
):
    """
    Plot the split of the dataset based on a given split file.

    Parameters:
    - adata (AnnData): The annotated data object.
    - split_path (str): Path to the split file.
    - use_2d (Literal['X_umap', 'X_tsne', 'X_pca']):
    The 2D embedding to use. Default is 'X_tsne'.
    - title (str | None): Title of the plot. Default is None.
    - point_size (float): Size of the points. Default is 8.
    - alpha (float): Transparency level of the points. Default is 0.5.
    - figsize (tuple[int, int]): Size of the figure. Default is (8, 6).
    - dpi (int): Dots per inch for the figure. Default is 300.

    Returns:
    - fig, ax: The figure and axis of the plot.
    """
    split_df = pd.read_csv(split_path, index_col=0)
    unique_splits = np.unique(split_df["cluster"])

    plt.rcParams["figure.dpi"] = dpi
    two_d_embedding = adata.obsm[use_2d]
    fig, ax = plt.subplots(figsize=figsize)

    for split_val in unique_splits:
        accessions = set(split_df[split_df["cluster"] == split_val]["AC"].to_list())
        mask = adata.obs["accession"].isin(accessions)
        x = two_d_embedding[mask, 0]
        y = two_d_embedding[mask, 1]
        ax.scatter(x, y, label=f"Partition #{split_val}", alpha=alpha, s=point_size)

    plt.legend()
    plt.axis("off")
    if title is not None:
        plt.title(title)

    return fig, ax


def plot_partial_label_distribution(
    full_adata: AnnData,
    partial_adata: AnnData,
    use_2d: Literal["X_umap", "X_tsne", "X_pca"] = "X_tsne",
    title: str | None = None,
    point_size: float = 8,
    alpha: float = 0.5,
    figsize: tuple[int, int] = (8, 6),
    dpi: int = 300,
    fontsize: int = 10,
):
    """
    Plot the distribution of partial labels on a 2D embedding.

    Parameters:
    - full_adata (AnnData): The full annotated data object.
    - partial_adata (AnnData): The partial annotated data object with labels.
    - use_2d (Literal['X_umap', 'X_tsne', 'X_pca']):
    The 2D embedding to use. Default is 'X_tsne'.
    - title (str | None): Title of the plot. Default is None.
    - point_size (float): Size of the points. Default is 8.
    - alpha (float): Transparency level of the points. Default is 0.5.
    - figsize (tuple[int, int]): Size of the figure. Default is (8, 6).
    - dpi (int): Dots per inch for the figure. Default is 300.
    - fontsize (int): Font size for the legend. Default is 10.

    Returns:
    - fig, ax: The figure and axis of the plot.
    """
    ac2label = defaultdict(
        lambda: "No label",
        {
            ac: label
            for ac, label in zip(partial_adata.obs["accession"], partial_adata.obs["y"])
        },
    )
    full_adata.obs["y"] = full_adata.obs["accession"].map(ac2label)

    plt.rcParams["figure.dpi"] = dpi
    fig, ax = plt.subplots(figsize=figsize)
    two_d_embedding = full_adata.obsm[use_2d]

    for label in np.unique(full_adata.obs["y"]):
        x, y = (
            two_d_embedding[full_adata.obs["y"] == label, 0],
            two_d_embedding[full_adata.obs["y"] == label, 1],
        )
        fig_label = f"{label} ({len(y)})"
        if label == "No label":
            ax.scatter(
                x, y, label=fig_label, alpha=alpha, marker="x", c="black", s=point_size
            )
        else:
            ax.scatter(x, y, label=fig_label, alpha=alpha, s=point_size)

    plt.legend(fontsize=fontsize)
    plt.axis("off")
    if title is not None:
        plt.title(title)

    return fig, ax


def plot_partial_split(
    full_adata: AnnData,
    split_path: str,
    use_2d: Literal["X_umap", "X_tsne", "X_pca"] = "X_tsne",
    title: str | None = None,
    point_size: float = 8,
    alpha: float = 0.5,
    figsize: tuple[int, int] = (8, 6),
    dpi: int = 300,
    fontsize: int = 10,
):
    """
    Plot the partial split of the dataset based on a given split file.

    Parameters:
    - full_adata (AnnData): The full annotated data object.
    - split_path (str): Path to the split file.
    - use_2d (Literal['X_umap', 'X_tsne', 'X_pca']):
    The 2D embedding to use. Default is 'X_tsne'.
    - title (str | None): Title of the plot. Default is None.
    - point_size (float): Size of the points. Default is 8.
    - alpha (float): Transparency level of the points. Default is 0.5.
    - figsize (tuple[int, int]): Size of the figure. Default is (8, 6).
    - dpi (int): Dots per inch for the figure. Default is 300.
    - fontsize (int): Font size for the legend. Default is 10.

    Returns:
    - fig, ax: The figure and axis of the plot.
    """
    split_df = pd.read_csv(split_path, index_col=0)
    two_d_embedding = full_adata.obsm[use_2d]

    plt.rcParams["figure.dpi"] = dpi
    fig, ax = plt.subplots(figsize=figsize)

    ac2cluster = defaultdict(
        lambda: -1,
        {ac: cluster for ac, cluster in zip(split_df["AC"], split_df["cluster"])},
    )
    full_adata.obs["cluster"] = full_adata.obs["accession"].map(ac2cluster)

    for cluster in np.unique(full_adata.obs["cluster"]):
        x = two_d_embedding[full_adata.obs["cluster"] == cluster, 0]
        y = two_d_embedding[full_adata.obs["cluster"] == cluster, 1]

        if cluster == -1:
            ax.scatter(
                x, y, label="Not used", alpha=alpha, marker="x", c="black", s=point_size
            )
        else:
            ax.scatter(x, y, label=f"Partition #{cluster}", alpha=alpha, s=point_size)

    plt.legend(fontsize=fontsize)
    plt.axis("off")
    if title is not None:
        plt.title(title)

    return fig, ax
