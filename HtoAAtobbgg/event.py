# ============================================================
#              Developed by Bapi Basak
#                    IISER Pune
#                   August 2026
# ============================================================


import awkward as ak

def event_mask(collections, trigger_mask=None, apply_bJet_tagger = False, **kwargs):

    jets = collections["Jet"]
    electrons = collections["Electron"]
    muons = collections["Muon"]
    photons = collections["Photon"]

    nJet = ak.num(jets)
    nEle = ak.num(electrons)
    nMuon = ak.num(muons)
    nPho = ak.num(photons)

    lepton_cut = (nEle + nMuon) >= 1
    photon_cut = nPho >= 2
    jet_cut = nJet >= 1

    bjet_cut = ak.any(jets.btagUParTAK4B > 0.0246, axis=1)   # loose WP
    mask = ak.ones_like(nJet, dtype=bool)
    cut_masks = {"all": mask}

    if trigger_mask is not None:
        mask = mask & trigger_mask
        cut_masks["trigger"] = mask

    mask = mask & lepton_cut
    cut_masks["lepton"] = mask
    mask = mask & photon_cut
    cut_masks["lepton_photon"] = mask
    mask = mask & jet_cut
    cut_masks["jet"] = mask

    # Extra b-tagging step
    if apply_bJet_tagger:
        mask = mask & bjet_cut
    cut_masks["bJet"] = mask

    return mask, cut_masks