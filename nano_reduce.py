# ============================================================
#              Developed by Bapi Basak
#                    IISER Pune
#                   August 2026
# ============================================================


import argparse

from core.reducer import NanoReducer
from core.writer import NanoWriter
import importlib.util

parser = argparse.ArgumentParser(
    description="Run NanoReducer on a NanoAOD ROOT file.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    epilog="""
Examples:
  python run.py --input input.root --output skim.root --config core/config.py

  python run.py --input input.root --config core/config_data.py --data
"""
)

parser.add_argument("--input", required=True)
parser.add_argument("--output", default="skim.root")

parser.add_argument(
    "--config",
    required=True,
    help="Path to the Python config file.",
)

parser.add_argument(
    "--object_selection_file",
    required=False,
    help="Path to the object selection file.",
)

parser.add_argument(
    "--event_selection_file",
    required=False,
    help="Path to the event selection file.",
)

parser.add_argument(
    "--apply-jet-selection",
    action="store_true",
    help="Apply jet selection.",
)

parser.add_argument(
    "--apply-electron-selection",
    action="store_true",
    help="Apply electron selection.",
)

parser.add_argument(
    "--apply-muon-selection",
    action="store_true",
    help="Apply muon selection.",
)

parser.add_argument(
    "--apply-photon-selection",
    action="store_true",
    help="Apply photon selection.",
)

parser.add_argument(
    "--apply-event-selection",
    action="store_true",
    help="Apply event selection.",
)

parser.add_argument(
    "--data",
    action="store_true",
    help="Process data instead of MC.",
)

parser.add_argument(
    "--apply_trigger",
    action="store_true",
    help="Apply the configured HLT trigger selection.",
)

parser.add_argument(
    "--apply_pixelSeed",
    action="store_true",
    help="Apply the pixelSeed selection on photons.",
)

parser.add_argument(
    "--apply_bJet_tagger",
    action="store_true",
    help="Apply the bJet_tagger selection.",
)

parser.add_argument(
    "--apply_kinematic_cuts_jet",
    action="store_true",
    help="Apply the bJet_tagger selection.",
)

#------added for H to aa to 4 photons----------
parser.add_argument(
    "--cut_4photons",
    action="store_true",
    help="Require at least 4 photons per event.",
)

parser.add_argument(
    "--cut_eta",
    action="store_true",
    help="Require the leading 4 photons to pass eta acceptance.",
)

parser.add_argument(
    "--cut_pixel_seed",
    action="store_true",
    help="Require the leading 4 photons to fail the pixelSeed veto.",
)

parser.add_argument(
    "--cut_pt",
    action="store_true",
    help="Require the leading 4 photons to pass pt > 12 GeV.",
)

parser.add_argument(
    "--apply_lumi_mask",
    action="store_true",
    help="Apply the Golden-JSON luminosity mask (data only).",
)

parser.add_argument(
    "--lumimask_json",
    default=None,
    help="Path to the Golden-JSON lumi mask file.",
)
#----------------------------------------------

args = parser.parse_args()

def load_config(config_path, module_name="user_config"):

    spec = importlib.util.spec_from_file_location(module_name, config_path)

    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load config: {config_path}")

    config = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(config)

    return config

config = load_config(args.config)

object_selection = None
event_selection = None

if args.object_selection_file:
    object_selection = load_config(args.object_selection_file, "object_selection")

if args.event_selection_file:
    event_selection = load_config(args.event_selection_file, "event_selection")

data_kind = "data" if args.data else "mc"


# --apply-event-selection is a convenience switch: it turns all four cuts on unless you're relying on the individual flags for finer control. Either path (the umbrella flag OR the individual flag) is enough to turn a given cut on.
cut_4photons = args.cut_4photons or args.apply_event_selection
cut_eta = args.cut_eta or args.apply_event_selection
cut_pixel_seed = args.cut_pixel_seed or args.apply_event_selection
cut_pt = args.cut_pt or args.apply_event_selection
apply_lumi_mask = args.apply_lumi_mask or args.apply_event_selection
'''
# no event-selection cuts applied
python run.py --input input.root --output skim_noselection.root --config core/config_data.py --data --apply_trigger

# all event-selection cuts applied
python run.py --input input.root --output skim_data.root --config core/config_data.py --data --apply_trigger --apply-event-selection

# eta and pixelSeed cuts stay OFF; only 4-photon + pt cuts applied
python run.py --input input.root --output skim_finegrained.root --config core/config_mc.py --apply-event-selection --cut_4photons --cut_pt

'''
#-----------------------------------------------------------------

store = NanoReducer(
    args.input,
    config=config,
    object_selection_config=object_selection,
    event_selection_config=event_selection,
    jet_selection=args.apply_jet_selection,
    electron_selection=args.apply_electron_selection,
    muon_selection=args.apply_muon_selection,
    photon_selection=args.apply_photon_selection,
    event_selection=args.apply_event_selection,
    apply_trigger=args.apply_trigger, 
    apply_pixelSeed=args.apply_pixelSeed,
    apply_bJet_tagger=args.apply_bJet_tagger,
    apply_kinematic_cuts_jet=args.apply_kinematic_cuts_jet,
    # ---- added for H to aa to 4 photons----
    cut_4photons=cut_4photons,
    cut_eta=cut_eta,
    cut_pixel_seed=cut_pixel_seed,
    cut_pt=cut_pt,
    apply_lumi_mask=apply_lumi_mask,
    lumimask_json=args.lumimask_json
).run()

NanoWriter(args.output, config=config, data_kind=data_kind).write(store)