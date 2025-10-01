"""
isolate_eff.py
--------------
Isolate a single effect from an EffDir structure.

Converted from original MATLAB script (IsolateEff.m).
"""

from copy import deepcopy


def isolate_eff(effdir, index, unique_effect_name):
    """
    Isolate one effect (from section 13) into a new EffDir structure.

    Parameters
    ----------
    effdir : EffDir object (from read_effdir)
    index : int
        Index of the effect in section 13 to isolate
    unique_effect_name : str
        New name for the isolated effect

    Returns
    -------
    neffdir : EffDir object
    """

    # --- Initialize a new EffDir ---
    neffdir = deepcopy(effdir)

    # Reset all sections to 0 entries but keep EOS
    for sec_num in range(1, 16):
        neffdir.sec[sec_num]["n_entries"] = 0
        neffdir.sec[sec_num]["entry"] = []
        if "eos" in effdir.sec[sec_num]:
            neffdir.sec[sec_num]["eos"] = effdir.sec[sec_num]["eos"]

    # Section 12: only 1 entry
    sec12_index_key = effdir.sec[13]["entry"][index]["index_key"] + 1
    neffdir.sec[12]["n_entries"] = 1
    neffdir.sec[12]["entry"] = [deepcopy(effdir.sec[12]["entry"][sec12_index_key])]

    # Section 13: only 1 effect + closing entry
    neffdir.sec[13]["entry"] = []
    effect_entry = deepcopy(effdir.sec[13]["entry"][index])
    effect_entry["index_key"] = 0
    effect_entry["str"] = unique_effect_name
    effect_entry["str_rep"] = len(unique_effect_name)
    neffdir.sec[13]["entry"].append(effect_entry)

    closing_entry = deepcopy(effdir.sec[13]["entry"][effdir.sec[12]["n_entries"]])
    neffdir.sec[13]["entry"].append(closing_entry)

    # --- Fix primary indices (loop similar to MATLAB switch-case) ---
    prim_indx = effdir.sec[12]["entry"][sec12_index_key]["prim_indx"]

    for i, flag in enumerate(prim_indx["indx_flag"]):
        sec_index_key = prim_indx["indx_key"][i]

        # Map section flag to real section number
        flag_map = {
            0: 1,
            1: 2,
            3: 4,
            4: 6,
            5: 7,
            6: 8,
            7: 9,
            8: 10,
            10: 11,
        }
        if flag in flag_map:
            sec_nr = flag_map[flag]

            neffdir.sec[sec_nr]["n_entries"] += 1
            if "entry" not in neffdir.sec[sec_nr]:
                neffdir.sec[sec_nr]["entry"] = []

            new_entry = deepcopy(effdir.sec[sec_nr]["entry"][sec_index_key + 1])
            neffdir.sec[sec_nr]["entry"].append(new_entry)

            # Update prim_indx to point to new entry index
            neffdir.sec[12]["entry"][0]["prim_indx"]["indx_key"][i] = (
                neffdir.sec[sec_nr]["n_entries"] - 1
            )

    return neffdir
