# ============================================================
# For H to aa to 4 photons analysis
# ============================================================


MAX_EVENTS_PER_FILE = 500000

COLLECTIONS = [
    "Jet",
    "Photon",
    "Electron",
    #"Muon",
    "PuppiMET",
    #"PFMET",
    "PV",
    #"GenPart",
    #"Flag",
    #"GenVtx",
]

SCALARS = [
    "run",
    "luminosityBlock",
    "event",
    #"Rho_fixedGridRhoFastjetAll",
    "Rho_fixedGridRhoAll",
    #"Pileup_nPU",
]

HLT = [
    "HLT_Diphoton30_18_R9IdL_AND_HE_AND_IsoCaloId"
]

WEIGHTS = []


DROP_FIELDS = {
    '''
    "Jet": [
        "Jet_chMultiplicity",   
        "Jet_nConstituents",   
        "Jet_nElectrons",   
        "Jet_nMuons",   
        "Jet_nSVs",   
        "Jet_neMultiplicity",
        "Jet_electronIdx1",   
        "Jet_electronIdx2",   
        "Jet_muonIdx1",   
        "Jet_muonIdx2",   
        "Jet_svIdx1",   
        "Jet_svIdx2",   
        "Jet_hfadjacentEtaStripsSize",
        "Jet_hfcentralEtaStripSize",   
        "Jet_PNetRegPtRawCorr",   
        "Jet_PNetRegPtRawCorrNeutrino",   
        "Jet_PNetRegPtRawRes",   
        "Jet_UParTAK4RegPtRawCorr",   
        "Jet_UParTAK4RegPtRawCorrNeutrino",   
        "Jet_UParTAK4RegPtRawRes",  
        "Jet_UParTAK4V1RegPtRawCorr",   
        "Jet_UParTAK4V1RegPtRawCorrNeutrino",   
        "Jet_UParTAK4V1RegPtRawRes",   
        "Jet_area",   
        "Jet_btagDeepFlavB",   
        "Jet_btagDeepFlavCvB",   
        "Jet_btagDeepFlavCvL",   
        "Jet_btagDeepFlavQG",   
        "Jet_btagPNetB",   
        "Jet_btagPNetCvB",   
        "Jet_btagPNetCvL",   
        "Jet_btagPNetCvNotB",   
        "Jet_btagPNetQvG",   
        "Jet_btagPNetTauVJet",   
        "Jet_btagUParTAK4B",   
        "Jet_btagUParTAK4CvB",   
        "Jet_btagUParTAK4CvL",   
        "Jet_btagUParTAK4CvNotB",   
        "Jet_btagUParTAK4Ele",   
        "Jet_btagUParTAK4Mu",   
        "Jet_btagUParTAK4QvG",   
        "Jet_btagUParTAK4SvCB",   
        "Jet_btagUParTAK4SvUDG",   
        "Jet_btagUParTAK4TauVJet",   
        "Jet_btagUParTAK4UDG",   
        "Jet_btagUParTAK4probb",   
        "Jet_btagUParTAK4probbb",   
        "Jet_chHEF",      
        "Jet_hfEmEF",   
        "Jet_hfHEF",   
        "Jet_hfsigmaEtaEta",   
        "Jet_hfsigmaPhiPhi",   
        "Jet_mass",   
        "Jet_muEF",   
        "Jet_muonSubtrDeltaEta",   
        "Jet_muonSubtrDeltaPhi",   
        "Jet_muonSubtrFactor",
        "Jet_neHEF",     
        "Jet_puIdDisc",   
        "Jet_rawFactor"
    ],
    '''

    "PuppiMET": [
        "PuppiMET_covXX",
        "PuppiMET_covXY",
        "PuppiMET_covYY",
        "PuppiMET_phiUnclusteredDown",
        "PuppiMET_phiUnclusteredUp",
        "PuppiMET_ptUnclusteredDown",
        "PuppiMET_ptUnclusteredUp",
        "PuppiMET_significance",
        "PuppiMET_sumEt",
        "PuppiMET_sumPtUnclustered"

    ]

}
