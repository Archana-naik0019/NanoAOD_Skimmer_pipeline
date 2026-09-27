import awkward as ak

def electron_mask(electrons):
    return ((electrons.pt > 25) & (abs(electrons.eta) < 2.5))

def muon_mask(muons):

    return ((muons.pt > 20) & (abs(muons.eta) < 2.4))

def photon_mask(photons, apply_pixelSeed=True):
    mask = ((photons.pt > 12) & (photons.isScEtaEB | photons.isScEtaEE))
    if apply_pixelSeed:
        mask = mask & (~photons.pixelSeed)
    return mask

def jet_mask(jets, apply_kinematic_cuts_jet=False):

    if apply_kinematic_cuts_jet:
        return ((jets.pt > 15) & (abs(jets.eta) < 2.4))
    return ak.ones_like(jets.pt, dtype=bool)
