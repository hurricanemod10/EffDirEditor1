"""
write_effdir.py
---------------
Writes EffDir binary data back to file.

Converted from original MATLAB script.
"""

import struct


def write_effdir(effdir, filename):
    """
    Write an EffDir object (from read_effdir.py) to a binary file.
    effdir.sec[...] should contain dictionaries with the data.
    """

    with open(filename, "wb") as f:
        for sec_num, sec_data in effdir.sec.items():
            # Example: write the DWORD value we stored in read_effdir
            if "dword" in sec_data:
                f.write(struct.pack("<I", sec_data["dword"]))

    print(f"EffDir structure written to {filename}")
