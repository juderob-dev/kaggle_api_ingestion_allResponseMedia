from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt



def plot_top_categories_views(parquet_path: Path, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    df = pd.read_parquet(parquet_path)

   
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

    outpath = out_dir / "top_categories_views.png"
    
    plt.savefig(outpath, dpi=200)
    print("✅ Saved:", outpath)
    return outpath



