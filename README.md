# Kaggle YouTube Trending Pipeline (GB)

A small, end-to-end Python data pipeline that fetches, transforms, and visualizes
YouTube Trending data from Kaggle.

The entire pipeline is executed with a single command:

```bash
python main.py
```

Dataset source:  
https://www.kaggle.com/datasets/datasnaek/youtube-new

---

## What This Project Does

When you run `main.py`, the pipeline performs three steps:

1. **Fetch**  
   Downloads the latest Kaggle dataset **only if it has changed** (idempotent).

2. **Transform**  
   Cleans and enriches the raw CSV/JSON files into a graph-ready format.

3. **Plot**  
   Generates a simple analytical visualization from the processed data.

---

## Project Structure

```
kaggle-youtube-trending/
│
├── scripts/
│   ├── fetch_data.py      # Fetch logic (idempotent)
│   ├── transform.py       # Data transformation
│   └── plot.py            # Visualization
│
├── data/
│   ├── raw/               # Raw Kaggle files
│   └── processed/         # Cleaned data
│
├── output/                # Generated plots
│
├── state.json             # Tracks dataset version (size-based heuristic)
├── main.py                # Orchestrates the full pipeline
├── requirements.txt
└── README.md
```

---

## Requirements

- Python 3.9+
- Kaggle account with API access

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## (Recommended) Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Kaggle API Setup (Required)

1. Go to Kaggle → Account → API → **Create New Token**
2. Move the token:
```bash
mkdir -p ~/.kaggle
mv kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json
```
if this does not work, use method on kaggle website
which will state 
export KAGGLE_API_TOKEN=KGAT_***********************

Verify access:
```bash
kaggle datasets list # (old way)
kaggle competitions list #(new way)
```


---

## Running the Pipeline

```bash
python main.py
```

The pipeline is safe to run multiple times.  
The fetch step will only download data if the remote dataset has changed.

---

## Outputs

After running `main.py`, the following files are produced:

```
data/raw/
  GBvideos.csv
  GB_category_id.json

data/processed/
  gb_videos.parquet
  gb_videos.csv

output/
  top_categories_views.png

state.json
```

---

## What the Plot Shows

- **Top 10 YouTube trending categories in Great Britain**
- Ranked by **total view count**
- Aggregated across all trending entries

Output file:
```
output/top_categories_views.png
```

---

## Design Notes

- Uses the official Kaggle CLI for reliability
- No hard-coded dataset versions
- Idempotent fetch step to avoid unnecessary downloads
- Explicit pipeline orchestration in `main.py`
- Focused on clarity and simplicity over abstraction

---

## Summary

This project demonstrates a simple, reproducible data pipeline:
- External data ingestion
- Data transformation
- Basic analytical visualization

Designed to be readable, extensible, and interview-ready.
