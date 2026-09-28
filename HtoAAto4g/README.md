This directory contains the skimming configurations to be used for the Higgs to AA to 4 photons analysis. It processes input NanoAOD files and retains only the subset of NanoAOD branches specified in [`HtoAAto4g/config_data.py`](https://github.com/Archana-naik0019/NanoAOD_Skimmer_pipeline/blob/main/HtoAAto4g/config_data.py) for data and in [`HtoAAto4g/config.py`](https://github.com/Archana-naik0019/NanoAOD_Skimmer_pipeline/blob/main/HtoAAto4g/config.py) for MC samples. All skimmed output files will contain exclusively these configured branches.
Additionally, a second tier of skimming is performed via [`HtoAAto4g/event.py`](https://github.com/Archana-naik0019/NanoAOD_Skimmer_pipeline/blob/main/HtoAAto4g/event.py) by applying:
- Lumi-based filtering (specific to data)
- High-Level Trigger (HLT) filtering (specific to data)
- Basic photon selection cuts (For both data and MC)
  ### Available Selection Options

```text
--cut_4photons
--cut_eta
--cut_pixel_seed
--cut_pt
--apply_lumi_mask
```

The individual event selections can be enabled independently.

## How to run

1. **Interactive Run**
  To run the skimmer interactively on a single ROOT file or a test sample, use the following command (this applies all the event selection cuts defined in [`HtoAAto4g/event.py`](https://github.com/Archana-naik0019/NanoAOD_Skimmer_pipeline/blob/main/HtoAAto4g/event.py)):
    ```bash
    python3 nano_reduce.py --input <input file name> --output <output file name> --apply_trigger --data --config HtoAAto4g/config_data.py --event_selection_file HtoAAto4g/event.py --apply-event-selection --apply_lumi_mask --lumimask_json <Golden.json file name>
    ```
  To run the skimmer while applying specific cuts from those defined in [`HtoAAto4g/event.py`](https://github.com/Archana-naik0019/NanoAOD_Skimmer_pipeline/blob/main/HtoAAto4g/event.py) :
   ```bash
   python3 nano_reduce.py --input <input file name> --output <output file name> --apply_trigger --data --config HtoAAto4g/config_data.py --event_selection_file HtoAAto4g/event.py --cut_4photons --cut_pt
   ```
 To run the skimmer while applying no event-selection cuts and only pruning the NanoAOD to drop unused branches:
  ```bash
   python3 nano_reduce.py --input <input file name> --output <output file name> --data --config HtoAAto4g/config_data.py
  ```
2. **Condor Submission**
  To submit jobs on HT Condor, use the script, use the following command:
   ```bash
    python3 submit_skimmer.py python3 submit_skimmer.py --dataset <specify the datasets from samples.json that are to be skimmed> --json <samples.json>
   ```
## Important Notes

- The input NanoAOD file must contain the branches requested by the selected configuration.
- MC processing expects `genWeight` when it is included in `config.SCALARS`.
- Data processing uses `config_data.py` and does not require MC generator weights.
- Trigger selection is only applied when `--apply_trigger` is explicitly enabled.
- The cutflow information for the HLT trigger and other event selection cuts is stored in the 'Metadata' TTree of the output file.

## Author
**Archana Naik**  
**IISER Pune**  
**August 2026**
