# ============================================================
#              Developed by Bapi Basak
#                    IISER Pune
#                   August 2026
# ============================================================


MAX_EVENTS_PER_FILE = 500000

COLLECTIONS = [
    "Jet",
    "Photon",
    "Electron",
    "Muon",
    "PuppiMET",
    "PFMET",
    "PV",
    "GenPart",
    "Flag",
    "GenVtx",
]

SCALARS = [
    "run",
    "luminosityBlock",
    "event",
    "genWeight",
    "Rho_fixedGridRhoFastjetAll",
    "Rho_fixedGridRhoAll",
    "Pileup_nTrueInt",
    "Pileup_nPU",
]

HLT = []

WEIGHTS = [
    "PSWeight",
    # "LHEScaleWeight",
    # "LHEPdfWeight",
]

DROP_FIELDS = {
    "Jet": [
        "btagDeepFlavB",
        "btagPNetB",
        "btagDeepFlavCvL",
        "btagPNetCvNotB",
        "PNetRegPtRawRes",
        "btagPNetCvL",
        "btagPNetQvG",
        "puIdDisc",
        "muonSubtrFactor",
        "btagDeepFlavQG",
        "PNetRegPtRawCorr",
        "muonSubtrDeltaEta",
        "PNetRegPtRawCorrNeutrino",
        # "rawFactor",
        "muonSubtrDeltaPhi",
        "electronIdx1",
        "svIdx2",
        "electronIdx2",
        "muonIdx2",
        "hfcentralEtaStripSize",
        "hfsigmaEtaEta",
        "hfsigmaPhiPhi",
        "hfadjacentEtaStripsSize",
        "muonIdx1",
        "muonIdx2",
        "btagDeepFlavCvB", 
        "btagPNetCvB",
        "btagPNetTauVJet",
        "genJetIdx"
    ],

    "Photon": [
        "x_calo",
        "y_calo",
        "z_calo",
        "etaWidth",
        "pfChargedIsoWorstVtx",
        "pfChargedIsoPFPV",
        "phiWidth"
        "ecalPFClusterIso",
        "hcalPFClusterIso",
        "s4",
        "hoe_PUcorr",
        "hoe_Tower",
        "vidNestedWPBitmap",
        "esEnergyOverRawE",
        "esEffSigmaRR",
        "jetIdx",
        "haloTaggerMVAVal",
        # "seedGain",
        "electronIdx"
    ],

    "Electron": [
        "ecalEnergy",
        "scEtOverPt",
        "jetDF",
        "IPx",
        "IPy",
        "IPz",
        "eInvMinusPInv",
        "mvaNoIso",
        "ipLengthSig",
        "miniPFRelIso_all",
        "mvaHZZIso",
        "gsfTrketaMode",
        "gsfTrkphiMode",
        "ip3d",
        "ecalEnergyError",
        "fbrem",
        "sip3d",
        "promptMVA",
        "gsfTrkpMode"
        "jetRelIso",
        "gsfTrkpModeErr",
        "jetPtRelv2",
        "miniPFRelIso_chg",
        "dr03EcalRecHitSumEt",
        "dxyErr",
        "dzErr",
        "dr03HcalDepth1TowerSumEt",
        "vidNestedWPBitmapHEEP",
        "dr03TkSumPt",
        "vidNestedWPBitmap",
        "PreshowerEnergy",
        "jetNDauCharged",
        "photonIdx",
        "mvaNoIso_WP80",
        "mvaNoIso_WP90",
        "mvaIso_WPHZZ",
        "isEB",
        "isPFcand",
        "tightCharge",
        "isEcalDriven",
        "fsrPhotonIdx",
        "lostHits",
        "pnScore_prompt"
        # "seedGain"

    ],

    "Muon": [
        "VXBS_Cov00",
        "pnScore_tau",
        "pnScore_prompt",
        "bsConstrainedPt",
        "VXBS_Cov03",
        "pnScore_heavy",
        "VXBS_Cov33",
        "pnScore_light",
        "dxybs",
        "IPy",
        "IPz",
        "IPx",
        "ipLengthSig",
        "ip3d",
        "miniPFRelIso_all",
        "sip3d",
        "promptMVA",
        "segmentComp",
        "mvaLowPt",
        "jetRelIso",
        "jetDF",
        "jetPtRelv2",
        "bsConstrainedChi2",
        "miniPFRelIso_chg",
        "bsConstrainedPtErr",
        "ptErr",
        "tuneP_pterr",
        "dzErr",
        "tkRelIso",
        "dxyErr",
        "mvaMuID",
        "dxybsErr",
        "softMvaRun3",
        "softMva",
        "jetIdx",
        "jetNDauCharged",
        "nStations",
        "puppiIsoId",
        "miniIsoId",
        "tuneP_charge",
        "Muon_tkIsoId",
        "svIdx",
        "multiIsoId",
        "softMvaId",
        "mediumPromptId",
        "highPtId",
        "triggerIdLoose",
        "isPFcand",
        "isStandalone",
        "highPurity",
        "tunepRelPt",
        "bestTrackType",
        "fsrPhotonIdx",
        "tightCharge",
        "inTimeMuon",
    ],
    "PFMET": [
        # "ptUnclusteredDown",
        # "ptUnclusteredUp"
    ],
    "PuppiMET": [
        # "ptUnclusteredDown",
        # "ptUnclusteredUp"
    ],
    "PV": [
        "chi2"
        "ndof"
        "npvs"
        "npvsGood"
        "score"
        "sumpt2"
        "sumpx"
        "sumpy"
        "x"
        "y"
    ]
}

