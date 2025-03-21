# SAEA Benchmark

A Python package to benchmark sequence splitting algorithms using:
- BLAST-based sequence identity calculation
- ML model performance evaluation

## Installation

This package can be installed via pip.
```
pip install saea-benchmark
```

## Usage

Instantiate an experiment object.

```
from saea_benchmark.experiment import BenchmarkExperiment

# Initialize experiment
benchmark = BenchmarkExperiment(
   full_fasta_file_path='*.fasta', # Path to the fasta file containing all sequences
   split_file_path='*.csv',        # Path to the csv file for the split
   suite=['blast', 'model']
)
```

Prepare arguments for configuring an experiment. 
```
args_blast = {
   "out_file": "blast_output.csv", # Path to save the identities, None for not saving them
   "max_identity_threshold": 0.8,  # Threshold for the "% below threshold" metric
   "n_procs": 8                    # Number of threads for sequence alignment
}

args_model = {
   "train_val_adata_path": '*.h5ad', # Path to the .h5ad file for train/validation
   "test_adata_path": '*.h5ad',      # Path to the .h5ad file for test
   "metric_name": 'gorodkin',        # Metric for hyperparam tuning, gorodkin, mcc or f1
   "n_trials": 10,                   # Number of tuning steps
   "random_state": 42,               # Random state
   "allow_logging": False            # Whether optuna logs are displayed
}
```

Run experiments.
```
# Run separately
blast_results = benchmark.run_blast_benchmark(**args_blast)
model_results = benchmark.run_model_benchmark(**args_model)

# Run together sequentially
merged_results = benchmark.run_suite(
    {
        'blast': args_blast,
        'model': args_model
    },
    concurrent=True # Run two suites concurrently
)
```

Save the results of an experiment.
```
benchmark.save_results('*.json') # Save results to a json file
```

Generate a plot to visualize the experiment.
```
import matplotlib.pyplot as plt
from saea_benchmark.create_plot import visualize_fold_analysis

fig = visualize_fold_analysis(
   full_adata_path='*.h5ad',      # .h5ad file storing embedding of all sequences
   split_df_path='*.csv',         # Path to the csv file for the split
   dataset_name='Cyc',            # Name of the dataset displayed on the title
   experiment_json_path='*.json', # File saving the results of benchmarking, default to None (no benchmarking results displayed)
   figsize=(14, 6),               # Figure size for matplotlib, default to (14, 6)
   width_ratios=(0.5, 0.5),       # Ratio of left/right halves of the image, default to (0.5, 0.5)
   scatter_alpha=0.5,             # Transparency for the scatter plot, default to 0.5
   table_col_widths=(0.15, 0.25, 0.3, 0.3, 0.3, 0.3), # Column widths for the table, default to (0.15, 0.25, 0.3, 0.3, 0.3, 0.3)
   table_font_size: int = 12,     # Font size for text in the table, default to 12
   table_scale=(0.65, 6),         # Scale for width/height of the table, default to (0.65, 6)
   bar_alpha=0.7,                 # Transparency for the bar plot, default to 0.7
   bar_width=0.25,                # Width of the bar, default to 0.25
   dpi=300,                       # Resolution of displayed/saved image, default to 300
   save_path=None,                # Path for saving the image, default to None (not saving the image)
)
plt.show()
```

Other methods can be viewed at [this notebook](https://github.com/qzheng75/saea_benchmark/blob/main/notebooks/example.ipynb).
