"""Validate every data JSON file, build its dropdown manifest, and stage Pages."""
import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def validate_table(data, path):
    if isinstance(data, list):
        rows = data
        if not rows:
            raise ValueError(f"{path}: an empty table must define columns")
    elif isinstance(data, dict):
        rows = data.get("rows", data.get("students", data.get("data")))
        columns = data.get("columns")
        if columns is not None:
            if not isinstance(columns, list) or not columns:
                raise ValueError(f"{path}: columns must be a non-empty array")
            keys = []
            for column in columns:
                if isinstance(column, str) and column:
                    keys.append(column)
                elif isinstance(column, dict) and isinstance(column.get("key"), str) and column["key"]:
                    keys.append(column["key"])
                else:
                    raise ValueError(f"{path}: each column needs a non-empty key")
            if len(keys) != len(set(keys)):
                raise ValueError(f"{path}: duplicate column keys")
        if not rows and not columns:
            raise ValueError(f"{path}: an empty table must define columns")
    else:
        raise ValueError(f"{path}: expected a table object or an array of row objects")
    if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
        raise ValueError(f"{path}: rows must be an array of objects")
    return rows


def build(local_manifest=False):
    entries = []
    files = sorted((ROOT / "data").rglob("*.json"), key=lambda p: p.as_posix().casefold())
    if not files:
        raise ValueError("Add at least one table JSON file in data/")
    for path in files:
        relative = path.relative_to(ROOT).as_posix()
        try:
            data = json.loads(path.read_text(encoding="utf-8-sig"))
            rows = validate_table(data, relative)
        except (ValueError, OSError) as error:
            raise ValueError(f"Cannot build {relative}: {error}") from error
        title = data.get("title") if isinstance(data, dict) else None
        entries.append({"file": relative, "title": str(title or path.stem), "count": len(rows)})
    target = ROOT / "_site"
    if target.exists():
        shutil.rmtree(target)
    target.mkdir()
    shutil.copy2(ROOT / "index.html", target / "index.html")
    shutil.copytree(ROOT / "data", target / "data")
    manifest = json.dumps({"files": entries}, ensure_ascii=False, indent=2) + "\n"
    (target / "files.json").write_text(manifest, encoding="utf-8")
    (target / ".nojekyll").write_text("", encoding="utf-8")
    if local_manifest:
        (ROOT / "files.json").write_text(manifest, encoding="utf-8")
    print(f"Built {len(entries)} table(s), {sum(entry['count'] for entry in entries)} rows in _site/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--local-manifest", action="store_true")
    try:
        build(parser.parse_args().local_manifest)
    except (ValueError, OSError) as error:
        raise SystemExit(str(error))
