# read_effdir.py
# Python translation of ReadEffDir.m (JENX) — Sections 1..15 + 13.5
# Produces an `effdir` dictionary similar to MATLAB's struct output.

import struct
from collections import defaultdict

def read_uint32(f):
    data = f.read(4)
    if len(data) < 4:
        raise EOFError("Unexpected EOF while reading uint32")
    return struct.unpack("<I", data)[0]

def read_int32(f):
    data = f.read(4)
    if len(data) < 4:
        raise EOFError("Unexpected EOF while reading int32")
    return struct.unpack("<i", data)[0]

def read_uint16(f):
    data = f.read(2)
    if len(data) < 2:
        raise EOFError("Unexpected EOF while reading uint16")
    return struct.unpack("<H", data)[0]

def read_int16(f):
    data = f.read(2)
    if len(data) < 2:
        raise EOFError("Unexpected EOF while reading int16")
    return struct.unpack("<h", data)[0]

def read_uint8(f):
    data = f.read(1)
    if len(data) < 1:
        raise EOFError("Unexpected EOF while reading uint8")
    return struct.unpack("<B", data)[0]

def read_int8(f):
    data = f.read(1)
    if len(data) < 1:
        raise EOFError("Unexpected EOF while reading int8")
    return struct.unpack("<b", data)[0]

def read_float(f):
    data = f.read(4)
    if len(data) < 4:
        raise EOFError("Unexpected EOF while reading float32")
    return struct.unpack("<f", data)[0]

def read_bytes(f, n):
    data = f.read(n)
    if len(data) < n:
        raise EOFError(f"Unexpected EOF while reading {n} bytes")
    return data

def read_string(f, length, encoding="latin1"):
    if length <= 0:
        return ""
    raw = read_bytes(f, length)
    try:
        return raw.decode(encoding, errors="ignore")
    except Exception:
        return raw.decode("latin1", errors="ignore")

def read_ubit_n_as_int(f, n_bytes):
    """Read N bytes and return little-endian integer"""
    raw = read_bytes(f, n_bytes)
    return int.from_bytes(raw, byteorder="little", signed=False)

def read_effdir(filename):
    effdir = {"sec": defaultdict(dict)}

    with open(filename, "rb") as f:
        # FILE HEADER: 2 x uint16
        effdir["init"] = [read_uint16(f), read_uint16(f)]

        # ---------------------------
        # SECTION 1 - Main Section
        # ---------------------------
        sec1 = {}
        sec1["n_entries"] = read_uint32(f)
        sec1["entry"] = []

        for _ in range(sec1["n_entries"]):
            e = {}
            # Read a long sequence of fields following the MATLAB comment order.
            # Many are DWORD (uint32) or float32 — translate as appropriate.
            # We'll follow the ordering described in the MATLAB file comments.

            # Basic header DWORDs
            e["dword1"] = read_uint32(f)
            e["constant0"] = read_uint32(f)  # usually 0x00000000
            e["dword2"] = read_uint32(f)

            # Duration min/max, released high detail, repeat flag
            e["duration_min"] = read_uint32(f)
            e["duration_max"] = read_uint32(f)
            e["released_high_detail"] = read_uint32(f)
            e["repeat_flag"] = read_uint32(f)

            # Some more DWORDs (time delay, pushes, velocity, shifts, size/variants)
            e["dword3"] = read_uint32(f)
            e["dword4"] = read_uint32(f)
            e["dword5"] = read_uint32(f)

            e["time_delay_min"] = read_uint32(f)
            e["time_delay_max"] = read_uint32(f)

            e["x_push_min"] = read_uint32(f)
            e["z_push_min"] = read_uint32(f)
            e["y_push_min"] = read_uint32(f)
            e["x_push_max"] = read_uint32(f)
            e["z_push_max"] = read_uint32(f)
            e["y_push_max"] = read_uint32(f)

            e["velocity_min"] = read_uint32(f)
            e["velocity_max"] = read_uint32(f)

            e["x_shift_min"] = read_uint32(f)
            e["z_shift_min"] = read_uint32(f)
            e["y_shift_min"] = read_uint32(f)
            e["x_shift_max"] = read_uint32(f)
            e["z_shift_max"] = read_uint32(f)
            e["y_shift_max"] = read_uint32(f)

            e["initial_size_var_pct"] = read_uint32(f)
            e["x_stretch_max"] = read_uint32(f)
            e["spin_var_max"] = read_uint32(f)
            e["dword6"] = read_uint32(f)
            e["alpha_var_max"] = read_uint32(f)
            e["color_var_r"] = read_uint32(f)
            e["color_var_g"] = read_uint32(f)
            e["color_var_b"] = read_uint32(f)

            # Reps list (DWORD count + DWORD reps)
            rep_count = read_uint32(f)
            e["reps"] = [read_uint32(f) for _ in range(rep_count)]

            # Color adjustments over time (count + 3*float per rep)
            color_rep = read_uint32(f)
            e["color_adj_over_time"] = []
            for _c in range(color_rep):
                r = read_float(f)
                g = read_float(f)
                b = read_float(f)
                e["color_adj_over_time"].append((r, g, b))

            # Brightness adjustments (count + float reps)
            bright_rep = read_uint32(f)
            e["brightness_over_time"] = [read_float(f) for _ in range(bright_rep)]

            # Size over time (count + float reps)
            size_rep = read_uint32(f)
            e["size_over_time"] = [read_float(f) for _ in range(size_rep)]

            # X-axis shrink/stretch over time
            xstretch_rep = read_uint32(f)
            e["xstretch_over_time"] = [read_float(f) for _ in range(xstretch_rep)]

            # Spin over time (count + reps as uint32 or float per original comment)
            spin_rep = read_uint32(f)
            e["spin_over_time"] = [read_uint32(f) for _ in range(spin_rep)]

            # Resource key (uint32)
            e["resource_key"] = read_uint32(f)

            # 2 bytes (unknown)
            e["two_bytes"] = read_uint16(f)

            # Several DWORD/float fields for movement/forces
            # Read several as floats where comments suggested float32, else uint32
            # We'll read as float where axis/forces are involved:
            e["d1"] = read_uint32(f)
            e["direction_of_travel_blur"] = read_uint32(f)
            e["x_force"] = read_uint32(f)
            e["z_force"] = read_uint32(f)
            e["y_force"] = read_uint32(f)
            e["carry"] = read_uint32(f)

            # many follow-up DWORDS (read a sequence)
            # read 9 additional DWORDs (to match the commented pattern)
            e["more_dw"] = [read_uint32(f) for _ in range(9)]

            # Spiral travel pattern max
            e["spiral_travel_max"] = read_uint32(f)

            # 28-byte reps (count + each rep is 7 floats?)
            spiral_rep = read_uint32(f)
            e["spiral_reps"] = []
            for _s in range(spiral_rep):
                # read 28 bytes -> 7 floats (but 7*4 = 28) if intended as floats
                vals = [read_float(f) for _ in range(7)]
                e["spiral_reps"].append(vals)

            # Additional unknown DWORDs (read 5)
            e["post_spiral_dw"] = [read_uint32(f) for _ in range(5)]

            # Coordinate system reps (count + 32-byte reps)
            coord_rep = read_uint32(f)
            e["coord_reps"] = []
            for _c in range(coord_rep):
                # 32 bytes -> 8 floats (X,Z,Y,X,Z,Y,seq,seq)
                vals = [read_float(f) for _ in range(8)]
                e["coord_reps"].append(vals)

            # Sub-entries count -> string list
            sub_count = read_uint32(f)
            e["sub_entries"] = []
            for _se in range(sub_count):
                slen = read_uint32(f)
                s = read_string(f, slen)
                sub_dw = read_uint32(f)
                e["sub_entries"].append({"str": s, "dw": sub_dw})

            # More trailing DWORDs - read a small block
            e["tail_dw1"] = read_uint32(f)
            e["tail_dw2"] = read_uint32(f)
            e["list_resource_keys_rep"] = read_uint32(f)
            e["list_resource_keys"] = [read_uint32(f) for _ in range(e["list_resource_keys_rep"])]
            e["tail_more"] = [read_uint32(f) for _ in range(3)]

            # Next list (count + reps)
            next_rep = read_uint32(f)
            e["next_list"] = [read_uint32(f) for _ in range(next_rep)]

            # End-of-entry marker (float probably 0x40800000)
            e["entry_end_marker"] = read_uint32(f)

            sec1["entry"].append(e)

        # End of section marker 0x0001 (uint16)
        sec1["eos"] = read_uint16(f)
        effdir["sec"][1] = sec1

        # ---------------------------
        # SECTION 2
        # ---------------------------
        sec2 = {}
        sec2["n_entries"] = read_uint32(f)
        sec2["entry"] = []
        for _ in range(sec2["n_entries"]):
            e = {}
            e["u1"] = read_uint32(f)
            e["resource_key"] = read_uint32(f)
            e["inverse_flg"] = read_uint8(f)
            e["repeat_flg"] = read_uint8(f)
            e["speed"] = read_float(f)

            # rotation over time
            rot_rep = read_uint32(f)
            e["rotation_over_time_rep"] = rot_rep
            e["rotation_over_time"] = [read_float(f) for _ in range(rot_rep)]

            # size adjustments over time
            size_rep = read_uint32(f)
            e["size_over_time_rep"] = size_rep
            e["size_over_time_pc"] = [read_float(f) for _ in range(size_rep)]

            # alpha over time
            alpha_rep = read_uint32(f)
            e["alpha_over_time_rep"] = alpha_rep
            e["alpha_over_time_pc"] = [read_float(f) for _ in range(alpha_rep)]

            # color adjustments over time (triples)
            color_rep = read_uint32(f)
            e["color_adj_over_time_rep"] = color_rep
            e["red"] = []
            e["green"] = []
            e["blue"] = []
            for _c in range(color_rep):
                e["red"].append(read_float(f))
                e["green"].append(read_float(f))
                e["blue"].append(read_float(f))

            # Y axis stretch over time
            yrep = read_uint32(f)
            e["y_axis_stretch_over_time_rep"] = yrep
            e["y_axis_stretch_over_time_pc"] = [read_float(f) for _ in range(yrep)]

            e["initial_intensity_var"] = read_float(f)
            e["initial_size_var"] = read_float(f)
            e["u2"] = read_float(f)
            e["u3"] = read_float(f)
            e["u4"] = read_float(f)
            e["u5"] = read_float(f)

            sec2["entry"].append(e)
        sec2["eos"] = read_uint16(f)
        effdir["sec"][2] = sec2

        # ---------------------------
        # SECTION 3
        # ---------------------------
        sec3 = {}
        sec3["n_entries"] = read_uint32(f)
        sec3["entry"] = []
        for _ in range(sec3["n_entries"]):
            e = {}
            e["u1"] = read_float(f)
            e["u2"] = read_float(f)
            u3_rep = read_uint32(f)
            e["u3_rep"] = u3_rep
            e["u3"] = [read_float(f) for _ in range(u3_rep)]
            u4_rep = read_uint32(f)
            e["u4_rep"] = u4_rep
            e["u4"] = [read_float(f) for _ in range(u4_rep)]
            e["u5"] = read_uint16(f)
            e["u6"] = read_uint8(f)
            e["u7"] = read_uint16(f)
            sec3["entry"].append(e)
        sec3["eos"] = read_uint16(f)
        effdir["sec"][3] = sec3

        # ---------------------------
        # SECTION 4
        # ---------------------------
        sec4 = {}
        sec4["n_entries"] = read_uint32(f)
        sec4["entry"] = []
        for _ in range(sec4["n_entries"]):
            e = {}
            u1_rep = read_uint32(f)
            e["u1_rep"] = u1_rep
            e["u1"] = {"u1": [], "u2": [], "u3": []}
            for _r in range(u1_rep):
                e["u1"]["u1"].append(read_float(f))
                e["u1"]["u2"].append(read_float(f))
                e["u1"]["u3"].append(read_float(f))
            u2_rep = read_uint32(f)
            e["u2_rep"] = u2_rep
            e["u2"] = [read_float(f) for _ in range(u2_rep)]
            e["u3"] = read_float(f)
            sec4["entry"].append(e)
        # EOS for sec4 may or may not be present; MATLAB commented out
        effdir["sec"][4] = sec4

        # ---------------------------
        # SECTION 5
        # ---------------------------
        sec5 = {}
        sec5["n_entries"] = read_uint32(f)
        sec5["entry"] = []
        for _ in range(sec5["n_entries"]):
            e = {}
            e["u1"] = read_uint8(f)
            e["u2"] = read_uint8(f)
            e["resource_key"] = read_uint32(f)
            e["u3"] = read_float(f)
            e["u4"] = read_float(f)
            e["u3b"] = read_ubit_n_as_int(f, 5)  # ubit40
            e["u5"] = read_float(f)
            e["u6"] = read_float(f)
            e["u7"] = read_float(f)
            e["u8"] = read_float(f)
            e["u9"] = read_float(f)
            sec5["entry"].append(e)
        effdir["sec"][5] = sec5

        # ---------------------------
        # SECTION 6
        # ---------------------------
        sec6 = {}
        sec6["n_entries"] = read_uint32(f)
        sec6["entry"] = []
        for _ in range(sec6["n_entries"]):
            e = {}
            e["u1"] = read_uint16(f)
            str_rep = read_uint32(f)
            e["str_rep"] = str_rep
            e["str"] = read_string(f, str_rep)
            e["type_id"] = read_uint8(f)
            sec6["entry"].append(e)
        effdir["sec"][6] = sec6

        # ---------------------------
        # SECTION 7
        # ---------------------------
        sec7 = {}
        sec7["n_entries"] = read_uint32(f)
        sec7["entry"] = []
        for _ in range(sec7["n_entries"]):
            e = {}
            # MATLAB used ubit58 etc. — we read raw 22 bytes to be safe
            e["u1_raw"] = read_bytes(f, 22)
            e["u2"] = read_float(f)
            e["u3"] = read_uint32(f)
            e["u4"] = read_uint32(f)
            e["u5"] = read_uint32(f)
            e["u5b"] = read_uint32(f)
            e["u6"] = read_float(f)
            e["u7"] = read_float(f)
            e["u8"] = read_float(f)
            e["u9"] = read_float(f)
            e["u10"] = read_uint32(f)
            e["u11"] = read_uint32(f)
            e["u12"] = read_uint32(f)
            sec7["entry"].append(e)
        effdir["sec"][7] = sec7

        # ---------------------------
        # SECTION 8
        # ---------------------------
        sec8 = {}
        sec8["n_entries"] = read_uint32(f)
        sec8["entry"] = []
        for _ in range(sec8["n_entries"]):
            e = {}
            e["u1"] = read_uint16(f)
            u2_rep = read_uint32(f)
            e["u2_rep"] = u2_rep
            e["u2"] = []
            for _s in range(u2_rep):
                sub = {}
                sub["u1"] = read_float(f)
                sub["u2"] = read_float(f)
                slen = read_uint32(f)
                sub["str_rep"] = slen
                sub["str"] = read_string(f, slen)
                e["u2"].append(sub)
            e["u3"] = read_uint32(f)
            sec8["entry"].append(e)
        effdir["sec"][8] = sec8

        # ---------------------------
        # SECTION 9
        # ---------------------------
        sec9 = {}
        sec9["n_entries"] = read_uint32(f)
        sec9["entry"] = []
        for _ in range(sec9["n_entries"]):
            e = {}
            e["u1"] = read_ubit_n_as_int(f, 6)  # ubit48 -> 6 bytes
            e["sound_resource_key"] = read_uint32(f)
            e["u2"] = read_float(f)
            e["u3"] = read_float(f)
            sec9["entry"].append(e)
        effdir["sec"][9] = sec9

        # ---------------------------
        # SECTION 10
        # ---------------------------
        sec10 = {}
        sec10["n_entries"] = read_uint32(f)
        sec10["entry"] = []
        for _ in range(sec10["n_entries"]):
            e = {}
            e["u1"] = read_float(f)
            e["u2"] = read_float(f)
            e["u3"] = read_float(f)
            sec10["entry"].append(e)
        sec10["eos"] = read_uint16(f)
        effdir["sec"][10] = sec10

        # ---------------------------
        # SECTION 11
        # ---------------------------
        sec11 = {}
        sec11["n_entries"] = read_uint32(f)
        sec11["entry"] = []
        for _ in range(sec11["n_entries"]):
            e = {}
            e["u1"] = read_uint32(f)
            str_rep = read_uint32(f)
            e["str_rep"] = str_rep
            e["str"] = read_string(f, str_rep) if str_rep > 0 else ""
            e["u2"] = read_uint32(f)
            e["u3"] = read_uint32(f)
            e["u4"] = read_uint32(f)
            e["u5"] = read_float(f)
            e["u6"] = read_float(f)
            e["u7"] = read_float(f)
            e["u8"] = read_float(f)
            e["u9"] = read_float(f)
            sec11["entry"].append(e)
        sec11["eos"] = read_uint16(f)
        effdir["sec"][11] = sec11

        # ---------------------------
        # SECTION 12
        # ---------------------------
        sec12 = {}
        sec12["n_entries"] = read_uint32(f)
        sec12["entry"] = []
        for _ in range(sec12["n_entries"]):
            e = {}
            e["u1"] = read_uint32(f)
            e["u2"] = read_uint32(f)
            prim_rep = read_uint32(f)
            e["prim_indx_rep"] = prim_rep
            e["prim_indx"] = []
            for _p in range(prim_rep):
                p = {}
                str_rep = read_uint32(f)
                p["str_rep"] = str_rep
                p["str"] = read_string(f, str_rep) if str_rep > 0 else ""
                p["indx_flag"] = read_uint8(f)
                p["u1"] = read_float(f)
                p["u2"] = read_float(f)
                p["u3a"] = read_uint32(f)
                p["u3b"] = read_uint32(f)
                p["u4"] = read_float(f)
                p["u5"] = read_float(f)
                p["u6"] = read_float(f)
                p["u7"] = read_float(f)
                p["u8"] = read_float(f)
                p["u9"] = read_float(f)
                p["xshift"] = read_float(f)
                p["zshift"] = read_float(f)
                p["yshift"] = read_float(f)
                p["u10"] = read_float(f)
                p["u11a"] = read_ubit_n_as_int(f, 5)
                p["u11b"] = read_ubit_n_as_int(f, 5)
                p["u12"] = read_float(f)
                p["u13"] = read_float(f)
                p["u14"] = read_float(f)
                p["u15"] = read_float(f)
                p["u16"] = read_uint16(f)
                p["u17"] = read_uint16(f)
                p["indx_key"] = read_uint32(f)
                e["prim_indx"].append(p)

            # secondary indices
            secidx_rep = read_uint32(f)
            e["sec_indx_rep"] = secidx_rep
            e["sec_indx"] = []
            for _s in range(secidx_rep):
                s = {}
                s["u1"] = read_uint32(f)
                s_str_rep = read_uint32(f)
                s["str_rep"] = s_str_rep
                s["str"] = read_string(f, s_str_rep) if s_str_rep > 0 else ""
                s["u2"] = read_uint32(f)
                s["index_key"] = read_uint32(f)
                e["sec_indx"].append(s)

            e["u3"] = read_uint32(f)
            e["u4"] = read_uint32(f)
            e["u5"] = read_uint32(f)
            e["u6"] = read_uint32(f)
            sec12["entry"].append(e)
        effdir["sec"][12] = sec12

        # ---------------------------
        # SECTION 13 (Main Effect Directory)
        # ---------------------------
        # Note: MATLAB loops sec12.n_entries + 1 times
        sec13 = {}
        sec13["entry"] = []
        # Use sec12 n_entries if present
        sec12_count = sec12.get("n_entries", 0)
        for _ in range(sec12_count + 1):
            entry = {}
            srep = read_uint32(f)
            entry["str_rep"] = srep
            entry["str"] = read_string(f, srep) if srep > 0 else ""
            entry["index_key"] = read_uint32(f)
            sec13["entry"].append(entry)
        sec13["eos1"] = read_uint8(f)
        sec13["eos2"] = read_uint8(f)
        effdir["sec"][13] = sec13

        # ---------------------------
        # SECTION 13.5
        # ---------------------------
        sec135 = {}
        sec135["u1"] = read_int8(f)
        sec135["u2"] = read_uint32(f)
        sec135["u3"] = read_float(f)
        sec135["u4"] = read_float(f)
        sec135["u5"] = read_float(f)
        sec135["u6"] = read_float(f)
        sec135["u7"] = read_float(f)
        sec135["u8"] = read_float(f)
        sec135["u9"] = read_float(f)
        sec135["u10"] = read_float(f)
        sec135["u11"] = read_float(f)
        effdir["sec135"] = sec135

        # ---------------------------
        # SECTION 14
        # ---------------------------
        sec14 = {}
        sec14["n_entries"] = read_uint32(f)
        sec14["entry"] = []
        for _ in range(sec14["n_entries"]):
            e = {}
            srep = read_uint32(f)
            e["str_rep"] = srep
            e["str"] = read_string(f, srep) if srep > 0 else ""
            e["group_prop"] = read_uint32(f)
            e["instance_prop"] = read_uint32(f)
            sec14["entry"].append(e)
        sec14["eos"] = read_uint16(f)
        effdir["sec"][14] = sec14

        # ---------------------------
        # SECTION 15
        # ---------------------------
        sec15 = {}
        sec15["n_entries"] = read_uint32(f)
        sec15["entry"] = []
        for _ in range(sec15["n_entries"]):
            e = {}
            e["class_id"] = read_uint32(f)
            srep = read_uint32(f)
            e["str_rep"] = srep
            e["str"] = read_string(f, srep) if srep > 0 else ""
            sec15["entry"].append(e)
        effdir["sec"][15] = sec15

        # Done reading file; EOF should be next.
    return effdir

# Example usage:
# eff = read_effdir("some_effect.eff")
# print(eff["sec"][2]["entry"][0]["resource_key"])
