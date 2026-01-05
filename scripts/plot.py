from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
INP = ROOT / "data" / "processed" / "gb_videos.parquet"
OUTDIR = ROOT / "output"
OUTDIR.mkdir(parents=True, exist_ok=True)


def main():
    df = pd.read_parquet(INP)

    # group and sort
    top = (
        df.dropna(subset=["category_name", "views"])
          .groupby("category_name", as_index=False)["views"].sum()
          .sort_values("views", ascending=False)
          .head(10)
    )

    plt.figure(figsize=(10, 6))
    plt.barh(top["category_name"][::-1], top["views"][::-1])  # reverse for nice ordering
    plt.xlabel("Total views (sum across rows)")
    plt.ylabel("Category")
    plt.title("Top 10 YouTube Trending Categories (GB) by Total Views")
    plt.tight_layout()

    outpath = OUTDIR / "top_categories_views.png"
    plt.savefig(outpath, dpi=200)
    print("✅ Saved:", outpath)


if __name__ == "__main__":
    main()
