import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)


def load_category_map(path: Path) -> dict[int, str]:
    data = json.loads(path.read_text())
    items = data["items"]
    return {int(it["id"]): it["snippet"]["title"] for it in items}


def main():
    cat_map = load_category_map(RAW / "GB_category_id.json")

    df = pd.read_csv(RAW / "GBvideos.csv")

    # ensure category_id is int so mapping works
    df["category_id"] = pd.to_numeric(df["category_id"], errors="coerce").astype("Int64")

    df["category_name"] = df["category_id"].map(cat_map)

    # keep a small, graph-friendly subset (you can add columns later)
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

    # basic cleanup
    df["publish_time"] = pd.to_datetime(df["publish_time"], errors="coerce", utc=True)
    df["views"] = pd.to_numeric(df["views"], errors="coerce")

    # save
    df.to_parquet(OUT / "gb_videos.parquet", index=False)
    df.to_csv(OUT / "gb_videos.csv", index=False)

    print("✅ Wrote:")
    print(" -", OUT / "gb_videos.parquet")
    print(" -", OUT / "gb_videos.csv")
    print("Rows:", len(df))


if __name__ == "__main__":
    main()
