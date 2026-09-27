# ============================================================
#              Developed by Bapi Basak
#                    IISER Pune
#                   August 2026
# ============================================================


import os

import awkward as ak
import numpy as np
import uproot

class NanoWriter:

    def __init__(self, filename, config, data_kind="mc"):
        self.filename = filename
        self.data_kind = data_kind
        self.config = config

    def write(self, store):
        MAX_EVENTS_PER_FILE = self.config.MAX_EVENTS_PER_FILE
        n_events_original = store.temp["n_events_original"]
        original_index = ak.to_numpy(store.scalars["__original_index__"])
        n_skim = len(original_index)

        if self.data_kind == "mc":
            genWeight_original = store.temp["genWeight_original"]

        # Determine skimmed split points
        if n_skim <= MAX_EVENTS_PER_FILE:
            split_points = []
        else:
            split_points = np.arange(MAX_EVENTS_PER_FILE, n_skim, MAX_EVENTS_PER_FILE)

        starts = np.concatenate((np.array([0]), split_points))
        stops = np.concatenate((split_points, np.array([n_skim])))

        # Original NanoAOD boundary
        original_start = 0

        for i, (start, stop) in enumerate(zip(starts, stops)):
            # Determine original event range
            if stop == n_skim:
                # Last output file includes all remaining original events
                original_stop = n_events_original
            else:
                # Find the original event corresponding to the last skimmed event in this file
                # +1 because Python slicing is [start:stop)
                original_stop = original_index[stop - 1] + 1

            branches = {}

            for name, array in store.scalars.items():
                if name == "__original_index__":
                    continue
                branches[name] = array[start:stop]

            for name, array in store.weights.items():
                branches[name] = array[start:stop]

            for name, collection in store.collections.items():
                branches[name] = collection[start:stop]

            metadata = {"n_events_presel": np.array([original_stop - original_start])}

            if self.data_kind == "mc":
                metadata["sum_genw_presel"] = np.array([float(ak.sum(genWeight_original[original_start:original_stop]))])

            # Cutflow metadata
            for name, cut_mask in store.temp.items():
                if not name.startswith("cutflow_"):
                    continue
                metadata[name] = np.array([int(ak.sum(cut_mask[original_start:original_stop]))])

            if len(starts) == 1:
                outfile = self.filename
            else:
                base, ext = os.path.splitext(self.filename)
                outfile = f"{base}_{i:03d}{ext}"

            with uproot.recreate(outfile, compression=uproot.LZMA(9)) as fout:
                events = fout.mktree("Events", {name: array.type for name, array in branches.items()})
                events.extend(branches)

                meta = fout.mktree("Metadata", {key: value.dtype for key, value in metadata.items()})
                meta.extend(metadata)

            print(f"Wrote {outfile} | skimmed events = {stop - start} | original events = {original_stop - original_start}")

            # Next output file starts at the original event
            original_start = original_stop
