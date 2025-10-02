# main.py
# Simple CLI to read, write, isolate using the other modules.
import argparse
import os
import pickle
from read_effdir import read_effdir
from write_effdir import write_effdir
from isolate_eff import isolate_eff

def save_pickle(obj, path):
    with open(path, "wb") as fh:
        import pickle
        pickle.dump(obj, fh)

def load_pickle(path):
    with open(path, "rb") as fh:
        import pickle
        return pickle.load(fh)

def cmd_read(args):
    eff = read_effdir(args.input)
    # Save a pickle snapshot so subsequent ops can load it quickly
    out_pickle = args.input + ".pkl"
    save_pickle(eff, out_pickle)
    print(f"Read {args.input} -> saved snapshot {out_pickle}")

def cmd_isolate(args):
    # read eff into memory (from file or snapshot)
    if args.input.endswith(".pkl"):
        eff = load_pickle(args.input)
    else:
        eff = read_effdir(args.input)
    neff = isolate_eff(eff, args.index, args.name)
    # write isolated file using write_effdir
    write_effdir(args.output, neff)
    print(f"Isolated effect #{args.index} as '{args.name}' -> {args.output}")

def cmd_write(args):
    # either load snapshot or read then write
    if args.input.endswith(".pkl"):
        eff = load_pickle(args.input)
    else:
        eff = read_effdir(args.input)
    write_effdir(args.output, eff)
    print(f"Wrote {args.output}")

def main():
    parser = argparse.ArgumentParser(prog="EffDirEditor")
    sub = parser.add_subparsers(dest="cmd")

    p_read = sub.add_parser("read"); p_read.add_argument("input")
    p_read.set_defaults(func=cmd_read)

    p_write = sub.add_parser("write"); p_write.add_argument("input"); p_write.add_argument("output")
    p_write.set_defaults(func=cmd_write)

    p_isolate = sub.add_parser("isolate")
    p_isolate.add_argument("input")   # .eff or .pkl snapshot
    p_isolate.add_argument("index", type=int)
    p_isolate.add_argument("name")
    p_isolate.add_argument("output")
    p_isolate.set_defaults(func=cmd_isolate)

    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        return
    args.func(args)

if __name__ == "__main__":
    main()
