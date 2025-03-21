"""
Compute maximum identity to other partitions for each sequence
in a partitioning using needleall.
Source: https://github.com/graph-part/graph-part/blob/main/benchmarking/partitioning_quality/align_partitions.py
"""

from __future__ import annotations

import concurrent.futures
import math
import os
import subprocess
from itertools import groupby
from tempfile import TemporaryDirectory
from typing import Dict, Tuple

import numpy as np
import pandas as pd
from tqdm import tqdm

NORMALIZATIONS = {
    "shortest": lambda a, b, c: a / min(b, c),  # a identity b len(seq1) c len(seq2)
    "longest": lambda a, b, c: a / max(b, c),
    "mean": lambda a, b, c: a / ((b + c) / 2),
}


def partition_fasta_file(
    fasta_file: str, partition_file: str, sep="|", directory=None
) -> Tuple[int, Dict[str, int]]:
    """
    Make a temporary fasta file for each individual partition,
    given the .csv assignments.
    Also return the number of partitions and the sequence lengths for convenience,
    so we don't have to read the file again.
    """
    seq_dict = {}  # Acc : Seq
    seq_lens = {}  # Acc : len

    # read fasta
    with open(fasta_file, "r") as f:
        id_seq_groups = (
            group for group in groupby(f, lambda line: line.startswith(">"))
        )

        for is_id, id_iter in id_seq_groups:
            if is_id:  # Only needed to find first id line, always True thereafter
                id = next(id_iter).strip().split(sep)[0]
                seq = "".join(seq.strip() for seq in next(id_seq_groups)[1])
                seq_dict[id.lstrip(">")] = seq
                seq_lens[id.lstrip(">")] = len(seq)

    # read partition table
    #'AC,label-val,cluster\n'
    df = pd.read_csv(partition_file)

    for idx, cl in enumerate(df["cluster"].unique()):
        acc_ids = df.loc[df["cluster"] == cl]["AC"]
        out_path = (
            f"partition_{idx}.fasta.tmp"
            if directory is None
            else f"{directory}/partition_{idx}.fasta.tmp"
        )
        with open(out_path, "w") as f:
            for acc_id in acc_ids:
                f.write(f">{acc_id}\n")
                f.write(seq_dict[acc_id] + "\n")
    return idx + 1, seq_lens


def chunk_fasta_file(
    fasta_file: str,
    n_chunks: int,
    prefix: str = "chunk",
    sep: str = "|",
    directory=None,
) -> int:
    """
    Break up fasta file into multiple smaller files that can be
    used for multiprocessing.
    Returns the number of generated chunks.
    """

    # read fasta
    ids = []
    seqs = []
    with open(fasta_file, "r") as f:
        id_seq_groups = (
            group for group in groupby(f, lambda line: line.startswith(">"))
        )
        for is_id, id_iter in id_seq_groups:
            if is_id:  # Only needed to find first id line, always True thereafter
                ids.append(next(id_iter).strip().split(sep)[0])
                seqs.append("".join(seq.strip() for seq in next(id_seq_groups)[1]))

    chunk_size = math.ceil(len(ids) / n_chunks)
    empty_chunks = 0
    for i in range(n_chunks):
        # because of ceil() we sometimes make less partitions than specified.
        if i * chunk_size >= len(ids):
            empty_chunks += 1
            continue

        chunk_ids = ids[i * chunk_size : (i + 1) * chunk_size]
        chunk_seqs = seqs[i * chunk_size : (i + 1) * chunk_size]

        out_path = (
            f"{prefix}_{i}.fasta.tmp"
            if directory is None
            else f"{directory}/{prefix}_{i}.fasta.tmp"
        )
        with open(out_path, "w") as f:
            for id, seq in zip(chunk_ids, chunk_seqs):
                f.write(id + "\n")
                f.write(seq + "\n")

    return n_chunks - empty_chunks


def compute_edges(
    query_fp: str,
    library_fp: str,
    results_dict: Dict[str, Tuple[float, str]],
    seq_lens: Dict[str, int],
    pbar: tqdm,
    denominator="full",
    delimiter: str = "|",
    is_nucleotide: bool = False,
    gapopen: float = 10,
    gapextend: float = 0.5,
    endweight: bool = False,
    endopen: float = 10,
    endextend: float = 0.5,
    matrix: str = "EBLOSUM62",
) -> None:
    """
    Run needleall on query_fp and library_fp,
    Retrieve pairwise similiarities, transform and
    insert into edge_dict.
    """
    if is_nucleotide:
        (
            type_1,
            type_2,
        ) = "-snucleotide1", "-snucleotide2"
    else:
        type_1, type_2 = "-sprotein1", "-sprotein2"

    command = [
        "needleall",
        "-auto",
        "-stdout",
        "-aformat",
        "pair",
        "-gapopen",
        str(gapopen),
        "-gapextend",
        str(gapextend),
        "-endopen",
        str(endopen),
        "-endextend",
        str(endextend),
        "-datafile",
        matrix,
        type_1,
        type_2,
        query_fp,
        library_fp,
    ]
    if endweight:
        command = command + ["-endweight"]

    count = 0
    with subprocess.Popen(
        command, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True
    ) as proc:
        for line_nr, line in enumerate(proc.stdout):
            if line.startswith("# 1:"):
                # # 1: P0CV73
                this_qry = line[5:].split()[0].split("|")[0]

            elif line.startswith("# 2:"):
                this_lib = line[5:].split()[0].split("|")[0]

            elif line.startswith("# Identity:"):
                identity_line = line

            elif line.startswith("# Gaps:"):
                count += 1
                if count == 1000:
                    pbar.update(1000)
                    count = 0
                # Gaps:           0/142 ( 0.0%)
                gaps, rest = line[7:].split("/")
                gaps = int(gaps)
                length = int(rest.split("(")[0])

                # Compute different sequence identities as needed.
                if denominator == "full":  # full is returned by default
                    identity = float(identity_line.split("(")[1][:-3]) / 100
                elif denominator == "no_gaps":
                    n_matches = int(identity_line[11:].split("/")[0])
                    identity = float(n_matches / (length - gaps))
                else:
                    n_matches = int(identity_line[11:].split("/")[0])
                    identity = NORMALIZATIONS[denominator](
                        n_matches, seq_lens[this_qry], seq_lens[this_lib]
                    )

                if this_qry not in results_dict:
                    results_dict[this_qry] = (identity, this_lib)
                else:
                    if results_dict[this_qry][0] < identity:
                        results_dict[this_qry] = (identity, this_lib)


def align_partitions(
    fasta_file: str,
    partition_file: str,
    denominator="full",
    delimiter: str = "|",
    is_nucleotide: bool = False,
    gapopen: float = 10,
    gapextend: float = 0.5,
    endweight: bool = False,
    endopen: float = 10,
    endextend: float = 0.5,
    matrix: str = "EBLOSUM62",
    n_procs: int = 8,
) -> Dict[str, Tuple[float, str]]:
    """
    Align each partition against each other partition,
    and find the shortest distance of each sample to any other sample in
    any other partition.
    """
    # Make partition files.
    with TemporaryDirectory() as tmp_dir:
        n_partitions, seq_lens = partition_fasta_file(
            fasta_file, partition_file, directory=tmp_dir
        )

        results_dict = {}  # Acc: [max_id, Acc]

        part_size = len(seq_lens) // n_partitions
        # this is still wrong,
        # we would need to count the actual number of seqs in each partition
        # like that its just an upper bound.
        pbar = tqdm(
            total=part_size * part_size * (n_partitions * n_partitions - n_partitions)
        )  # inner complexity x nested for loops.
        jobs = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=n_procs) as executor:
            for query_partition in range(n_partitions):
                for lib_partition in range(n_partitions):
                    if query_partition == lib_partition:
                        continue
                    else:
                        q = os.path.join(
                            tmp_dir, f"partition_{query_partition}.fasta.tmp"
                        )
                        l = os.path.join(
                            tmp_dir, f"partition_{lib_partition}.fasta.tmp"
                        )

                        # chunk one of the files to max out threads.
                        # otherwise, can at max use (n_partitions x n_partitions)
                        # - n_partitions threads.
                        n_chunks = chunk_fasta_file(
                            q,
                            n_chunks=10,
                            prefix=f"chunk_p_{query_partition}",
                            directory=tmp_dir,
                        )
                        for i in range(n_chunks):
                            q_c = os.path.join(
                                tmp_dir, f"chunk_p_{query_partition}_{i}.fasta.tmp"
                            )
                            future = executor.submit(
                                compute_edges,
                                q_c,
                                l,
                                results_dict,
                                seq_lens,
                                pbar,
                                denominator,
                                delimiter,
                                is_nucleotide,
                                gapopen,
                                gapextend,
                                endweight,
                                endopen,
                                endextend,
                                matrix,
                            )
                            jobs.append(future)
        return results_dict


def verify_needle_installation():
    try:
        subprocess.run(["needle", "-version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise RuntimeError(
            "EMBOSS 'needle' command not found. "
            + "Please install EMBOSS package: "
            + "conda install -c bioconda emboss"
        )


def get_max_identities(
    fasta_file: str,
    partition_file: str,
    out_file: str | None = None,
    denominator="full",
    is_nucleotide: bool = False,
    delimiter: str = "|",
    gapopen: float = 10,
    gapextend: float = 0.5,
    endweight: bool = False,
    endopen: float = 10,
    endextend: float = 0.5,
    matrix: str = "EBLOSUM62",
    n_procs: int = 8,
) -> pd.DataFrame:
    verify_needle_installation()
    try:
        identities = align_partitions(
            fasta_file=fasta_file,
            partition_file=partition_file,
            denominator=denominator,
            delimiter=delimiter,
            is_nucleotide=is_nucleotide,
            gapopen=gapopen,
            gapextend=gapextend,
            endweight=endweight,
            endopen=endopen,
            endextend=endextend,
            matrix=matrix,
            n_procs=n_procs,
        )
    except Exception as e:
        raise Exception(f"Error during partition alignment: {e}")

    df_partitions = pd.read_csv(partition_file)
    df_partitions["max_ident_other"] = None
    df_partitions["closest_other"] = None

    for idx, row in df_partitions.iterrows():
        max_ident, closest = identities[row["AC"]]
        df_partitions.loc[idx, "max_ident_other"] = max_ident
        df_partitions.loc[idx, "closest_other"] = closest

    if out_file is not None:
        df_partitions.to_csv(out_file, index=False)

    return df_partitions


def compute_identity(
    input_df: pd.DataFrame | None = None,
    input_file: str | None = None,
    threshold: float = 0.8,
    exclude_clusters: list[int] | None = None,
) -> dict[str, float]:
    if input_df is None and input_file is None:
        raise ValueError("Either input_df or input_file must be provided.")
    if input_df is not None and input_file is not None:
        raise ValueError("Only one of input_df or input_file can be provided.")
    if input_df is not None:
        df = input_df
    else:
        df = pd.read_csv(input_file, index_col=0)
    if exclude_clusters is None:
        exclude_clusters = []

    n_bins = len(np.unique(df["cluster"]))
    result = {}
    for cluster in range(n_bins):
        if cluster in exclude_clusters:
            continue
        test_size = np.mean(df["cluster"] == cluster)
        temp_df = df[df["cluster"] == cluster]
        mask = temp_df["max_ident_other"] <= threshold
        result[cluster] = {"size": test_size, "under_threshold": mask.mean()}

    return result
