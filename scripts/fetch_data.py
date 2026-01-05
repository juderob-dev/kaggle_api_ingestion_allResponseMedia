import json
import subprocess
import tempfile
import zipfile
from pathlib import Path

DATASET = "datasnaek/youtube-new"
NEEDED = ["GBvideos.csv", "GB_category_id.json"]

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
STATE = ROOT / "state.json"


def sh(cmd: list[str]) -> str:
    p = subprocess.run(cmd, text=True, capture_output=True)
    if p.returncode != 0:
        raise RuntimeError(
            f"Command failed ({p.returncode}): {cmd}\n"
            f"STDOUT:\n{p.stdout}\n"
            f"STDERR:\n{p.stderr}\n"
        )
    return p.stdout.strip()
def load_version() -> int:
    if not STATE.exists():
        return -1
    try:
        return int(json.loads(STATE.read_text()).get("versionNumber", -1))
    except Exception:
        return -1


def save_version(v: int) -> None:
    STATE.write_text(json.dumps({"dataset": DATASET, "versionNumber": v}, indent=2))


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    out = sh(["kaggle", "datasets", "files", "-d", DATASET])

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
    local_v = load_version()

    if remote_v <= local_v:
        print(f"✅ Up to date (local={local_v}, remote={remote_v})")
        return
  

    print(f"⬇️ Downloading (local={local_v}, remote={remote_v})")

    
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)

        # 3. download zip
        sh(["kaggle", "datasets", "download", "-d", DATASET, "-p", str(td)])

        zip_path = next(td.glob("*.zip"))

        # 4. extract only what we need
        with zipfile.ZipFile(zip_path) as z:
            names = z.namelist()
            for want in NEEDED:
                match = next(
                    (n for n in names if n.endswith("/" + want) or n.endswith(want)),
                    None
                )
                if not match:
                    raise SystemExit(f"Missing in zip: {want}")
                (RAW / want).write_bytes(z.read(match))

    # 5. save new state
    save_version(remote_v)
    print("✅ Done. Saved:", ", ".join(NEEDED))


if __name__ == "__main__":
    main()
