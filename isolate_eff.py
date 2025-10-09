func isolate_eff
# Translate of IsolateEff.m to Python, keeps logic and indexing
def isolate_eff(effdir, index, unique_effect_name):
    """
    effdir: dict from read_effdir
    index: integer index into sec(13).entry (MATLAB style, 1-based)
    unique_effect_name: string
    Returns neffdir (new isolated effdir)
    """
    # In MATLAB index likely 1-based; our Python translation preserves the same convention.
    # So index argument should be 1-based here.
    if "sec" not in effdir:
        raise ValueError("effdir missing 'sec'")

    # sec13 entry with given index
    sec13_entries = effdir["sec"][13]["entry"]
    if index < 1 or index > len(sec13_entries):
        raise IndexError("index out of range for sec13 entries")

    src_entry = sec13_entries[index-1]
    sec12_index_key = src_entry["index_key"] + 1  # MATLAB used +1 for indexing into sec(12).entry

    # initialize new effdir
    neffdir = {"sec": {}}
    neffdir["init"] = effdir.get("init", [0,0])
    if "sec135" in effdir:
        neffdir["sec135"] = effdir["sec135"]

    # set all sections n_entries=0 and copy eos if present
    for i in range(1,16):
        neffdir["sec"][i] = {"n_entries": 0}
        if i in effdir["sec"] and "eos" in effdir["sec"][i]:
            neffdir["sec"][i]["eos"] = effdir["sec"][i]["eos"]

    # copy sec13 eos bytes
    neffdir["sec"][13] = {}
    neffdir["sec"][13]["eos1"] = effdir["sec"][13].get("eos1",0)
    neffdir["sec"][13]["eos2"] = effdir["sec"][13].get("eos2",0)
    neffdir["sec"][12] = {}

    # new sec12 has 1 entry = the selected entry from original sec12
    sec12_entries = effdir["sec"][12]["entry"]
    if sec12_index_key - 1 < 0 or sec12_index_key - 1 >= len(sec12_entries):
        raise IndexError("sec12 index key out of range")
    neffdir["sec"][12]["n_entries"] = 1
    neffdir["sec"][12]["entry"] = [sec12_entries[sec12_index_key-1].copy()]

    # sec13: new has the chosen entry as entry(1), and also the closing entry (original sec13 last)
    neffdir["sec"][13]["entry"] = []
    new_entry = src_entry.copy()
    new_entry["index_key"] = 0
    new_entry["str"] = unique_effect_name
    new_entry["str_rep"] = len(unique_effect_name)
    neffdir["sec"][13]["entry"].append(new_entry)
    # append closing entry (MATLAB used effdir.sec(13).entry(effdir.sec(12).n_entries+1))
    closing_index = len(effdir["sec"][13]["entry"]) - 1
    neffdir["sec"][13]["entry"].append(effdir["sec"][13]["entry"][closing_index].copy())

    # Now copy primary-index referenced entries into new neffdir
    prim_indx = effdir["sec"][12]["entry"][sec12_index_key-1]["prim_indx"]
    prim_rep = effdir["sec"][12]["entry"][sec12_index_key-1]["prim_indx_rep"]
    # Ensure prim_indx is list of dicts
    for i in range(prim_rep):
        sec_flag = prim_indx[i]["indx_flag"]
        sec_index_key = prim_indx[i]["indx_key"]
        # mapping from flags to section numbers (as in your MATLAB switch)
        mapping = {0:1, 1:2, 3:4, 4:6, 5:7, 6:8, 7:9, 8:10, 10:11}
        if sec_flag not in mapping:
            # skip unknown/redirect flags
            continue
        sec_nr = mapping[sec_flag]
        # increment new section entry count and append the referenced entry (MATLAB used +1 shift)
        # original effdir sections are 1-based in MATLAB, Python lists are 0-based
        original_entries = effdir["sec"][sec_nr]["entry"]
        original_index = sec_index_key + 1  # MATLAB used +1 earlier; keep behavior consistent
        if original_index - 1 < 0 or original_index - 1 >= len(original_entries):
            # skip if out of range
            continue
        # ensure neffdir sec exists
        if "entry" not in neffdir["sec"][sec_nr]:
            neffdir["sec"][sec_nr]["entry"] = []
        neffdir["sec"][sec_nr]["n_entries"] = neffdir["sec"][sec_nr].get("n_entries",0) + 1
        # append the referenced entry (deep copy preferred)
        neffdir["sec"][sec_nr]["entry"].append(original_entries[original_index-1].copy())
        # update the prim_indx index key in new sec12 entry
        neffdir["sec"][12]["entry"][0]["prim_indx"][i]["indx_key"] = neffdir["sec"][sec_nr]["n_entries"] - 1

    return neffdir

# quick test usage when run directly
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 4:
        print("Usage: python isolate_eff.py effdir.pkl index newname")
    else:
        import pickle
        eff = None
        with open(sys.argv[1], "rb") as fh:
            eff = pickle.load(fh)
        neff = isolate_eff(eff, int(sys.argv[2]), sys.argv[3])
        with open("isolated.pkl", "wb") as fh:
            pickle.dump(neff, fh)
        print("Isolated OK -> isolated.pkl")
