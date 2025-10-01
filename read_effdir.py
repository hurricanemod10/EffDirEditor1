"""
read_effdir.py
---------------
Reads EffDir binary files into a Python data structure.

Converted from original MATLAB script.
"""

import struct


class EffDir:
    def __init__(self):
        # Store sections as a dictionary
        self.sec = {}

    def read_from_file(self, filename):
        with open(filename, "rb") as f:
            section_num = 1

            while True:
                # Example: read DWORD (4 bytes) as unsigned int
                data = f.read(4)
                if not data:
                    break  # End of file

                dword_val = struct.unpack("<I", data)[0]

                # Store the result in sec[section_num]
                self.sec[section_num] = {"dword": dword_val}

                # In MATLAB you had a loop across sections (1–15)
                # Here we just increment and continue
                section_num += 1

        print(f"Read {section_num-1} sections.")
        return self
