import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read results
df = pd.read_csv("benchmark.csv")

# Extract dataset names
df["dataset_size"] = df["input"].str.extract(r"_(\d+)pct").astype(int)

# Tool order
tools = ["delly", "tiddit", "manta", "lumpy"]

# Dataset sizes
dataset_sizes = sorted(df["dataset_size"].unique())

# Set bar positions
x = np.arange(len(dataset_sizes))
width = 0.2

# Organize data
def get_values(metric, tool):
    values = []

    for size in dataset_sizes:
        result = df[
            (df["tool"].str.lower() == tool) &
            (df["dataset_size"] == size)
        ][metric]

        # Average if multiple runs exist
        values.append(result.mean() if not result.empty else np.nan)

    return values


# GRAPH 1: RUNTIME 

fig, ax = plt.subplots(figsize=(10, 6))

for i, tool in enumerate(tools):
    values = get_values("runtime_seconds", tool)

    ax.bar(
        #i wanted it to have spaces for visual clarity
        x + (i - 1.5) * width,
        values,
        width,
        label=tool.capitalize()
    )

ax.set_xlabel("BAM Dataset Size")
ax.set_ylabel("Runtime (seconds)")
ax.set_title("SV Caller Runtime Comparison")
ax.set_xticks(x)
ax.set_xticklabels([f"{size}%" for size in dataset_sizes])

ax.set_yscale("linear")
ax.legend(title="SV Caller")
ax.grid(axis="y", linestyle="--", alpha=0.4)

plt.tight_layout()
#save to results
plt.savefig("results/runtime_comparison.png", dpi=300)
plt.show()


# GRAPH 2: PEAK MEMORY 

fig, ax = plt.subplots(figsize=(10, 6))

for i, tool in enumerate(tools):
    values = get_values("peak_memory_mb", tool)

    ax.bar(
        x + (i - 1.5) * width,
        values,
        width,
        label=tool.capitalize()
    )

ax.set_xlabel("BAM Dataset Size")
ax.set_ylabel("Peak Memory (MB)")
ax.set_title("SV Caller Peak Memory Comparison")
ax.set_xticks(x)
ax.set_xticklabels([f"{size}%" for size in dataset_sizes])

ax.set_yscale("linear")
ax.legend(title="SV Caller")
ax.grid(axis="y", linestyle="--", alpha=0.4)

plt.tight_layout()
#save to results
plt.savefig("results/memory_comparison.png", dpi=300)
plt.show()
