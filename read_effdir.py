func read_effdir.py
# Line-by-line Python translation of ReadEffDir.m (struct-style)
import struct


def _read_uint32(f):
    data = f.read(4)
    if len(data)!=4:
        raise EOFError("Unexpected EOF reading uint32")
    return struct.unpack("<I", data)[0]

def _read_int32(f):
    data = f.read(4); return struct.unpack("<i", data)[0]

def _read_uint16(f):
    data = f.read(2); return struct.unpack("<H", data)[0]

def _read_int16(f):
    data = f.read(2); return struct.unpack("<h", data)[0]

def _read_uint8(f):
    data = f.read(1); return struct.unpack("<B", data)[0]

def _read_int8(f):
    data = f.read(1); return struct.unpack("<b", data)[0]

def _read_float(f):
    data = f.read(4); return struct.unpack("<f", data)[0]

def _read_bytes(f, n):
    data = f.read(n)
    if len(data) != n:
        raise EOFError(f"Unexpected EOF reading {n} bytes")
    return data

def read_effdir(path):
    """
    Read an .eff file into a nested dict structure effdir similar to MATLAB effdir struct.
    """
    effdir = {"sec": {}}
    with open(path, "rb") as f:
        # header: originally fread(fid,2,'uint16') in MATLAB; earlier translations sometimes used different counts
        # we'll read two uint16 exactly like your MATLAB header
        effdir["init"] = [_read_uint16(f), _read_uint16(f)]

        # Section 1
        sec1 = {}
        sec1["n_entries"] = _read_uint32(f)
        sec1["entry"] = []
        for _ in range(sec1["n_entries"]):
            e = {}
            # The original is very large; read fields in same order as your MATLAB comments/translations
            e["u1"] = _read_int32(f)
            e["u2"] = _read_int32(f)
            e["u3"] = _read_int32(f)
            e["dur_min"] = _read_float(f)
            e["dur_max"] = _read_float(f)
            e["high_detail"] = _read_float(f)
            e["loop"] = _read_uint32(f)
            e["u4"] = _read_float(f)
            e["u5"] = _read_float(f)
            e["u6"] = _read_float(f)
            e["delay_min"] = _read_float(f)
            e["delay_max"] = _read_float(f)
            e["x_axis_push_min"] = _read_float(f)
            e["z_axis_push_min"] = _read_float(f)
            e["y_axis_push_min"] = _read_float(f)
            e["x_axis_push_max"] = _read_float(f)
            e["z_axis_push_max"] = _read_float(f)
            e["y_axis_push_max"] = _read_float(f)
            e["init_vel_min"] = _read_float(f)
            e["init_vel_max"] = _read_float(f)
            e["initial_x_axis_shift_min"] = _read_float(f)
            e["initial_z_axis_shift_min"] = _read_float(f)
            e["initial_y_axis_shift_min"] = _read_float(f)
            e["initial_x_axis_shift_max"] = _read_float(f)
            e["initial_z_axis_shift_max"] = _read_float(f)
            e["initial_y_axis_shift_max"] = _read_float(f)
            e["initial_size_varation_pc"] = _read_float(f)
            e["initial_x_axis_stretch_max"] = _read_float(f)
            e["initial_spin_variation_max"] = _read_float(f)
            e["u7"] = _read_float(f)
            e["initial_alpha_var_max"] = _read_float(f)
            e["initial_color_var_pc_red"] = _read_float(f)
            e["initial_color_var_pc_green"] = _read_float(f)
            e["initial_color_var_pc_blue"] = _read_float(f)

            # u8 reps (count then floats)
            e["u8_rep"] = _read_uint32(f)
            e["u8"] = [_read_float(f) for __ in range(e["u8_rep"])]

            # color adjustments (triples)
            e["color_adj_over_time_rep"] = _read_uint32(f)
            e["red"] = []
            e["green"] = []
            e["blue"] = []
            for __ in range(e["color_adj_over_time_rep"]):
                e["red"].append(_read_float(f))
                e["green"].append(_read_float(f))
                e["blue"].append(_read_float(f))

            # brightness reps
            e["bright_adj_over_time_rep"] = _read_uint32(f)
            e["bright"] = [_read_float(f) for __ in range(e["bright_adj_over_time_rep"])]

            # size reps
            e["size_over_time_rep"] = _read_uint32(f)
            e["size"] = [_read_float(f) for __ in range(e["size_over_time_rep"])]

            # x shrink
            e["x_shrink_over_time_rep"] = _read_uint32(f)
            e["x_shrink"] = [_read_float(f) for __ in range(e["x_shrink_over_time_rep"])]

            # spin over time
            e["spin_over_time_rep"] = _read_uint32(f)
            e["spin"] = [_read_float(f) for __ in range(e["spin_over_time_rep"])]

            e["main_resource_key"] = _read_uint32(f)
            e["u9"] = _read_int16(f)
            e["u10"] = _read_uint32(f)

            e["direction_travel_blur"] = _read_float(f)
            e["x_force"] = _read_float(f)
            e["y_force"] = _read_float(f)
            e["z_force"] = _read_float(f)
            e["carry"] = _read_float(f)

            # read dozens of trailing floats/dwords as per your MATALB file: keep same names
            e["u11"] = _read_float(f); e["u12"] = _read_float(f); e["u13"] = _read_float(f)
            e["u14"] = _read_float(f); e["u15"] = _read_float(f)

            e["spiral_travel_pattern_max"] = _read_float(f)

            # u16: rep of 28-byte reps? Your writer used uint64/u32; we read as sequence of
            e["u16_rep"] = _read_uint32(f)
            e["u16"] = []
            for __ in range(e["u16_rep"]):
                # original used uint64 for some fields — read them as two uint64 and a uint32
                u16block = {
                    "u1": _read_uint32(f), # Note: using uint32 here to avoid platform issues; adapt if needed
                    "u2": _read_uint32(f),
                    "u3": _read_uint32(f),
                    "u4": _read_uint32(f)
                }
                e["u16"].append(u16block)

            # u17..u33 etc (read as floats)
            for label in ["u17","u18","u19","u20","u21","u22"]:
                e[label] = _read_float(f)
            e["u23_rep"] = _read_uint32(f)
            e["u23"] = [_read_float(f) for __ in range(e["u23_rep"])]

            # tail floats
            for label in ["u24","u25","u26","u27","u28","u29","u30","u31","u32","u33"]:
                e[label] = _read_float(f)

            # string u34
            e["u34_str_rep"] = _read_uint32(f)
            e["u34_str"] = ""
            if e["u34_str_rep"]>0:
                e["u34_str"] = f.read(e["u34_str_rep"]).decode("latin1", errors="ignore")

            # more floats
            for label in ["u35","u36","u37","u38","u39","u40","u41","u42","u43","u44","u45","u46","u47","u48"]:
                e[label] = _read_float(f)

            e["u49_rep"] = _read_uint32(f)
            e["u49"] = [_read_float(f) for __ in range(e["u49_rep"])]

            e["u50"] = _read_float(f)
            e["u51"] = _read_float(f)

            # coordinate system movements (32-byte reps -> 8 floats)
            e["coord_syst_mvt_rep"] = _read_uint32(f)
            e["coord"] = {"x1":[],"y1":[],"z1":[],"x2":[],"y2":[],"z2":[],"seq_num1":[],"seq_num2":[]}
            for __ in range(e["coord_syst_mvt_rep"]):
                e["coord"]["x1"].append(_read_float(f))
                e["coord"]["y1"].append(_read_float(f))
                e["coord"]["z1"].append(_read_float(f))
                e["coord"]["x2"].append(_read_float(f))
                e["coord"]["y2"].append(_read_float(f))
                e["coord"]["z2"].append(_read_float(f))
                e["coord"]["seq_num1"].append(_read_float(f))
                e["coord"]["seq_num2"].append(_read_float(f))

            e["u52"] = _read_float(f)

            # u53 subentries
            e["u53_rep"] = _read_uint32(f)
            e["u53_str_rep"] = []
            e["u53_str"] = []
            e["u53_u1"] = []
            for __ in range(e["u53_rep"]):
                srep = _read_uint32(f)
                e["u53_str_rep"].append(srep)
                if srep>0:
                    e["u53_str"].append(f.read(srep).decode("latin1", errors="ignore"))
                else:
                    e["u53_str"].append("")
                e["u53_u1"].append(_read_float(f))

            e["u54"] = _read_float(f)
            e["u55"] = _read_float(f)

            # resource key list
            e["resource_key_rep"] = _read_uint32(f)
            e["resource_key"] = [_read_uint32(f) for __ in range(e["resource_key_rep"])]

            e["u56"] = _read_float(f)
            e["u57"] = _read_float(f)

            e["u58_rep"] = _read_uint32(f)
            e["u58"] = [_read_float(f) for __ in range(e["u58_rep"])]

            e["eoe"] = _read_uint32(f)
            sec1["entry"].append(e)
        sec1["eos"] = _read_uint16(f)
        effdir["sec"][1] = sec1

        # Section 2
        sec2 = {}
        sec2["n_entries"] = _read_uint32(f)
        sec2["entry"] = []
        for _ in range(sec2["n_entries"]):
            e = {}
            e["u1"] = _read_uint32(f)
            e["resource_key"] = _read_uint32(f)
            e["inverse_flg"] = _read_uint8(f)
            e["repeat_flg"] = _read_uint8(f)
            e["speed"] = _read_float(f)

            rot_rep = _read_uint32(f)
            e["rotation_over_time_rep"] = rot_rep
            e["rotation_over_time"] = [_read_float(f) for __ in range(rot_rep)]

            size_rep = _read_uint32(f)
            e["size_over_time_rep"] = size_rep
            e["size_over_time_pc"] = [_read_float(f) for __ in range(size_rep)]

            alpha_rep = _read_uint32(f)
            e["alpha_over_time_rep"] = alpha_rep
            e["alpha_over_time_pc"] = [_read_float(f) for __ in range(alpha_rep)]

            color_rep = _read_uint32(f)
            e["color_adj_over_time_rep"] = color_rep
            e["red"] = []; e["green"] = []; e["blue"] = []
            for __ in range(color_rep):
                e["red"].append(_read_float(f)); e["green"].append(_read_float(f)); e["blue"].append(_read_float(f))

            yrep = _read_uint32(f)
            e["y_axis_stretch_over_time_rep"] = yrep
            e["y_axis_stretch_over_time_pc"] = [_read_float(f) for __ in range(yrep)]

            e["initial_intensity_var"] = _read_float(f)
            e["initial_size_var"] = _read_float(f)
            e["u2"] = _read_float(f); e["u3"] = _read_float(f); e["u4"] = _read_float(f); e["u5"] = _read_float(f)

            sec2["entry"].append(e)
        sec2["eos"] = _read_uint16(f)
        effdir["sec"][2] = sec2

        # Section 3
        sec3 = {"n_entries": _read_uint32(f), "entry":[]}
        for _ in range(sec3["n_entries"]):
            e = {}
            e["u1"] = _read_float(f)
            e["u2"] = _read_float(f)
            u3_rep = _read_uint32(f); e["u3_rep"] = u3_rep
            e["u3"] = [_read_float(f) for __ in range(u3_rep)]
            u4_rep = _read_uint32(f); e["u4_rep"] = u4_rep
            e["u4"] = [_read_float(f) for __ in range(u4_rep)]
            e["u5"] = _read_uint16(f)
            e["u6"] = _read_uint8(f)
            e["u7"] = _read_uint16(f)
            sec3["entry"].append(e)
        sec3["eos"] = _read_uint16(f)
        effdir["sec"][3] = sec3

        # Section 4
        sec4 = {"n_entries": _read_uint32(f), "entry":[]}
        for _ in range(sec4["n_entries"]):
            e = {}
            u1_rep = _read_uint32(f); e["u1_rep"]=u1_rep
            e["u1"] = {"u1":[], "u2":[], "u3":[]}
            for __ in range(u1_rep):
                e["u1"]["u1"].append(_read_float(f)); e["u1"]["u2"].append(_read_float(f)); e["u1"]["u3"].append(_read_float(f))
            u2_rep = _read_uint32(f); e["u2_rep"] = u2_rep
            e["u2"] = [_read_float(f) for __ in range(u2_rep)]
            e["u3"] = _read_float(f)
            sec4["entry"].append(e)
        effdir["sec"][4] = sec4

        # Section 5
        sec5 = {"n_entries": _read_uint32(f), "entry":[]}
        for _ in range(sec5["n_entries"]):
            e = {}
            e["u1"] = _read_uint8(f); e["u2"] = _read_uint8(f)
            e["resource_key"] = _read_uint32(f)
            e["u3"] = _read_float(f); e["u4"] = _read_float(f)
            e["u3b"] = _read_bytes(f,5)  # raw 5 bytes (ubit40)
            e["u5"] = _read_float(f); e["u6"] = _read_float(f); e["u7"]=_read_float(f); e["u8"]=_read_float(f); e["u9"]=_read_float(f)
            sec5["entry"].append(e)
        effdir["sec"][5] = sec5

        # Section 6
        sec6 = {"n_entries": _read_uint32(f), "entry":[]}
        for _ in range(sec6["n_entries"]):
            e = {}
            e["u1"] = _read_uint16(f)
            str_rep = _read_uint32(f); e["str_rep"] = str_rep
            e["str"] = f.read(str_rep).decode("latin1", errors="ignore") if str_rep>0 else ""
            e["type_id"] = _read_uint8(f)
            sec6["entry"].append(e)
        effdir["sec"][6] = sec6

        # Section 7
        sec7 = {"n_entries": _read_uint32(f), "entry":[]}
        for _ in range(sec7["n_entries"]):
            e = {}
            e["u1_raw"] = _read_bytes(f,22)  # raw 22 bytes
            e["u2"] = _read_float(f)
            e["u3"] = _read_uint32(f); e["u4"] = _read_uint32(f)
            e["u5"] = _read_bytes(f,8)
            e["u6"] = _read_float(f); e["u7"] = _read_float(f); e["u8"]= _read_float(f); e["u9"]= _read_float(f)
            e["u10"] = _read_uint32(f); e["u11"] = _read_uint32(f); e["u12"] = _read_uint32(f)
            sec7["entry"].append(e)
        effdir["sec"][7] = sec7

        # Section 8
        sec8 = {"n_entries": _read_uint32(f), "entry":[]}
        for _ in range(sec8["n_entries"]):
            e = {}
            e["u1"] = _read_uint16(f)
            u2_rep = _read_uint32(f); e["u2_rep"]=u2_rep
            e["u2"] = []
            for __ in range(u2_rep):
                sub = {}
                sub["u1"] = _read_float(f)
                sub["u2"] = _read_float(f)
                srep = _read_uint32(f)
                sub["str_rep"] = srep
                sub["str"] = f.read(srep).decode("latin1", errors="ignore") if srep>0 else ""
                e["u2"].append(sub)
            e["u3"] = _read_uint32(f)
            sec8["entry"].append(e)
        effdir["sec"][8] = sec8

        # Section 9
        sec9 = {"n_entries": _read_uint32(f), "entry":[]}
        for _ in range(sec9["n_entries"]):
            e = {}
            e["u1"] = _read_bytes(f,6)  # raw 6 bytes
            e["sound_resource_key"] = _read_uint32(f)
            e["u2"] = _read_float(f)
            e["u3"] = _read_float(f)
            sec9["entry"].append(e)
        effdir["sec"][9] = sec9

        # Section 10
        sec10 = {"n_entries": _read_uint32(f), "entry":[]}
        for _ in range(sec10["n_entries"]):
            e = {"u1":_read_float(f), "u2":_read_float(f), "u3":_read_float(f)}
            sec10["entry"].append(e)
        sec10["eos"] = _read_uint16(f)
        effdir["sec"][10] = sec10

        # Section 11
        sec11 = {"n_entries": _read_uint32(f), "entry":[]}
        for _ in range(sec11["n_entries"]):
            e = {}
            e["u1"] = _read_uint32(f)
            srep = _read_uint32(f); e["str_rep"] = srep
            e["str"] = f.read(srep).decode("latin1", errors="ignore") if srep>0 else ""
            e["u2"] = _read_uint32(f); e["u3"] = _read_uint32(f); e["u4"]=_read_uint32(f)
            e["u5"] = _read_float(f); e["u6"] = _read_float(f); e["u7"] = _read_float(f)
            e["u8"] = _read_float(f); e["u9"] = _read_float(f)
            sec11["entry"].append(e)
        sec11["eos"] = _read_uint16(f)
        effdir["sec"][11] = sec11

        # Section 12 (heavy)
        sec12 = {"n_entries": _read_uint32(f), "entry":[]}
        for _ in range(sec12["n_entries"]):
            ent = {}
            ent["u1"] = _read_uint32(f); ent["u2"] = _read_uint32(f)
            prim_rep = _read_uint32(f); ent["prim_indx_rep"] = prim_rep
            ent["prim_indx"] = []
            for __ in range(prim_rep):
                p = {}
                p["str_rep"] = _read_uint32(f)
                p["str"] = f.read(p["str_rep"]).decode("latin1",errors="ignore") if p["str_rep"]>0 else ""
                p["indx_flag"] = _read_uint8(f)
                p["u1"] = _read_float(f); p["u2"] = _read_float(f)
                p["u3a"] = _read_uint32(f); p["u3b"] = _read_uint32(f)
                p["u4"] = _read_float(f); p["u5"] = _read_float(f); p["u6"] = _read_float(f); p["u7"] = _read_float(f)
                p["u8"] = _read_float(f); p["u9"] = _read_float(f)
                p["xshift"] = _read_float(f); p["zshift"] = _read_float(f); p["yshift"] = _read_float(f)
                p["u10"] = _read_float(f)
                p["u11a"] = _read_bytes(f,5); p["u11b"] = _read_bytes(f,5)  # raw 5+5 = 10 bytes
                p["u12"] = _read_float(f); p["u13"] = _read_float(f); p["u14"] = _read_float(f); p["u15"] = _read_float(f)
                p["u16"] = _read_uint16(f); p["u17"] = _read_uint16(f)
                p["indx_key"] = _read_uint32(f)
                ent["prim_indx"].append(p)

            # secondary indices
            secidx_rep = _read_uint32(f); ent["sec_indx_rep"] = secidx_rep
            ent["sec_indx"] = []
            for __ in range(secidx_rep):
                s = {}
                s["u1"] = _read_uint32(f)
                s["str_rep"] = _read_uint32(f)
                s["str"] = f.read(s["str_rep"]).decode("latin1",errors="ignore") if s["str_rep"]>0 else ""
                s["u2"] = _read_uint32(f)
                s["index_key"] = _read_uint32(f)
                ent["sec_indx"].append(s)

            ent["u3"] = _read_uint32(f); ent["u4"] = _read_uint32(f); ent["u5"] = _read_uint32(f); ent["u6"] = _read_uint32(f)
            sec12["entry"].append(ent)
        effdir["sec"][12] = sec12

        # Section 13
        sec13 = {"entry":[]}
        # MATLAB uses sec12.n_entries + 1 loop
        for __ in range(effdir["sec"][12]["n_entries"] + 1):
            entry = {}
            entry["str_rep"] = _read_uint32(f)
            entry["str"] = f.read(entry["str_rep"]).decode("latin1",errors="ignore") if entry["str_rep"]>0 else ""
            entry["index_key"] = _read_uint32(f)
            sec13["entry"].append(entry)
        sec13["eos1"] = _read_uint8(f); sec13["eos2"] = _read_uint8(f)
        effdir["sec"][13] = sec13

        # Section 13.5
        sec135 = {}
        sec135["u1"] = _read_int8(f)
        sec135["u2"] = _read_uint32(f)
        for i in range(3,12):
            sec135[f"u{i}"] = _read_float(f)
        effdir["sec135"] = sec135

        # Section 14
        sec14 = {"n_entries": _read_uint32(f), "entry":[]}
        for _ in range(sec14["n_entries"]):
            s = {}
            s["str_rep"] = _read_uint32(f)
            s["str"] = f.read(s["str_rep"]).decode("latin1",errors="ignore") if s["str_rep"]>0 else ""
            s["group_prop"] = _read_uint32(f)
            s["instance_prop"] = _read_uint32(f)
            sec14["entry"].append(s)
        sec14["eos"] = _read_uint16(f)
        effdir["sec"][14] = sec14

        # Section 15
        sec15 = {"n_entries": _read_uint32(f), "entry":[]}
        for _ in range(sec15["n_entries"]):
            s = {}
            s["class_id"] = _read_uint32(f)
            s["str_rep"] = _read_uint32(f)
            s["str"] = f.read(s["str_rep"]).decode("latin1",errors="ignore") if s["str_rep"]>0 else ""
            sec15["entry"].append(s)
        effdir["sec"][15] = sec15

    return effdir

# If invoked directly for quick test:
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python read_effdir.py file.eff")
    else:
        d = read_effdir(sys.argv[1])
        print("Sections read:", list(d["sec"].keys()))
