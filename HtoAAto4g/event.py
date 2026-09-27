import numpy as np
import awkward as ak

from coffea.lumi_tools import LumiMask

GAP_BARREL_ETA = 1.4442
GAP_ENDCAP_ETA = 1.5660
MAX_ETA = 2.5

def get_lumi_mask(run, luminosityBlock, json_path):
    #Applies a Golden-JSON luminosity mask for Data events
    if json_path is None:
        return np.ones(len(run), dtype=bool)

    lumi_mask = LumiMask(json_path)
    return lumi_mask(run, luminosityBlock)

def event_mask(
    collections,
    trigger_mask=None,
    apply_bJet_tagger=None,
    cut_4photons=True,
    cut_eta=True,
    cut_pixel_seed=True,
    cut_pt=True,
    apply_lumi_mask=False,
    run=None,
    luminosityBlock=None,
    lumimask_json=None,
):
    photons = collections["Photon"]
    nPho = ak.num(photons, axis=1)

    mask = trigger_mask if trigger_mask is not None else ak.ones_like(nPho, dtype=bool)

    if apply_lumi_mask and run is not None and luminosityBlock is not None:
        lumi_mask = get_lumi_mask(
            ak.to_numpy(run), ak.to_numpy(luminosityBlock), lumimask_json
        )
        mask = mask & lumi_mask
    
    cut_masks = {}

    if cut_4photons:
        mask = mask & (nPho >= 4)
    cut_masks["4photons"] = mask

    photons_padded = ak.pad_none(photons, 4, axis=1)
    pho4 = photons_padded[:, :4]

    if cut_eta:
        abs_eta = np.abs(pho4.eta)
        eta_pass_each = (abs_eta < GAP_BARREL_ETA) | (
            (abs_eta > GAP_ENDCAP_ETA) & (abs_eta < MAX_ETA)
        )
        mask = mask & ak.fill_none(ak.all(eta_pass_each, axis=1), False)
    cut_masks["eta"] = mask

    if cut_pixel_seed:
        pixel_pass_each = pho4.pixelSeed == False
        mask = mask & ak.fill_none(ak.all(pixel_pass_each, axis=1), False)
    cut_masks["pixelSeed"] = mask

    if cut_pt:
        pt_pass_each = pho4.pt > 12.0
        mask = mask & ak.fill_none(ak.all(pt_pass_each, axis=1), False)
    cut_masks["pt_cuts"] = mask

    return mask, cut_masks
