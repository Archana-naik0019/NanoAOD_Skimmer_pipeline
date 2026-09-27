# ============================================================
#              Developed by Bapi Basak
#                    IISER Pune
#                   August 2026
# ============================================================

import uproot
import awkward as ak

class NanoReader:

    def __init__(self, filename):
        self.tree = uproot.open(filename)["Events"]

    def drop_fields(self, obj, fields):
        for field in fields:
            if field in obj.fields:
                obj = ak.without_field(obj, field)
        return obj

    def read_scalar(self, branch):
        return self.tree[branch].array(library="ak")

    def read_weight(self, branch):
        return self.tree[branch].array(library="ak")

    def read(self, collection):
        branches = [b for b in self.tree.keys() if b.startswith(collection + "_")]
        arrays = self.tree.arrays(branches, library="ak")
        return ak.zip({b[len(collection)+1:]: arrays[b] for b in branches})
