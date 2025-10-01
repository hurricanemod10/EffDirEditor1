"""
main.py
-------
Command-line tool for reading, writing, and isolating effects
from SimCity 4 EffDir files.

Usage:
    python main.py read input.effdir
    python main.py write input.json output.effdir
    python main.py isolate input.effdir output.effdir --index 5 --name "farmhorses"

    # Read EffDir into JSON (terminal output)
python main.py read myfile.effdir

# Isolate one effect (index 5, rename it)
python main.py isolate myfile.effdir newfile.effdir --index 5 --name farmhorses
"""

import argparse
import json
from read_effdir import read_effdir
from write_effdir import write_effdir
from isolate_eff import isolate_eff


def main():
    parser = argparse.ArgumentParser(
        description="EffDir Editor - Read, Write, Isolate SimCity 4 effect directories"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- Read EffDir ---
    read_parser = subparsers.add_parser("read", help="Read an EffDir file")
    read_parser.add_argument("input", help="Path to input .effdir file")

    # --- Write EffDir ---
    write_parser = subparsers.add_parser("write", help="Write EffDir from JSON")
    write_parser.add_argument("input", help="Path to input JSON file")
    write_parser.add_argument("output", help="Path to output .effdir file")

    # --- Isolate Effect ---
    isolate_parser = subparsers.add_parser("isolate", help="Isolate one effect")
    isolate_parser.add_argument("input", help="Path to input .effdir file")
    isolate_parser.add_argument("output", help="Path to output .effdir file")
    isolate_parser.add_argument("--index", type=int, required=True, help="Effect index (in section 13)")
    isolate_parser.add_argument("--name", type=str, required=True, help="New name for isolated effect")

    args = parser.parse_args()

    # --- Handle commands ---
    if args.command == "read":
        effdir = read_effdir(args.input)
        print(json.dumps(effdir.sec, indent=2, default=str))

    elif args.command == "write":
        with open(args.input, "r") as f:
            data = json.load(f)
        write_effdir(data, args.output)
        print(f"EffDir written to {args.output}")

    elif args.command == "isolate":
        effdir = read_effdir(args.input)
        new_effdir = isolate_eff(effdir, args.index, args.name)
        write_effdir(new_effdir, args.output)
        print(f"Isolated effect saved to {args.output}")


if __name__ == "__main__":
    main()
  
