#!/usr/bin/env python3
import json
import hashlib
import argparse
import os
import sys

def compute_sha256(path: str) -> str:
    """Compute SHA-256 digest of the given file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    p = argparse.ArgumentParser(
        description="Inject real SHA256 checksums into a Croissant JSON-LD"
    )
    p.add_argument(
        "jsonld_in",
        help="Input JSON-LD file (with placeholders)"
    )
    p.add_argument(
        "-o", "--output",
        default="croissant.with-sha256.json",
        help="Output JSON-LD file"
    )
    args = p.parse_args()

    # Load JSON-LD
    with open(args.jsonld_in, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Ensure distribution exists
    dists = data.get("distribution", [])
    if not dists:
        print("No 'distribution' array found in JSON-LD.", file=sys.stderr)
        sys.exit(1)

    # Process each fileObject
    for entry in dists:
        cid = entry.get("contentUrl")
        if not cid:
            continue

        # If checksum already present and not a placeholder, skip
        existing = entry.get("sha256", "")
        if existing and not existing.startswith("REPLACE_WITH_"):
            print(f"✔ Skipping {cid}, already has sha256: {existing}")
            continue

        # Compute path relative to JSON file directory
        base = os.path.dirname(os.path.abspath(args.jsonld_in))
        file_path = os.path.join(base, cid)
        if not os.path.isfile(file_path):
            print(f"❌ File not found: {file_path}", file=sys.stderr)
            sys.exit(1)

        sha256 = compute_sha256(file_path)
        entry["sha256"] = sha256
        print(f"✔ {cid} → {sha256}")

    # Write updated JSON-LD
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"\n✅ Wrote updated JSON-LD to {args.output}")

if __name__ == "__main__":
    main()
