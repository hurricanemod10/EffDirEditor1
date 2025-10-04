import argparse

def main():
    print("Effect Dir Editor v1.0 starting...")
    # This just ensures the build runs correctly.
    # Later we’ll connect this to read_effdir, write_effdir, and isolate_eff.
    print("Build successful. Ready for EffDir operations.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Effect Dir Editor v1.0")
    args = parser.parse_args()
    main()
