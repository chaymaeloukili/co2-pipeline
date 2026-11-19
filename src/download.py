import hashlib
import http.client
import shutil
import sys
from datetime import date
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen


COMMIT = "382ee6c662b0ece26e111f263b44c029afad7787"
FILES = (
    "owid-co2-data.csv",
    "owid-co2-codebook.csv",
)
BASE_URL = f"https://raw.githubusercontent.com/owid/co2-data/{COMMIT}"


class DownloadError(RuntimeError):
    pass


def download_file(url: str, destination: Path) -> bool:
    created = False
    try:
        with destination.open("xb") as output:
            created = True
            with urlopen(url, timeout=60) as response:
                shutil.copyfileobj(response, output)
    except FileExistsError:
        return False
    except (OSError, http.client.HTTPException, URLError) as error:
        if created:
            try:
                destination.unlink()
            except OSError as cleanup_error:
                raise DownloadError(
                    f"Download failed for {destination.name}, and the partial "
                    f"file could not be removed: {cleanup_error}"
                ) from error
        raise DownloadError(
            f"Download failed for {destination.name}: {error}"
        ) from error
    return True


def file_details(path: Path) -> tuple[int, str]:
    checksum = hashlib.sha256()
    size = 0
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            size += len(chunk)
            checksum.update(chunk)
    return size, checksum.hexdigest()


def append_source(log, url: str, filename: str) -> None:
    log.seek(0)
    contents = log.read()
    if contents and not contents.endswith(("\n", "\r")):
        log.write("\n")
    log.write(f"{date.today().isoformat()}\t{url}\t{filename}\n")
    log.flush()


def main() -> int:
    project_root = Path(__file__).resolve().parent.parent
    raw_dir = project_root / "data" / "raw"
    sources_path = raw_dir / "SOURCES.txt"
    urls = {
        filename: f"{BASE_URL}/{filename}"
        for filename in FILES
    }

    try:
        raw_dir.mkdir(parents=True, exist_ok=True)
        for filename in FILES:
            path = raw_dir / filename
            if path.is_symlink() and not path.exists():
                raise OSError(f"{path} is a broken symbolic link")
            if path.exists() and not path.is_file():
                raise OSError(f"{path} exists but is not a regular file")

        missing = [
            filename
            for filename in FILES
            if not (raw_dir / filename).exists()
        ]
        if missing:
            with sources_path.open("a+", encoding="utf-8", newline="\n") as log:
                for filename in FILES:
                    path = raw_dir / filename
                    if not path.exists():
                        downloaded = download_file(urls[filename], path)
                        if downloaded:
                            append_source(log, urls[filename], filename)

                    size, checksum = file_details(path)
                    print(
                        f"{filename}: {size} bytes, SHA-256 {checksum}"
                    )
        else:
            for filename in FILES:
                path = raw_dir / filename
                size, checksum = file_details(path)
                print(f"{filename}: {size} bytes, SHA-256 {checksum}")
    except (DownloadError, OSError, URLError, http.client.HTTPException) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
