import json
import subprocess
import tempfile
import zipfile
from pathlib import Path


def sh(cmd: list[str]) -> str:
    p = subprocess.run(cmd, text=True, capture_output=True)
    if p.returncode != 0:
        raise RuntimeError(
            f"Command failed ({p.returncode}): {cmd}\n"
            f"STDOUT:\n{p.stdout}\n"
            f"STDERR:\n{p.stderr}\n"
        )
    return p.stdout.strip()


def load_version(state_file: Path) -> int:
    if not state_file.exists():
        return -1
    try:
        return int(json.loads(state_file.read_text()).get("versionNumber", -1))
    except Exception:
        return -1


def save_version(state_file: Path, dataset: str, v: int) -> None:
    state_file.write_text(json.dumps({"dataset": dataset, "versionNumber": v}, indent=2))


def fetch_if_newer(dataset: str, needed: list[str], raw_dir: Path, state_file: Path) -> bool:
   
    raw_dir.mkdir(parents=True, exist_ok=True)

  
    out = sh(["kaggle", "datasets", "files", "-d", dataset])
    lines = out.splitlines()

    sizes = []
    for line in lines:
        parts = line.split()
        if len(parts) >= 2 and parts[-1].upper().endswith(("KB", "MB", "GB")):
            size = parts[-1].upper()
            if size.endswith("KB"):
                sizes.append(int(float(size[:-2]) * 1_000))
            elif size.endswith("MB"):
                sizes.append(int(float(size[:-2]) * 1_000_000))
            elif size.endswith("GB"):
                sizes.append(int(float(size[:-2]) * 1_000_000_000))

    remote_v = sum(sizes)
    local_v = load_version(state_file)

    if remote_v <= local_v:
        print(f"✅ Up to date (local={local_v}, remote={remote_v})")
        return False

    print(f"⬇️ Downloading (local={local_v}, remote={remote_v})")

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)

        sh(["kaggle", "datasets", "download", "-d", dataset, "-p", str(td)])
        zip_path = next(td.glob("*.zip"))

        with zipfile.ZipFile(zip_path) as z:
            names = z.namelist()
            for want in needed:
                match = next(
                    (n for n in names if n.endswith("/" + want) or n.endswith(want)),
                    None
                )
                if not match:
                    raise SystemExit(f"Missing in zip: {want}")
                (raw_dir / want).write_bytes(z.read(match))

    save_version(state_file, dataset, remote_v)
    print("✅ Done. Saved:", ", ".join(needed))
    return True


if __name__ == "__main__":
    ROOT = Path(__file__).resolve().parents[1]
    DATASET = "datasnaek/youtube-new"
    NEEDED = ["GBvideos.csv", "GB_category_id.json"]

    fetch_if_newer(
        dataset=DATASET,
        needed=NEEDED,
        raw_dir=ROOT / "data" / "raw",
        state_file=ROOT / "state.json",
    )

