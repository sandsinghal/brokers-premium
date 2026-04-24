"""
scripts/download_data.py
------------------------
Download the SNAP Twitch Gamers dataset (~15 MB zipped) into `.data/`.

Usage:
    python scripts/download_data.py
"""
import os
import urllib.request
import zipfile

DATADIR = ".data"
ZIPURL = "https://snap.stanford.edu/data/twitch_gamers.zip"
ZIPPATH = os.path.join(DATADIR, "twitch_gamers.zip")


def main() -> None:
    os.makedirs(DATADIR, exist_ok=True)
    if not os.path.exists(ZIPPATH):
        print(f"Downloading Twitch Gamers from {ZIPURL}...")
        urllib.request.urlretrieve(ZIPURL, ZIPPATH)
        print(f"  Saved to {ZIPPATH}")
    else:
        print(f"Already present at {ZIPPATH}")
    print("Extracting...")
    with zipfile.ZipFile(ZIPPATH, "r") as z:
        z.extractall(DATADIR)
    print(f"Done. Files in {DATADIR}:")
    for f in sorted(os.listdir(DATADIR)):
        size_mb = os.path.getsize(os.path.join(DATADIR, f)) / 1e6
        print(f"  {f}  ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
