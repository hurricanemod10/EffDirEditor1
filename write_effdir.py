# write_effdir.py
# Python translation of WriteEffDir.m (Sections 1-15)
# Defensive: tolerates missing fields and uses defaults.
# Usage:
#   from write_effdir import write_effdir
#   write_effdir(effdir_dict, "output.eff")

import struct
import os

def _u16(v): return struct.pack('<H', int(v) & 0xFFFF)
def _u32(v): return struct.pack('<I', int(v) & 0xFFFFFFFF)
def _f32(v): return struct.pack('<f', float(v))
def _bytes_of_int(v, length): return int(v).to_bytes(length, 'little', signed=False)

def _write_string_with_length(f, s):
    if s is None:
        f.write(_u32(0))
        return
    if isinstance(s, str):
        b = s.encode('utf-8')
    else:
        b = bytes(s)
    f.write(_u32(len(b)))
    if len(b) > 0:
        f.write(b)

def _write_raw_string_given_len(f, s, length):
    # Write exact number of bytes (no leading length) - used where MATLAB used fread(...,'*char') with known length
    if s is None:
        f.write(b'\x00' * length)
        return
    b = s.encode('utf-8')
    if len(b) < length:
        b = b + b'\x00' * (length - len(b))
    f.write(b[:length])

def _list_or_empty(x): return x if (x is not None) else []

def write_effdir(effdir, combfn):
    """
    effdir: dict with keys like 'init' (list of uint16s), 'sec' (list indexed 0..14 for sections 1..15)
    combfn: output filename
    """

    # sanity checks and defaults
    if combfn is None:
        raise ValueError("combfn (output filename) required")

    sec = effdir.get('sec', [{} for _ in range(15)])
    # ensure at least 15 sections exist as dicts
    while len(sec) < 15:
        sec.append({})

    # open file
    with open(combfn, 'wb') as f:
        # FILE HEADER: effdir.init is two uint16 values in original script
        init = effdir.get('init', [0, 0])
        if not isinstance(init, (list, tuple)):
            init = [init]
        for v in init:
            f.write(_u16(v))

        # ========== SECTION 1 ==========
        s1 = sec[0]
        n_entries = int(s1.get('n_entries', 0))
        f.write(_u32(n_entries))
        entries = s1.get('entries', [])
        # ensure length matches n_entries (defensive)
        for i in range(n_entries):
            entry = entries[i] if i < len(entries) else {}
            # Following MATLAB mapping: most fields are DWORD or float
            # Many fields in MATLAB comments map as uint32 or float32.
            # We'll prefer float for values flagged in comments as float (like velocities, delays).
            # But we will write them as uint32 if they're integer in your dict - using safe casting.

            # Example block following comments in the MAT file:
            # a series of DWORDs and floats; keep order consistent
            def w_u32(key, default=0):
                f.write(_u32(entry.get(key, default)))
            def w_f32(key, default=0.0):
                f.write(_f32(entry.get(key, default)))

            # start writing many fields — use keys from earlier examples
            w_u32('u1', 0)
            w_u32('u2_const_zero', 0)  # constant 0
            w_u32('u3', 0)
            w_f32('dur_min', 0.0)
            w_f32('dur_max', 0.0)
            w_f32('high_detail', 0.0)
            w_u32('loop', 0)
            w_f32('u4', 0.0)
            w_f32('u5', 0.0)
            w_f32('u6', 0.0)
            w_f32('delay_min', 0.0)
            w_f32('delay_max', 0.0)

            # push mins/maxs and velocity/shift values
            w_f32('x_axis_push_min', 0.0)
            w_f32('z_axis_push_min', 0.0)
            w_f32('y_axis_push_min', 0.0)
            w_f32('x_axis_push_max', 0.0)
            w_f32('z_axis_push_max', 0.0)
            w_f32('y_axis_push_max', 0.0)

            w_f32('init_vel_min', 0.0)
            w_f32('init_vel_max', 0.0)
            w_f32('initial_x_axis_shift_min', 0.0)
            w_f32('initial_z_axis_shift_min', 0.0)
            w_f32('initial_y_axis_shift_min', 0.0)
            w_f32('initial_x_axis_shift_max', 0.0)
            w_f32('initial_z_axis_shift_max', 0.0)
            w_f32('initial_y_axis_shift_max', 0.0)

            # initial variations
            w_f32('initial_size_varation_pc', 0.0)
            w_f32('initial_x_axis_stretch_max', 0.0)
            w_f32('initial_spin_variation_max', 0.0)
            w_f32('u7', 0.0)
            w_f32('initial_alpha_var_max', 0.0)
            w_f32('initial_color_var_pc_red', 0.0)
            w_f32('initial_color_var_pc_green', 0.0)
            w_f32('initial_color_var_pc_blue', 0.0)

            # dynamic arrays: color_adj_over_time (rgb triplets), brightness, size, x_shrink, spin
            # color_adj_over_time: write rep count then rep*3 floats
            color_adj = entry.get('color_adj_over_time', [])
            f.write(_u32(len(color_adj)))
            for rgb in color_adj:
                # each rgb expected like (r,g,b)
                r,g,b = (0.0,0.0,0.0)
                if isinstance(rgb, (list,tuple)) and len(rgb) >= 3:
                    r,g,b = float(rgb[0]), float(rgb[1]), float(rgb[2])
                f.write(_f32(r)); f.write(_f32(g)); f.write(_f32(b))

            # brightness over time
            bright = entry.get('bright_over_time', [])
            f.write(_u32(len(bright)))
            for v in bright:
                f.write(_f32(v))

            # size over time
            size_ot = entry.get('size_over_time', [])
            f.write(_u32(len(size_ot)))
            for v in size_ot:
                f.write(_f32(v))

            # x-axis shrink/stretch over time
            x_shrink = entry.get('x_shrink_over_time', [])
            f.write(_u32(len(x_shrink)))
            for v in x_shrink:
                f.write(_f32(v))

            # spin over time (reps then ints or floats)
            spin = entry.get('spin_over_time', [])
            f.write(_u32(len(spin)))
            for v in spin:
                # original had DWORD; write as uint32 if integer else float32 cast
                if isinstance(v, int):
                    f.write(_u32(v))
                else:
                    # cast float to uint32 representation - write as float32 for safety
                    f.write(_f32(float(v)))

            # main resource key (uint32)
            f.write(_u32(entry.get('main_resource_key', 0)))

            # two-byte value
            f.write(_u16(entry.get('u9', 0)))
            # u10 uint32
            f.write(_u32(entry.get('u10', 0)))

            # direction_travel_blur, x_force, y_force, z_force, carry, etc.
            w_f32('direction_travel_blur', 0.0)
            w_f32('x_force', 0.0)
            w_f32('y_force', 0.0)
            w_f32('z_force', 0.0)
            w_f32('carry', 0.0)

            # a bunch of u# floats (u11..u16)
            w_f32('u11', 0.0)
            w_f32('u12', 0.0)
            w_f32('u13', 0.0)
            w_f32('u14', 0.0)
            w_f32('u15', 0.0)

            # spiral travel pattern max
            w_f32('spiral_travel_pattern_max', 0.0)

            # u16 block: variable complex entries; write rep count then for each rep write four values as placeholder
            u16_rep = int(entry.get('u16_rep', 0))
            f.write(_u32(u16_rep))
            u16 = entry.get('u16', [])
            for j in range(u16_rep):
                sub = u16[j] if j < len(u16) else {}
                # using 64-bit fields as MATLAB used uint64 in example
                u1 = sub.get('u1', 0)
                u2 = sub.get('u2', 0)
                u3 = sub.get('u3', 0)
                u4 = sub.get('u4', 0)
                # pack as uint64, uint64, uint64, uint32
                f.write(_bytes_of_int(u1, 8))
                f.write(_bytes_of_int(u2, 8))
                f.write(_bytes_of_int(u3, 8))
                f.write(_u32(u4))

            # u17..u23 floats
            w_f32('u17', 0.0)
            w_f32('u18', 0.0)
            w_f32('u19', 0.0)
            w_f32('u20', 0.0)
            w_f32('u21', 0.0)
            w_f32('u22', 0.0)

            # u23 rep & values (float)
            u23 = entry.get('u23', [])
            f.write(_u32(len(u23)))
            for v in u23:
                f.write(_f32(v))

            # u24..u33 floats (a sequence)
            for k in range(24, 34):
                w_f32(f'u{k}', 0.0)

            # u34 string with length
            _write_string_with_length(f, entry.get('u34_str', None))
            # u35..u48 floats
            for k in range(35, 49):
                w_f32(f'u{k}', 0.0)

            # u49 rep & floats
            u49 = entry.get('u49', [])
            f.write(_u32(len(u49)))
            for v in u49:
                f.write(_f32(v))

            # u50, u51 floats
            w_f32('u50', 0.0)
            w_f32('u51', 0.0)

            # coordinate system for movement: rep then for each rep 8 floats
            coord_rep = int(entry.get('coord_syst_mvt_rep', 0))
            f.write(_u32(coord_rep))
            coord = entry.get('coord', {})
            # coord expected keys x1,y1,z1,x2,y2,z2,seq_num1,seq_num2 arrays
            for x in range(coord_rep):
                f.write(_f32(coord.get('x1', [0]*coord_rep)[x] if x < len(coord.get('x1', [])) else 0.0))
                f.write(_f32(coord.get('y1', [0]*coord_rep)[x] if x < len(coord.get('y1', [])) else 0.0))
                f.write(_f32(coord.get('z1', [0]*coord_rep)[x] if x < len(coord.get('z1', [])) else 0.0))
                f.write(_f32(coord.get('x2', [0]*coord_rep)[x] if x < len(coord.get('x2', [])) else 0.0))
                f.write(_f32(coord.get('y2', [0]*coord_rep)[x] if x < len(coord.get('y2', [])) else 0.0))
                f.write(_f32(coord.get('z2', [0]*coord_rep)[x] if x < len(coord.get('z2', [])) else 0.0))
                f.write(_f32(coord.get('seq_num1', [0]*coord_rep)[x] if x < len(coord.get('seq_num1', [])) else 0.0))
                f.write(_f32(coord.get('seq_num2', [0]*coord_rep)[x] if x < len(coord.get('seq_num2', [])) else 0.0))

            # u52 float
            w_f32('u52', 0.0)

            # u53: sub entries with string lengths and floats
            u53_rep = int(entry.get('u53_rep', 0))
            f.write(_u32(u53_rep))
            u53_str_rep = entry.get('u53_str_rep', [])
            u53_str = entry.get('u53_str', [])
            u53_u1 = entry.get('u53_u1', [])
            for y in range(u53_rep):
                rep_len = u53_str_rep[y] if y < len(u53_str_rep) else 0
                f.write(_u32(rep_len))
                if rep_len > 0:
                    s = u53_str[y] if y < len(u53_str) else ""
                    # write exactly rep_len chars
                    bs = s.encode('utf-8')
                    if len(bs) < rep_len:
                        bs = bs + b'\x00'*(rep_len - len(bs))
                    f.write(bs[:rep_len])
                # then float
                v = u53_u1[y] if y < len(u53_u1) else 0.0
                f.write(_f32(v))

            # u54, u55 floats
            w_f32('u54', 0.0)
            w_f32('u55', 0.0)

            # resource key rep and keys
            resource_key_rep = int(entry.get('resource_key_rep', 0))
            f.write(_u32(resource_key_rep))
            rkeys = entry.get('resource_key', [])
            for k in range(resource_key_rep):
                f.write(_u32(rkeys[k] if k < len(rkeys) else 0))

            # u56, u57 floats
            w_f32('u56', 0.0)
            w_f32('u57', 0.0)

            # u58 rep & floats
            u58_rep = int(entry.get('u58_rep', 0))
            f.write(_u32(u58_rep))
            u58 = entry.get('u58', [])
            for k in range(u58_rep):
                f.write(_f32(u58[k] if k < len(u58) else 0.0))

            # EOE uint32
            f.write(_u32(entry.get('eoe', 0x40800000)))  # default end-of-entry marker from comments

        # end of section 1: eos uint16
        f.write(_u16(s1.get('eos', 0x0001)))

        # ========== SECTION 2 ==========
        s2 = sec[1]
        n2 = int(s2.get('n_entries', 0))
        f.write(_u32(n2))
        entries2 = s2.get('entry', [])
        for i in range(n2):
            e = entries2[i] if i < len(entries2) else {}
            f.write(_u32(e.get('u1', 0)))
            f.write(_u32(e.get('resource_key', 0)))
            # bytes: inverse, repeat flags (uint8)
            f.write(struct.pack('<B', e.get('inverse_flg', 0)))
            f.write(struct.pack('<B', e.get('repeat_flg', 0)))
            f.write(_f32(e.get('speed', 0.0)))

            # rotation_over_time
            rot_rep = int(e.get('rotation_over_time_rep', 0))
            f.write(_u32(rot_rep))
            for v in e.get('rotation_over_time', [])[:rot_rep]:
                f.write(_f32(v))
            # size over time
            size_rep = int(e.get('size_over_time_rep', 0))
            f.write(_u32(size_rep))
            for v in e.get('size_over_time_pc', [])[:size_rep]:
                f.write(_f32(v))
            # alpha over time
            alpha_rep = int(e.get('alpha_over_time_rep', 0))
            f.write(_u32(alpha_rep))
            for v in e.get('alpha_over_time_pc', [])[:alpha_rep]:
                f.write(_f32(v))
            # color adj over time (rep then r,g,b floats)
            color_rep = int(e.get('color_adj_over_time_rep', 0))
            f.write(_u32(color_rep))
            for rgb in e.get('color_triplets', [])[:color_rep]:
                r,g,b = (0.0,0.0,0.0)
                if isinstance(rgb, (list,tuple)) and len(rgb) >= 3:
                    r,g,b = rgb[0], rgb[1], rgb[2]
                f.write(_f32(r)); f.write(_f32(g)); f.write(_f32(b))
            # y-axis stretch
            yrep = int(e.get('y_axis_stretch_over_time_rep', 0))
            f.write(_u32(yrep))
            for v in e.get('y_axis_stretch_over_time_pc', [])[:yrep]:
                f.write(_f32(v))
            # initial intensity/size var
            f.write(_f32(e.get('initial_intensity_var', 0.0)))
            f.write(_f32(e.get('initial_size_var', 0.0)))
            # u2..u5 floats
            f.write(_f32(e.get('u2', 0.0)))
            f.write(_f32(e.get('u3', 0.0)))
            f.write(_f32(e.get('u4', 0.0)))
            f.write(_f32(e.get('u5', 0.0)))
        # end of section2 eos
        f.write(_u16(s2.get('eos', 0x0000)))

        # ========== SECTION 3 ==========
        s3 = sec[2]
        f.write(_u32(int(s3.get('n_entries', 0))))
        for i in range(int(s3.get('n_entries', 0))):
            e = s3.get('entry', [])[i] if i < len(s3.get('entry', [])) else {}
            f.write(_f32(e.get('u1', 0.0)))
            f.write(_f32(e.get('u2', 0.0)))
            u3r = int(e.get('u3_rep', 0))
            f.write(_u32(u3r))
            for v in e.get('u3', [])[:u3r]:
                f.write(_f32(v))
            u4r = int(e.get('u4_rep', 0))
            f.write(_u32(u4r))
            for v in e.get('u4', [])[:u4r]:
                f.write(_f32(v))
            # 5 bytes u5/u6?
            f.write(_u16(e.get('u5', 0)))
            f.write(struct.pack('<B', e.get('u6', 0)))
            f.write(_u16(e.get('u7', 0)))
        f.write(_u16(s3.get('eos', 0x0000)))

        # ========== SECTION 4 ==========
        s4 = sec[3]
        f.write(_u32(int(s4.get('n_entries', 0))))
        for i in range(int(s4.get('n_entries', 0))):
            u1rep = int(s4.get('entry', [])[i].get('u1_rep', 0) if i < len(s4.get('entry', [])) else 0)
            f.write(_u32(u1rep))
            u1block = (s4.get('entry', [])[i].get('u1', {}) if i < len(s4.get('entry', [])) else {})
            for j in range(u1rep):
                f.write(_f32(u1block.get('u1', [0]*u1rep)[j] if j < len(u1block.get('u1', [])) else 0.0))
                f.write(_f32(u1block.get('u2', [0]*u1rep)[j] if j < len(u1block.get('u2', [])) else 0.0))
                f.write(_f32(u1block.get('u3', [0]*u1rep)[j] if j < len(u1block.get('u3', [])) else 0.0))
            u2rep = int(s4.get('entry', [])[i].get('u2_rep', 0) if i < len(s4.get('entry', [])) else 0)
            f.write(_u32(u2rep))
            for v in s4.get('entry', [])[i].get('u2', [])[:u2rep]:
                f.write(_f32(v))
            f.write(_f32(s4.get('entry', [])[i].get('u3', 0.0) if i < len(s4.get('entry', [])) else 0.0))
        # no explicit eos in your snippet

        # ========== SECTION 5 ==========
        s5 = sec[4]
        f.write(_u32(int(s5.get('n_entries', 0))))
        for i in range(int(s5.get('n_entries', 0))):
            e = s5.get('entry', [])[i] if i < len(s5.get('entry', [])) else {}
            # u1,u2 uint8
            f.write(struct.pack('<B', e.get('u1', 0)))
            f.write(struct.pack('<B', e.get('u2', 0)))
            f.write(_u32(e.get('resource_key', 0)))
            f.write(_f32(e.get('u3', 0.0)))
            f.write(_f32(e.get('u4', 0.0)))
            # 40-bit (5 bytes) - write as 5 raw bytes if provided as int
            u3b = e.get('u3b', 0)
            try:
                f.write(int(u3b).to_bytes(5, 'little'))
            except Exception:
                f.write(b'\x00'*5)
            f.write(_f32(e.get('u5', 0.0)))
            f.write(_f32(e.get('u6', 0.0)))
            f.write(_f32(e.get('u7', 0.0)))
            f.write(_f32(e.get('u8', 0.0)))
            f.write(_f32(e.get('u9', 0.0)))

        # ========== SECTION 6 ==========
        s6 = sec[5]
        f.write(_u32(int(s6.get('n_entries', 0))))
        for i in range(int(s6.get('n_entries', 0))):
            e = s6.get('entry', [])[i] if i < len(s6.get('entry', [])) else {}
            f.write(_u16(e.get('u1', 0)))
            str_rep = int(e.get('str_rep', 0))
            f.write(_u32(str_rep))
            if str_rep > 0:
                s = e.get('str', '')[:str_rep]
                # write exact number of chars
                bs = s.encode('utf-8')
                f.write(bs)
            f.write(struct.pack('<B', e.get('type_id', 0)))

        # ========== SECTION 7 ==========
        s7 = sec[6]
        f.write(_u32(int(s7.get('n_entries', 0))))
        for i in range(int(s7.get('n_entries', 0))):
            e = s7.get('entry', [])[i] if i < len(s7.get('entry', [])) else {}
            # complex bitfields (ubit58 etc) - write 8 bytes placeholders
            u1a = int(e.get('u1a', 0))
            u1b = int(e.get('u1b', 0))
            u1c = int(e.get('u1c', 0))
            # write 8 bytes each (placeholder)
            f.write(_bytes_of_int(u1a, 8))
            f.write(_bytes_of_int(u1b, 8))
            f.write(_bytes_of_int(u1c, 8))
            f.write(_f32(e.get('u2', 0.0)))
            f.write(_u32(e.get('u3', 0)))
            f.write(_u32(e.get('u4', 0)))
            f.write(_u32(e.get('u5', 0)))
            f.write(_u32(e.get('u5b', 0)))
            f.write(_f32(e.get('u6', 0.0)))
            f.write(_f32(e.get('u7', 0.0)))
            f.write(_f32(e.get('u8', 0.0)))
            f.write(_f32(e.get('u9', 0.0)))
            f.write(_u32(e.get('u10', 0)))
            f.write(_u32(e.get('u11', 0)))
            f.write(_u32(e.get('u12', 0)))

        # ========== SECTION 8 ==========
        s8 = sec[7]
        f.write(_u32(int(s8.get('n_entries', 0))))
        for i in range(int(s8.get('n_entries', 0))):
            e = s8.get('entry', [])[i] if i < len(s8.get('entry', [])) else {}
            f.write(_u16(e.get('u1', 0)))
            u2rep = int(e.get('u2_rep', 0))
            f.write(_u32(u2rep))
            u2 = e.get('u2', {})
            for j in range(u2rep):
                f.write(_f32(u2.get('u1', [0]*u2rep)[j] if j < len(u2.get('u1', [])) else 0.0))
                f.write(_f32(u2.get('u2', [0]*u2rep)[j] if j < len(u2.get('u2', [])) else 0.0))
                strlen = int(u2.get('str_rep', [0]*u2rep)[j] if j < len(u2.get('str_rep', [])) else 0)
                f.write(_u32(strlen))
                if strlen > 0:
                    s = u2.get('str', [""]*u2rep)[j]
                    bs = s.encode('utf-8')
                    if len(bs) < strlen:
                        bs = bs + b'\x00'*(strlen-len(bs))
                    f.write(bs[:strlen])
            f.write(_u32(e.get('u3', 0)))

        # ========== SECTION 9 ==========
        s9 = sec[8]
        f.write(_u32(int(s9.get('n_entries', 0))))
        for i in range(int(s9.get('n_entries', 0))):
            e = s9.get('entry', [])[i] if i < len(s9.get('entry', [])) else {}
            # u1 6 bytes - write 6 raw bytes if provided as int
            u1 = e.get('u1', 0)
            try:
                f.write(int(u1).to_bytes(6, 'little'))
            except Exception:
                f.write(b'\x00'*6)
            f.write(_u32(e.get('sound_resource_key', 0)))
            f.write(_f32(e.get('u2', 0.0)))
            f.write(_f32(e.get('u3', 0.0)))

        # ========== SECTION 10 ==========
        s10 = sec[9]
        f.write(_u32(int(s10.get('n_entries', 0))))
        for i in range(int(s10.get('n_entries', 0))):
            e = s10.get('entry', [])[i] if i < len(s10.get('entry', [])) else {}
            f.write(_f32(e.get('u1', 0.0)))
            f.write(_f32(e.get('u2', 0.0)))
            f.write(_f32(e.get('u3', 0.0)))
        f.write(_u16(s10.get('eos', 0x0001)))

        # ========== SECTION 11 ==========
        s11 = sec[10]
        f.write(_u32(int(s11.get('n_entries', 0))))
        for i in range(int(s11.get('n_entries', 0))):
            e = s11.get('entry', [])[i] if i < len(s11.get('entry', [])) else {}
            f.write(_u32(e.get('u1', 0)))
            str_rep = int(e.get('str_rep', 0))
            f.write(_u32(str_rep))
            if str_rep > 0:
                s = e.get('str', '')[:str_rep]
                f.write(s.encode('utf-8'))
            f.write(_u32(e.get('u2', 0)))
            f.write(_u32(e.get('u3', 0)))
            f.write(_u32(e.get('u4', 0)))
            f.write(_f32(e.get('u5', 0.0)))
            f.write(_f32(e.get('u6', 0.0)))
            f.write(_f32(e.get('u7', 0.0)))
            f.write(_f32(e.get('u8', 0.0)))
            f.write(_f32(e.get('u9', 0.0)))
        f.write(_u16(s11.get('eos', 0x0002)))

        # ========== SECTION 12 ==========
        s12 = sec[11]
        f.write(_u32(int(s12.get('n_entries', 0))))
        for i in range(int(s12.get('n_entries', 0))):
            e = s12.get('entry', [])[i] if i < len(s12.get('entry', [])) else {}
            f.write(_u32(e.get('u1', 0)))
            f.write(_u32(e.get('u2', 0)))
            prim_rep = int(e.get('prim_indx_rep', 0))
            f.write(_u32(prim_rep))
            prim = e.get('prim_indx', {})
            # prim_indx array
            for j in range(prim_rep):
                str_rep = int(prim.get('str_rep', [0]*prim_rep)[j] if j < len(prim.get('str_rep', [])) else 0)
                f.write(_u32(str_rep))
                if str_rep > 0:
                    s = prim.get('str', [""]*prim_rep)[j]
                    bs = s.encode('utf-8')
                    if len(bs) < str_rep:
                        bs = bs + b'\x00'*(str_rep-len(bs))
                    f.write(bs[:str_rep])
                f.write(struct.pack('<B', prim.get('indx_flag', [0]*prim_rep)[j] if j < len(prim.get('indx_flag', [])) else 0))
                # prim_indx.u1..u2 floats
                f.write(_f32(prim.get('u1', [0]*prim_rep)[j] if j < len(prim.get('u1', [])) else 0.0))
                f.write(_f32(prim.get('u2', [0]*prim_rep)[j] if j < len(prim.get('u2', [])) else 0.0))
                f.write(_u32(prim.get('u3a', [0]*prim_rep)[j] if j < len(prim.get('u3a', [])) else 0))
                f.write(_u32(prim.get('u3b', [0]*prim_rep)[j] if j < len(prim.get('u3b', [])) else 0))
                f.write(_f32(prim.get('u4', [0]*prim_rep)[j] if j < len(prim.get('u4', [])) else 0.0))
                f.write(_f32(prim.get('u5', [0]*prim_rep)[j] if j < len(prim.get('u5', [])) else 0.0))
                f.write(_f32(prim.get('u6', [0]*prim_rep)[j] if j < len(prim.get('u6', [])) else 0.0))
                f.write(_f32(prim.get('u7', [0]*prim_rep)[j] if j < len(prim.get('u7', [])) else 0.0))
                f.write(_f32(prim.get('u8', [0]*prim_rep)[j] if j < len(prim.get('u8', [])) else 0.0))
                f.write(_f32(prim.get('u9', [0]*prim_rep)[j] if j < len(prim.get('u9', [])) else 0.0))
                f.write(_f32(prim.get('xshift', [0]*prim_rep)[j] if j < len(prim.get('xshift', [])) else 0.0))
                f.write(_f32(prim.get('zshift', [0]*prim_rep)[j] if j < len(prim.get('zshift', [])) else 0.0))
                f.write(_f32(prim.get('yshift', [0]*prim_rep)[j] if j < len(prim.get('yshift', [])) else 0.0))
                f.write(_f32(prim.get('u10', [0]*prim_rep)[j] if j < len(prim.get('u10', [])) else 0.0))
                # u11a/u11b 40-bit fields -> write as 5 bytes each
                u11a = prim.get('u11a', [0]*prim_rep)[j] if j < len(prim.get('u11a', [])) else 0
                u11b = prim.get('u11b', [0]*prim_rep)[j] if j < len(prim.get('u11b', [])) else 0
                try:
                    f.write(int(u11a).to_bytes(5, 'little'))
                except Exception:
                    f.write(b'\x00'*5)
                try:
                    f.write(int(u11b).to_bytes(5, 'little'))
                except Exception:
                    f.write(b'\x00'*5)
                f.write(_f32(prim.get('u12', [0]*prim_rep)[j] if j < len(prim.get('u12', [])) else 0.0))
                f.write(_f32(prim.get('u13', [0]*prim_rep)[j] if j < len(prim.get('u13', [])) else 0.0))
                f.write(_f32(prim.get('u14', [0]*prim_rep)[j] if j < len(prim.get('u14', [])) else 0.0))
                f.write(_f32(prim.get('u15', [0]*prim_rep)[j] if j < len(prim.get('u15', [])) else 0.0))
                f.write(_u16(prim.get('u16', [0]*prim_rep)[j] if j < len(prim.get('u16', [])) else 0))
                f.write(_u16(prim.get('u17', [0]*prim_rep)[j] if j < len(prim.get('u17', [])) else 0))
                f.write(_u32(prim.get('indx_key', [0]*prim_rep)[j] if j < len(prim.get('indx_key', [])) else 0))

            # secondary indices block
            sec_rep = int(e.get('sec_indx_rep', 0))
            f.write(_u32(sec_rep))
            secidx = e.get('sec_indx', {})
            for k in range(sec_rep):
                f.write(_u32(secidx.get('u1', [0]*sec_rep)[k] if k < len(secidx.get('u1', [])) else 0))
                str_rep = int(secidx.get('str_rep', [0]*sec_rep)[k] if k < len(secidx.get('str_rep', [])) else 0)
                f.write(_u32(str_rep))
                if str_rep > 0:
                    s = secidx.get('str', [""]*sec_rep)[k]
                    bs = s.encode('utf-8')
                    if len(bs) < str_rep: bs = bs + b'\x00'*(str_rep-len(bs))
                    f.write(bs[:str_rep])
                f.write(_u32(secidx.get('u2', [0]*sec_rep)[k] if k < len(secidx.get('u2', [])) else 0))
                f.write(_u32(secidx.get('index_key', [0]*sec_rep)[k] if k < len(secidx.get('index_key', [])) else 0))

            f.write(_u32(e.get('u3', 0)))
            f.write(_u32(e.get('u4', 0)))
            f.write(_u32(e.get('u5', 0)))
            f.write(_u32(e.get('u6', 0)))

        # ========== SECTION 13 ==========
        s13 = sec[12] if len(sec) >= 13 else {}
        # NOTE: MATLAB used loop for sec12.n_entries+1 items
        n13 = int((sec[11].get('n_entries', 0) if 11 < len(sec) else 0) + 1)
        for i in range(n13):
            e = s13.get('entry', [])[i] if i < len(s13.get('entry', [])) else {}
            _write_string_with_length(f, e.get('str', None))
            f.write(_u32(e.get('index_key', 0)))
        # eos bytes for sec13 (two bytes)
        f.write(struct.pack('<B', s13.get('eos1', 0)))
        f.write(struct.pack('<B', s13.get('eos2', 0)))

        # ========== SECTION 13.5 ==========
        sec135 = effdir.get('sec135', {})
        if sec135:
            f.write(struct.pack('<b', int(sec135.get('u1', 0))))
            f.write(_u32(sec135.get('u2', 0)))
            for k in range(3, 12):  # u3..u11 floats
                f.write(_f32(sec135.get(f'u{k}', 0.0)))

        # ========== SECTION 14 ==========
        s14 = sec[13]
        f.write(_u32(int(s14.get('n_entries', 0))))
        for i in range(int(s14.get('n_entries', 0))):
            e = s14.get('entry', [])[i] if i < len(s14.get('entry', [])) else {}
            _write_string_with_length(f, e.get('str', None))
            f.write(_u32(e.get('group_prop', 0)))
            f.write(_u32(e.get('instance_prop', 0)))
        f.write(_u16(s14.get('eos', 0x0000)))

        # ========== SECTION 15 ==========
        s15 = sec[14]
        f.write(_u32(int(s15.get('n_entries', 0))))
        for i in range(int(s15.get('n_entries', 0))):
            e = s15.get('entry', [])[i] if i < len(s15.get('entry', [])) else {}
            f.write(_u32(e.get('class_id', 0)))
            _write_string_with_length(f, e.get('str', None))

    # file closed
    return True
