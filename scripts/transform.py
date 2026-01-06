import json
from pathlib import Path
import pandas as pd


def load_category_map(path: Path) -> dict[int, str]:
    data = json.loads(path.read_text())
    items = data["items"]
    return {int(it["id"]): it["snippet"]["title"] for it in items}

def transform_gb(raw_dir: Path, out_dir: Path, csv_file: str, json_file: str) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)

    cat_map = load_category_map(raw_dir / json_file)
    df = pd.read_csv(raw_dir / csv_file)

    df["category_id"] = pd.to_numeric(df["category_id"], errors="coerce").astype("Int64")
    df["category_name"] = df["category_id"].map(cat_map)

    keep = [
        "title",
        "channel_title",
        "publish_time",
        "trending_date",
        "category_id",
        "category_name",
        "views",
        "likes",
        "dislikes",
        "comment_count",
    ]
    df = df[keep]

    df["publish_time"] = pd.to_datetime(df["publish_time"], errors="coerce", utc=True)
    df["views"] = pd.to_numeric(df["views"], errors="coerce")

    outpath = out_dir / "gb_videos.parquet"
    df.to_parquet(outpath, index=False)
    df.to_csv(out_dir / "gb_videos.csv", index=False)

    print("✅ Transformed ->", outpath)
    print("Rows:", len(df))

    return outpath


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    transform_gb(
        raw_dir=root / "data" / "raw",
        out_dir=root / "data" / "processed",
    )
