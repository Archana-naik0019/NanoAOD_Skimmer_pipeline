This skimmer processes input files and retains only the subset of NanoAOD branches (required for the H to AA to 4 photons analysis) specified in [`core/config_Data_updated.py`](https://github.com/Archana-naik0019/Skimmer_Higgs_to_AA_to_4photons/blob/main/core/config_Data_updated.py) for data and in [`core/config/updated.py`](https://github.com/Archana-naik0019/Skimmer_Higgs_to_AA_to_4photons/blob/main/core/config_updated.py) for MC samples. All skimmed output files will contain exclusively these configured branches.
Additionally, a second tier of skimming is performed via [`selection/event.py`](https://github.com/Archana-naik0019/Skimmer_Higgs_to_AA_to_4photons/blob/main/selection/event.py) by applying:
- Lumi-based filtering (specific to data)
- High-Level Trigger (HLT) filtering (specific to data)
- Basic photon selection cuts

#How to run

1. **Interactive Run**
  To run the skimmer interactively on a single ROOT file or a test sample, use the following command:
    ```bash
    python3 nano_reduce.py --input <input file name> --output <output file name> --apply_trigger --data --config HtoAAto4g/config_data.py --event_selection_file HtoAAto4g/event.py --apply-event-selection --lumimask_json <Golden.json file name>

2. **Condor Submission**
  To submit jobs on HT Condor, use the script, use the following command:
   ```bash
    python3 submit_skimmer.py python3 submit_skimmer.py --dataset <specify the datasets from samples.json that are to be skimmed> --json <samples.json>


