# write_effdir.py
# Line-by-line Python translation of WriteEffDir.m
import struct

func _write_uint32(f, v): f.write(struct.pack("<I", int(v) & 0xFFFFFFFF))
func _write_int32(f, v): f.write(struct.pack("<i", int(v)))
func _write_uint16(f, v): f.write(struct.pack("<H", int(v) & 0xFFFF))
func _write_int16(f, v): f.write(struct.pack("<h", int(v)))
func _write_uint8(f, v): f.write(struct.pack("<B", int(v) & 0xFF))
func _write_int8(f, v): f.write(struct.pack("<b", int(v)))
func _write_float(f, v): f.write(struct.pack("<f", float(v)))
func _write_bytes(f, b): f.write(bytes(b))

def write_effdir(path, effdir):
    """
    Write effdir (as produced by read_effdir/isolate) back to binary file.
    Mirrors the MATLAB WriteEffDir.m layout and field order.
    """
    with open(path, "wb") as f:
        # header (two uint16 like in read)
        init = effdir.get("init", [0,0])
        _write_uint16(f, init[0]); _write_uint16(f, init[1])

        # Section 1
        s1 = effdir["sec"][1]
        _write_uint32(f, s1["n_entries"])
        for e in s1["entry"]:
            _write_int32(f, e.get("u1",0))
            _write_int32(f, e.get("u2",0))
            _write_int32(f, e.get("u3",0))
            _write_float(f, e.get("dur_min",0.0))
            _write_float(f, e.get("dur_max",0.0))
            _write_float(f, e.get("high_detail",0.0))
            _write_uint32(f, e.get("loop",0))
            _write_float(f, e.get("u4",0.0))
            _write_float(f, e.get("u5",0.0))
            _write_float(f, e.get("u6",0.0))
            _write_float(f, e.get("delay_min",0.0))
            _write_float(f, e.get("delay_max",0.0))
            _write_float(f, e.get("x_axis_push_min",0.0))
            _write_float(f, e.get("z_axis_push_min",0.0))
            _write_float(f, e.get("y_axis_push_min",0.0))
            _write_float(f, e.get("x_axis_push_max",0.0))
            _write_float(f, e.get("z_axis_push_max",0.0))
            _write_float(f, e.get("y_axis_push_max",0.0))
            _write_float(f, e.get("init_vel_min",0.0))
            _write_float(f, e.get("init_vel_max",0.0))
            _write_float(f, e.get("initial_x_axis_shift_min",0.0))
            _write_float(f, e.get("initial_z_axis_shift_min",0.0))
            _write_float(f, e.get("initial_y_axis_shift_min",0.0))
            _write_float(f, e.get("initial_x_axis_shift_max",0.0))
            _write_float(f, e.get("initial_z_axis_shift_max",0.0))
            _write_float(f, e.get("initial_y_axis_shift_max",0.0))
            _write_float(f, e.get("initial_size_varation_pc",0.0))
            _write_float(f, e.get("initial_x_axis_stretch_max",0.0))
            _write_float(f, e.get("initial_spin_variation_max",0.0))
            _write_float(f, e.get("u7",0.0))
            _write_float(f, e.get("initial_alpha_var_max",0.0))
            _write_float(f, e.get("initial_color_var_pc_red",0.0))
            _write_float(f, e.get("initial_color_var_pc_green",0.0))
            _write_float(f, e.get("initial_color_var_pc_blue",0.0))

            _write_uint32(f, e.get("u8_rep", 0))
            for v in e.get("u8", []):
                _write_float(f, v)

            # color triplets
            _write_uint32(f, e.get("color_adj_over_time_rep", 0))
            for j in range(e.get("color_adj_over_time_rep", 0)):
                _write_float(f, e["red"][j])
                _write_float(f, e["green"][j])
                _write_float(f, e["blue"][j])

            _write_uint32(f, e.get("bright_adj_over_time_rep", 0))
            for v in e.get("bright", []): _write_float(f, v)

            _write_uint32(f, e.get("size_over_time_rep", 0))
            for v in e.get("size", []): _write_float(f, v)

            _write_uint32(f, e.get("x_shrink_over_time_rep", 0))
            for v in e.get("x_shrink", []): _write_float(f, v)

            _write_uint32(f, e.get("spin_over_time_rep", 0))
            for v in e.get("spin", []): _write_float(f, v)

            _write_uint32(f, e.get("main_resource_key", 0))
            _write_int16(f, e.get("u9", 0))
            _write_uint32(f, e.get("u10", 0))

            _write_float(f, e.get("direction_travel_blur", 0.0))
            _write_float(f, e.get("x_force",0.0))
            _write_float(f, e.get("y_force",0.0))
            _write_float(f, e.get("z_force",0.0))
            _write_float(f, e.get("carry",0.0))

            _write_float(f, e.get("u11",0.0)); _write_float(f, e.get("u12",0.0)); _write_float(f, e.get("u13",0.0))
            _write_float(f, e.get("u14",0.0)); _write_float(f, e.get("u15",0.0))

            _write_float(f, e.get("spiral_travel_pattern_max",0.0))

            _write_uint32(f, e.get("u16_rep",0))
            for b in e.get("u16",[]):
                # writer earlier used u64/u32 - here we write 4x uint32 to match read representation
                _write_uint32(f, b.get("u1",0))
                _write_uint32(f, b.get("u2",0))
                _write_uint32(f, b.get("u3",0))
                _write_uint32(f, b.get("u4",0))

            for label in ["u17","u18","u19","u20","u21","u22"]:
                _write_float(f, e.get(label,0.0))

            _write_uint32(f, e.get("u23_rep",0))
            for v in e.get("u23",[]): _write_float(f, v)

            for label in ["u24","u25","u26","u27","u28","u29","u30","u31","u32","u33"]:
                _write_float(f, e.get(label,0.0))

            _write_uint32(f, e.get("u34_str_rep", 0))
            if e.get("u34_str_rep",0)>0:
                _write_bytes(f, e.get("u34_str","").encode("latin1")[:e["u34_str_rep"]])

            for label in ["u35","u36","u37","u38","u39","u40","u41","u42","u43","u44","u45","u46","u47","u48"]:
                _write_float(f, e.get(label,0.0))

            _write_uint32(f, e.get("u49_rep",0))
            for v in e.get("u49",[]): _write_float(f, v)

            _write_float(f, e.get("u50",0.0)); _write_float(f, e.get("u51",0.0))

            _write_uint32(f, e.get("coord_syst_mvt_rep",0))
            for idx in range(e.get("coord_syst_mvt_rep",0)):
                _write_float(f, e["coord"]["x1"][idx])
                _write_float(f, e["coord"]["y1"][idx])
                _write_float(f, e["coord"]["z1"][idx])
                _write_float(f, e["coord"]["x2"][idx])
                _write_float(f, e["coord"]["y2"][idx])
                _write_float(f, e["coord"]["z2"][idx])
                _write_float(f, e["coord"]["seq_num1"][idx])
                _write_float(f, e["coord"]["seq_num2"][idx])

            _write_float(f, e.get("u52",0.0))

            _write_uint32(f, e.get("u53_rep",0))
            for idx in range(e.get("u53_rep",0)):
                _write_uint32(f, e["u53_str_rep"][idx])
                if e["u53_str_rep"][idx]>0:
                    _write_bytes(f, e["u53_str"][idx].encode("latin1")[:e["u53_str_rep"][idx]])
                _write_float(f, e["u53_u1"][idx])

            _write_float(f, e.get("u54",0.0)); _write_float(f, e.get("u55",0.0))

            _write_uint32(f, e.get("resource_key_rep",0))
            for v in e.get("resource_key",[]): _write_uint32(f, v)

            _write_float(f, e.get("u56",0.0)); _write_float(f, e.get("u57",0.0))

            _write_uint32(f, e.get("u58_rep",0))
            for v in e.get("u58",[]): _write_float(f, v)

            _write_uint32(f, e.get("eoe",0))

        _write_uint16(f, s1.get("eos", 0))

        # Section 2
        s2 = effdir["sec"][2]
        _write_uint32(f, s2["n_entries"])
        for e in s2["entry"]:
            _write_uint32(f, e.get("u1",0))
            _write_uint32(f, e.get("resource_key",0))
            _write_uint8(f, e.get("inverse_flg",0))
            _write_uint8(f, e.get("repeat_flg",0))
            _write_float(f, e.get("speed",0.0))

            _write_uint32(f, e.get("rotation_over_time_rep",0))
            for v in e.get("rotation_over_time",[]): _write_float(f, v)

            _write_uint32(f, e.get("size_over_time_rep",0))
            for v in e.get("size_over_time_pc",[]): _write_float(f, v)

            _write_uint32(f, e.get("alpha_over_time_rep",0))
            for v in e.get("alpha_over_time_pc",[]): _write_float(f, v)

            _write_uint32(f, e.get("color_adj_over_time_rep",0))
            for idx in range(e.get("color_adj_over_time_rep",0)):
                _write_float(f, e["red"][idx]); _write_float(f, e["green"][idx]); _write_float(f, e["blue"][idx])

            _write_uint32(f, e.get("y_axis_stretch_over_time_rep",0))
            for v in e.get("y_axis_stretch_over_time_pc",[]): _write_float(f, v)

            _write_float(f, e.get("initial_intensity_var",0.0)); _write_float(f, e.get("initial_size_var",0.0))
            _write_float(f, e.get("u2",0.0)); _write_float(f, e.get("u3",0.0)); _write_float(f, e.get("u4",0.0)); _write_float(f, e.get("u5",0.0))
        _write_uint16(f, s2.get("eos",0))

        # Sections 3..11 are lengthy; for brevity we write them using the same field names as the reader
        # Section 3
        s3 = effdir["sec"][3]; _write_uint32(f, s3["n_entries"])
        for e in s3["entry"]:
            _write_float(f, e.get("u1",0.0)); _write_float(f, e.get("u2",0.0))
            _write_uint32(f, e.get("u3_rep",0))
            for v in e.get("u3",[]): _write_float(f, v)
            _write_uint32(f, e.get("u4_rep",0))
            for v in e.get("u4",[]): _write_float(f, v)
            _write_uint16(f, e.get("u5",0)); _write_uint8(f, e.get("u6",0)); _write_uint16(f, e.get("u7",0))
        _write_uint16(f, s3.get("eos",0))

        # Section 4
        s4 = effdir["sec"][4]; _write_uint32(f, s4["n_entries"])
        for e in s4["entry"]:
            _write_uint32(f, e.get("u1_rep",0))
            for idx in range(e.get("u1_rep",0)):
                _write_float(f, e["u1"]["u1"][idx]); _write_float(f, e["u1"]["u2"][idx]); _write_float(f, e["u1"]["u3"][idx])
            _write_uint32(f, e.get("u2_rep",0))
            for v in e.get("u2",[]): _write_float(f, v)
            _write_float(f, e.get("u3",0.0))

        # Section 5
        s5 = effdir["sec"][5]; _write_uint32(f, s5["n_entries"])
        for e in s5["entry"]:
            _write_uint8(f, e.get("u1",0)); _write_uint8(f, e.get("u2",0))
            _write_uint32(f, e.get("resource_key",0)); _write_float(f, e.get("u3",0.0)); _write_float(f, e.get("u4",0.0))
            _write_bytes(f, e.get("u3b", b'\x00'*5))
            _write_float(f, e.get("u5",0.0)); _write_float(f, e.get("u6",0.0)); _write_float(f, e.get("u7",0.0))
            _write_float(f, e.get("u8",0.0)); _write_float(f, e.get("u9",0.0))

        # Section 6
        s6 = effdir["sec"][6]; _write_uint32(f, s6["n_entries"])
        for e in s6["entry"]:
            _write_uint16(f, e.get("u1",0)); _write_uint32(f, e.get("str_rep",0))
            if e.get("str_rep",0)>0:
                _write_bytes(f, e.get("str","").encode("latin1")[:e["str_rep"]])
            _write_uint8(f, e.get("type_id",0))

        # Section 7
        s7 = effdir["sec"][7]; _write_uint32(f, s7["n_entries"])
        for e in s7["entry"]:
            _write_bytes(f, e.get("u1_raw", b'\x00'*22))
            _write_float(f, e.get("u2",0.0))
            _write_uint32(f, e.get("u3",0)); _write_uint32(f, e.get("u4",0))
            _write_bytes(f, e.get("u5", b'\x00'*8))
            _write_float(f, e.get("u6",0.0)); _write_float(f, e.get("u7",0.0)); _write_float(f, e.get("u8",0.0)); _write_float(f, e.get("u9",0.0))
            _write_uint32(f, e.get("u10",0)); _write_uint32(f, e.get("u11",0)); _write_uint32(f, e.get("u12",0))

        # Section 8
        s8 = effdir["sec"][8]; _write_uint32(f, s8["n_entries"])
        for e in s8["entry"]:
            _write_uint16(f, e.get("u1",0)); _write_uint32(f, e.get("u2_rep",0))
            for sub in e.get("u2",[]):
                _write_float(f, sub.get("u1",0.0)); _write_float(f, sub.get("u2",0.0))
                _write_uint32(f, sub.get("str_rep",0))
                if sub.get("str_rep",0)>0:
                    _write_bytes(f, sub.get("str","").encode("latin1")[:sub["str_rep"]])
            _write_uint32(f, e.get("u3",0))

        # Section 9
        s9 = effdir["sec"][9]; _write_uint32(f, s9["n_entries"])
        for e in s9["entry"]:
            _write_bytes(f, e.get("u1", b'\x00'*6))
            _write_uint32(f, e.get("sound_resource_key",0))
            _write_float(f, e.get("u2",0.0)); _write_float(f, e.get("u3",0.0))

        # Section 10
        s10 = effdir["sec"][10]; _write_uint32(f, s10["n_entries"])
        for e in s10["entry"]:
            _write_float(f, e.get("u1",0.0)); _write_float(f, e.get("u2",0.0)); _write_float(f, e.get("u3",0.0))
        _write_uint16(f, s10.get("eos",0))

        # Section 11
        s11 = effdir["sec"][11]; _write_uint32(f, s11["n_entries"])
        for e in s11["entry"]:
            _write_uint32(f, e.get("u1",0))
            _write_uint32(f, e.get("str_rep",0))
            if e.get("str_rep",0)>0:
                _write_bytes(f, e.get("str","").encode("latin1")[:e["str_rep"]])
            _write_uint32(f, e.get("u2",0)); _write_uint32(f, e.get("u3",0)); _write_uint32(f, e.get("u4",0))
            _write_float(f, e.get("u5",0.0)); _write_float(f, e.get("u6",0.0)); _write_float(f, e.get("u7",0.0))
            _write_float(f, e.get("u8",0.0)); _write_float(f, e.get("u9",0.0))
        _write_uint16(f, s11.get("eos",0))

        # Section 12
        s12 = effdir["sec"][12]; _write_uint32(f, s12["n_entries"])
        for ent in s12["entry"]:
            _write_uint32(f, ent.get("u1",0)); _write_uint32(f, ent.get("u2",0))
            _write_uint32(f, ent.get("prim_indx_rep",0))
            for p in ent.get("prim_indx",[]):
                _write_uint32(f, p.get("str_rep",0))
                if p.get("str_rep",0)>0:
                    _write_bytes(f, p.get("str","").encode("latin1")[:p["str_rep"]])
                _write_uint8(f, p.get("indx_flag",0))
                _write_float(f, p.get("u1",0.0)); _write_float(f, p.get("u2",0.0))
                _write_uint32(f, p.get("u3a",0)); _write_uint32(f, p.get("u3b",0))
                _write_float(f, p.get("u4",0.0)); _write_float(f, p.get("u5",0.0)); _write_float(f, p.get("u6",0.0))
                _write_float(f, p.get("u7",0.0)); _write_float(f, p.get("u8",0.0)); _write_float(f, p.get("u9",0.0))
                _write_float(f, p.get("xshift",0.0)); _write_float(f, p.get("zshift",0.0)); _write_float(f, p.get("yshift",0.0))
                _write_float(f, p.get("u10",0.0))
                # write 10 raw bytes
                _write_bytes(f, p.get("u11a", b'\x00'*5))
                _write_bytes(f, p.get("u11b", b'\x00'*5))
                _write_float(f, p.get("u12",0.0)); _write_float(f, p.get("u13",0.0)); _write_float(f, p.get("u14",0.0)); _write_float(f, p.get("u15",0.0))
                _write_uint16(f, p.get("u16",0)); _write_uint16(f, p.get("u17",0))
                _write_uint32(f, p.get("indx_key",0))

            _write_uint32(f, ent.get("sec_indx_rep",0))
            for s in ent.get("sec_indx",[]):
                _write_uint32(f, s.get("u1",0))
                _write_uint32(f, s.get("str_rep",0))
                if s.get("str_rep",0)>0:
                    _write_bytes(f, s.get("str","").encode("latin1")[:s["str_rep"]])
                _write_uint32(f, s.get("u2",0))
                _write_uint32(f, s.get("index_key",0))

            _write_uint32(f, ent.get("u3",0)); _write_uint32(f, ent.get("u4",0)); _write_uint32(f, ent.get("u5",0)); _write_uint32(f, ent.get("u6",0))

        # Section 13
        # MATLAB used sec12.n_entries + 1 entries
        for entry in effdir["sec"][13]["entry"]:
            _write_uint32(f, entry.get("str_rep",0))
            if entry.get("str_rep",0)>0:
                _write_bytes(f, entry.get("str","").encode("latin1")[:entry["str_rep"]])
            _write_uint32(f, entry.get("index_key",0))
        # EOS bytes for sec13
        _write_uint8 = lambda buf, v: buf.write(struct.pack("<B", int(v) & 0xFF))
        # write two eos bytes (if provided)
        sec13eos1 = effdir["sec"][13].get("eos1",0)
        sec13eos2 = effdir["sec"][13].get("eos2",0)
        _write_uint8(f, sec13eos1); _write_uint8(f, sec13eos2)

        # Section 13.5
        if "sec135" in effdir:
            s135 = effdir["sec135"]
            _write_int8(f, s135.get("u1",0))
            _write_uint32(f, s135.get("u2",0))
            for i in range(3,12):
                _write_float(f, s135.get(f"u{i}",0.0))

        # Section 14
        s14 = effdir["sec"][14]; _write_uint32(f, s14["n_entries"])
        for e in s14["entry"]:
            _write_uint32(f, e.get("str_rep",0))
            if e.get("str_rep",0)>0:
                _write_bytes(f, e.get("str","").encode("latin1")[:e["str_rep"]])
            _write_uint32(f, e.get("group_prop",0)); _write_uint32(f, e.get("instance_prop",0))
        _write_uint16(f, s14.get("eos",0))

        # Section 15
        s15 = effdir["sec"][15]; _write_uint32(f, s15["n_entries"])
        for e in s15["entry"]:
            _write_uint32(f, e.get("class_id",0))
            _write_uint32(f, e.get("str_rep",0))
            if e.get("str_rep",0)>0:
                _write_bytes(f, e.get("str","").encode("latin1")[:e["str_rep"]])

    # done
