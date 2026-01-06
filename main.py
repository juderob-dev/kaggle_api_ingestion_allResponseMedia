# This is a very basic prompt file to get you started, feel free to amend as you please, though please use the dataset and file names provided
from pathlib import Path

from config import DATASET, CSV_FILE_NAME, JSON_FILE_NAME, DOWNLOAD_URL 
from scripts.fetch_data import fetch_if_newer
from scripts.transform import transform_gb
from scripts.plot import plot_top_categories_views


def main():
    root = Path(__file__).resolve().parent

    raw_dir = root / "data" / "raw"
    processed_dir = root / "data" / "processed"
    output_dir = root / "output"
    state_file = root / "state.json"

    needed = [CSV_FILE_NAME, JSON_FILE_NAME]

    print("== Fetch ==")
    _downloaded = fetch_if_newer(DATASET, needed, raw_dir, state_file)

    print("\n== Transform ==")
    parquet_path = transform_gb(raw_dir, processed_dir, CSV_FILE_NAME, JSON_FILE_NAME)

    print("\n== Plot ==")
    plot_top_categories_views(parquet_path, output_dir)

    print("\n✅ Pipeline complete.")
    print("(Reference URL you provided):", DOWNLOAD_URL)


if __name__ == "__main__":
    main()

