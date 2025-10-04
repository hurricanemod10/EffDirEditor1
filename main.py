import argparse
import json
import sys
import traceback
import struct

def main():
    print("Effect Dir Editor v1.0 starting...")
    # This just ensures the build runs correctly.
    # Later we’ll connect this to read_effdir, write_effdir, and isolate_eff.
    print("Build successful. Ready for EffDir operations.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Effect Dir Editor v1.0")
    args = parser.parse_args()
    main()
    
# main.py
"""
CLI entrypoint for EffDirEditor (minimal, robust).
Usage examples:
    python main.py read input.effdir
    python main.py isolate input.effdir output.effdir --index 5 --name farmhorses
    python main.py write input.json output.effdir
"""

from read_effdir import read_effdir
from write_effdir import write_effdir
from isolate_eff import isolate_eff

def safe_print_json(obj):
    try:
        print(json.dumps(obj, indent=2, ensure_ascii=False))
    except Exception:
        # fallback: print repr
        print(repr(obj))

def main():
    parser = argparse.ArgumentParser(description="EffDirEditor (minimal)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("read", help="Read an EffDir file")
    r.add_argument("input", help="Input .effdir file")

    w = sub.add_parser("write", help="Write effdir from a JSON file (minimal)")
    w.add_argument("input", help="Input JSON file")
    w.add_argument("output", help="Output .effdir file")

    iso = sub.add_parser("isolate", help="Isolate an effect (minimal)")
    iso.add_argument("input", help="Input .effdir file")
    iso.add_argument("output", help="Output .effdir file")
    iso.add_argument("--index", type=int, required=True)
    iso.add_argument("--name", type=str, required=True)

    args = parser.parse_args()

    try:
        if args.cmd == "read":
            info = read_effdir(args.input)
            # remove raw bytes from printing to keep logs small
            info_no_raw = {k: v for k, v in info.items() if k != "_raw_bytes"}
            safe_print_json(info_no_raw)

        elif args.cmd == "write":
            with open(args.input, "r", encoding="utf-8") as jf:
                data = json.load(jf)
            res = write_effdir(data, args.output)
            safe_print_json(res)

        elif args.cmd == "isolate":
            eff = read_effdir(args.input)
            ne = isolate_eff(eff, args.index, args.name)
            res = write_effdir(ne, args.output)
            safe_print_json(res)

    except Exception as e:
        print("ERROR during command execution:", file=sys.stderr)
        traceback.print_exc()
        sys.exit(2)


if __name__ == "__main__":
    main()
