# ============================================================
#              Developed by Bapi Basak
#                    IISER Pune
#                   August 2026
# ============================================================


from core.reader import NanoReader
from core.event_store import EventStore
import awkward as ak

class NanoReducer:

    def __init__(
        self,
        input_file,
        config,
        object_selection_config=None,
        event_selection_config=None,
        jet_selection=False,
        electron_selection=False,
        muon_selection=False,
        photon_selection=False,
        event_selection=False,
        apply_trigger=False,
        apply_pixelSeed=False,
        apply_bJet_tagger=False, 
        apply_kinematic_cuts_jet=False,
        # ---- added for H to aa to 4 photons----
        cut_4photons=False,
        cut_eta=False,
        cut_pixel_seed=False,
        cut_pt=False,
        apply_lumi_mask=False,
        lumimask_json=None
    ):

        self.reader = NanoReader(input_file)
        self.config = config

        # Optional object selection
        self.jet_mask = (object_selection_config.jet_mask if object_selection_config is not None else None)
        self.electron_mask = (object_selection_config.electron_mask if object_selection_config is not None else None)
        self.muon_mask = (object_selection_config.muon_mask if object_selection_config is not None else None)
        self.photon_mask = (object_selection_config.photon_mask if object_selection_config is not None else None)

        # Optional event selection
        self.event_mask = (event_selection_config.event_mask if event_selection_config is not None else None)

        self.jet_selection = jet_selection
        self.electron_selection = electron_selection
        self.muon_selection = muon_selection
        self.photon_selection = photon_selection
        self.event_selection = event_selection
        self.apply_trigger = apply_trigger
        self.apply_pixelSeed = apply_pixelSeed
        self.apply_bJet_tagger = apply_bJet_tagger
        self.apply_kinematic_cuts_jet = apply_kinematic_cuts_jet
        # ---- added for H to aa to 4 photons ----
        self.cut_4photons = cut_4photons
        self.cut_eta = cut_eta
        self.cut_pixel_seed = cut_pixel_seed
        self.cut_pt = cut_pt
        self.apply_lumi_mask = apply_lumi_mask
        self.lumimask_json = lumimask_json

    def run(self):

        collections = {}
        # Create store
        store = EventStore()
        event = self.reader.read_scalar("event")
        original_index = ak.local_index(event)
        # Number of events in the original NanoAOD
        store.add_temp("n_events_original", len(event))

        if "genWeight" in self.config.SCALARS:
            genWeight = self.reader.read_scalar("genWeight")
            store.add_temp("genWeight_original",genWeight)

        for collection in self.config.COLLECTIONS:
            print(f"Reading {collection}")
            obj = self.reader.read(collection)
            if collection in self.config.DROP_FIELDS:
                for field in self.config.DROP_FIELDS[collection]:
                    if field in obj.fields:
                        obj = ak.without_field(obj, field)

            if collection == "Jet" and self.jet_selection:
                if self.jet_mask is None:
                    raise ValueError("Jet selection requested, but no object_selection_file was provided.")
                obj = obj[self.jet_mask(obj, apply_kinematic_cuts_jet=self.apply_kinematic_cuts_jet)]

            if collection == "Electron" and self.electron_selection:
                if self.electron_mask is None:
                    raise ValueError("Electron selection requested, but no object_selection_file was provided.")
                obj = obj[self.electron_mask(obj)]

            if collection == "Muon" and self.muon_selection:
                if self.muon_mask is None:
                    raise ValueError("Muon selection requested, but no object_selection_file was provided.")
                obj = obj[self.muon_mask(obj)]

            if collection == "Photon" and self.photon_selection:
                if self.photon_mask is None:
                    raise ValueError("Photon selection requested, but no object_selection_file was provided.")
                obj = obj[self.photon_mask(obj, apply_pixelSeed=self.apply_pixelSeed)]

            collections[collection] = obj

        trigger_mask = None

        if self.apply_trigger:
            trigger_mask = ak.zeros_like(original_index, dtype=bool)
            for trigger in self.config.HLT:
                print(f"Reading trigger: {trigger}")
                value = self.reader.read_scalar(trigger)
                trigger_mask = trigger_mask | value

        if self.event_selection:
            is_data = "genWeight" not in self.config.SCALARS
            mask, cut_masks = self.event_mask(collections, trigger_mask = trigger_mask, apply_bJet_tagger=self.apply_bJet_tagger,
                #----added for H to aa to 4 photons analysis-------------
                cut_4photons=self.cut_4photons,
                cut_eta=self.cut_eta,
                cut_pixel_seed=self.cut_pixel_seed,
                cut_pt=self.cut_pt,
                apply_lumi_mask=(self.apply_lumi_mask and is_data),
                run=self.reader.read_scalar("run") if (self.apply_lumi_mask and is_data) else None,
                luminosityBlock=self.reader.read_scalar("luminosityBlock") if (self.apply_lumi_mask and is_data) else None,
                lumimask_json=self.lumimask_json)
            for name, cut_mask in cut_masks.items():
                store.add_temp(f"cutflow_{name}", cut_mask)
        else:
            if trigger_mask is not None:
                mask = trigger_mask
            else:
                mask = ak.ones_like( original_index, dtype=bool)

        store.add_scalar("__original_index__", original_index[mask])

        for name, obj in collections.items():
            store.add_collection(name, obj[mask])

        for branch in self.config.SCALARS:
            print(f"Reading {branch}")
            value = self.reader.read_scalar(branch)
            store.add_scalar(branch, value[mask])

        for branch in self.config.HLT:
            print(f"Reading {branch}")
            value = self.reader.read_scalar(branch)
            store.add_scalar(branch, value[mask])

        for branch in self.config.WEIGHTS:
            print(f"Reading {branch}")
            value = self.reader.read_weight(branch)
            store.add_weight(branch, value[mask])

        return store