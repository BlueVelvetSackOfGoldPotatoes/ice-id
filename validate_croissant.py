#!/usr/bin/env python3
import sys
import argparse
import mlcroissant as mlc

def validate_file(jsonld_path: str, debug: bool = False) -> int:
    """
    Validate a Croissant JSON-LD file using the mlcroissant library.
    
    Args:
        jsonld_path: Local path or URL to the Croissant metadata file.
        debug: If True, print detailed debug information.
    
    Returns:
        Exit code: 0 if valid (warnings only), 1 if errors found.
    """
    try:
        # Load the dataset metadata (static analysis happens on load)
        ds = mlc.Dataset(jsonld=jsonld_path)
        issues = ds.metadata.issues
    except Exception as e:
        print(f"❌ Failed to load or parse Croissant file: {e}")
        return 1

    # Print full report (warnings + errors)
    report = issues.report()  # prints a human-readable summary :contentReference[oaicite:0]{index=0}
    print(report)

    # If there are any hard errors, signal failure
    if issues.errors:
        print("❌ Croissant validation failed (errors above).")
        return 1

    print("✅ Croissant validation passed (no errors).")
    return 0

def main():
    parser = argparse.ArgumentParser(
        description="Validate a Croissant metadata JSON-LD file using mlcroissant."
    )
    parser.add_argument(
        "jsonld",
        help="Path or URL to the Croissant metadata JSON-LD file"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug output (not yet implemented in API; reserved for future use)"
    )
    args = parser.parse_args()
    sys.exit(validate_file(args.jsonld, args.debug))

if __name__ == "__main__":
    main()
