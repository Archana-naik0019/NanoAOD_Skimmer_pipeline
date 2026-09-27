# NanoSkimmer

**Developed by Bapi Basak | IISER Pune | August 2026**

NanoSkimmer is a Python-based NanoAOD skimming framework designed to reduce CMS NanoAOD ROOT files by applying object-level and event-level selections while retaining the branches needed for analysis.

It uses **Uproot** and **Awkward Array** for ROOT I/O and event processing and supports both **MC** and **data** workflows. The package can also submit one Condor job per input ROOT file.

## Features

- Reads CMS NanoAOD ROOT files with Uproot.
- Uses Awkward Array for event and object manipulation.
- Supports Jet, Electron, Muon, Photon, MET, PV, GenPart and Flag collections.
- Configurable branch removal through `config.py` and `config_data.py`.
- Object-level selections for jets, electrons, muons and photons.
- Event-level selection and cutflow bookkeeping.
- Optional HLT trigger selection for data.
- Optional photon pixel-seed selection.
- Optional b-jet tagger selection.
- Optional jet kinematic cuts.
- Separate configurations for MC and data.
- Splits large skimmed outputs at `500000` events per file by default.
- Stores metadata including preselection event counts, MC generator-weight sums and cutflow information.
- High compression using LZMA.
- Condor submission support with automatic retries and EOS output verification.

## Directory Structure

```text
NanoSkimmer/
├── nano_reduce.py
├── run_skimmer.sh
├── submit_skimmer.py
│
├── core/
│   ├── __init__.py
│   ├── config.py
│   ├── config_data.py
│   ├── event_store.py
│   ├── reader.py
│   ├── reducer.py
│   └── writer.py
│
└── selection/
    ├── __init__.py
    ├── electron.py
    ├── event.py
    ├── jet.py
    ├── muon.py
    └── photon.py
```

### Main Components

**`nano_reduce.py`**  
Main command-line entry point. Selects the MC or data configuration, runs the reducer and writes the skimmed ROOT file.

**`core/reader.py` — `NanoReader`**  
Reads scalar branches, weight branches and NanoAOD collections from the `Events` tree.

**`core/reducer.py` — `NanoReducer`**  
Controls the complete reduction procedure: branch loading, branch removal, object selections, trigger selection and event selection.

**`core/event_store.py` — `EventStore`**  
Temporary container used to hold collections, scalar branches, weights, metadata and intermediate information during processing.

**`core/writer.py` — `NanoWriter`**  
Writes the selected events to ROOT using Uproot. It also creates a `Metadata` tree and handles output splitting.

**`selection/`**  
Contains the object and event selection functions.

**`core/config.py`**  
Configuration used for MC processing.

**`core/config_data.py`**  
Configuration used for data processing.

**`run_skimmer.sh`**  
Runs a single input ROOT file, retries failed processing/copy operations and copies the output to EOS.

**`submit_skimmer.py`**  
Creates and submits Condor jobs, one job per input ROOT file.

## Requirements

The code requires a Python environment containing at least:

```bash
python3
uproot
awkward
numpy
```

A CERN LCG environment is recommended when running on CERN infrastructure.

For example:

```bash
source /cvmfs/sft.cern.ch/lcg/views/LCG_109/x86_64-el9-gcc15-opt/setup.sh
```

Make sure the required Python packages are available in the environment.

## Local Usage

From inside the `NanoSkimmer` directory:

```bash
python3 nano_reduce.py --input input.root --output skim.root --config core/config.py
```

By default this uses the MC configuration.

### Process Data

```bash
python3 nano_reduce.py --input input.root --output skim.root --data --config core/config_data.py
```

### Apply the Data Trigger Selection

```bash
python3 nano_reduce.py --input input.root --output skim.root --data --apply_trigger --config core/config.py
```

### Optional Selections

Apply the photon pixel-seed selection:

```bash
python3 nano_reduce.py --input input.root --output skim.root --apply_pixelSeed --config core/config.py
```

Apply the b-jet tagger selection:

```bash
python3 nano_reduce.py --input input.root --output skim.root --apply_bJet_tagger --config core/config.py
```

Apply jet kinematic cuts:

```bash
python3 nano_reduce.py --input input.root --output skim.root --apply_kinematic_cuts_jet --config core/config.py
```

Multiple options can be combined:

```bash
python3 nano_reduce.py --input input.root --output skim.root --apply_pixelSeed --apply_bJet_tagger --config core/config.py
```

### Apply object selections

Individual selection stages can be enabled:

```bash
python3 nano_reduce.py --input input.root --output skim.root --apply-jet-selection --config core/config.py
```

Available options:

```text
--apply-jet-selection
--apply-electron-selection
--apply-muon-selection
--apply-photon-selection
--apply-event-selection
```

## Output ROOT File

The output contains two trees:

```text
Events
Metadata
```

### `Events`

Contains the selected scalar branches, collections and configured weights.

The temporary `__original_index__` branch is not written to the output.

### `Metadata`

Contains information associated with the original NanoAOD event range represented by each output file.

For MC, the metadata includes:

```text
n_events_presel
sum_genw_presel
```

Cutflow quantities are stored with names beginning with:

```text
cutflow_
```

The writer keeps track of the original NanoAOD event indices so that metadata refers to the corresponding range of the original input file rather than only the skimmed event count.

## Output Splitting

The default maximum number of skimmed events per output file is:

```python
MAX_EVENTS_PER_FILE = 500000
```

This is configured independently in:

```text
core/config.py
core/config_data.py
```

If the skim contains more than the configured number of events, the output is split automatically:

```text
skim_000.root
skim_001.root
skim_002.root
...
```

The final output file contains the remaining events.

## Configuration

The main configuration parameters are:

```python
MAX_EVENTS_PER_FILE
COLLECTIONS
SCALARS
HLT
WEIGHTS
DROP_FIELDS
```

### `COLLECTIONS`

Specifies which NanoAOD collections are read.

### `SCALARS`

Specifies scalar event-level branches to retain.

### `HLT`

Specifies trigger branches. These are used when:

```bash
--apply_trigger
```

is enabled.

### `WEIGHTS`

Specifies weight branches to retain, such as:

```text
PSWeight
LHEScaleWeight
LHEPdfWeight
```

### `DROP_FIELDS`

Specifies fields that should be removed from individual collections before writing the output.

This is useful for reducing output size by removing branches that are not needed for the analysis.

## Condor Workflow

For batch processing, the framework provides:

```text
run_skimmer.sh
submit_skimmer.py
```

### Single Condor Job

`run_skimmer.sh` takes:

```text
DATASET INPUT OUTPUT_DIR MAX_ATTEMPTS IS_DATA
```

Example:

```bash
./run_skimmer.sh MyDataset input.root root://eosuser.cern.ch//eos/user/b/bbapi/output 3 0
```

For data:

```bash
./run_skimmer.sh MyDataset input.root root://eosuser.cern.ch//eos/user/b/bbapi/output 3 1
```

The script:

1. Creates a temporary working directory.
2. Runs `nano_reduce.py`.
3. Checks that the local ROOT output exists and is non-empty.
4. Copies the output to EOS using `xrdcp`.
5. Verifies the EOS file using `xrdfs`.
6. Retries failed operations up to the requested number of attempts.

## Condor Submission

`submit_skimmer.py` reads a JSON file containing dataset names and their input ROOT files.

Example JSON structure:

```json
{
    "TTto2L2Nu": [
        "root://xrootd-cms.infn.it//path/to/file1.root",
        "root://xrootd-cms.infn.it//path/to/file2.root"
    ],
    "TTtoLNu2Q": [
        "root://xrootd-cms.infn.it//path/to/file3.root"
    ]
}
```

Submit selected datasets:

```bash
python3 submit_skimmer.py --dataset TTto2L2Nu TTtoLNu2Q
```

Submit all datasets:

```bash
python3 submit_skimmer.py --all
```

Specify a JSON file:

```bash
python3 submit_skimmer.py --dataset TTto2L2Nu --json samples.json
```

Set the number of retries:

```bash
python3 submit_skimmer.py --dataset TTto2L2Nu --retries 5
```

Submit in data mode:

```bash
python3 submit_skimmer.py --dataset DataSample --data
```

## Condor Job Behaviour

The submission script requests:

```text
CPUs    : 1
Memory  : 4096 MB
Flavour : workday
```

Input files transferred to the worker include:

```text
run_skimmer.sh
nano_reduce.py
core/
selection/
```

Condor stdout/stderr and logs are configured to be stored on EOS.

Jobs are held on non-zero exit codes or signals and include retry/hold logic to handle problematic jobs.

## Selection Flow

The basic processing sequence is:

```text
NanoAOD ROOT file
        │
        ▼
   NanoReader
        │
        ▼
 Read configured collections
        │
        ▼
 Remove unwanted fields
        │
        ▼
 Object selections
 (Jet/Electron/Muon/Photon)
        │
        ▼
 Trigger selection (optional)
        │
        ▼
 Event selection
        │
        ▼
   EventStore
        │
        ▼
     NanoWriter
        │
        ├──────────────► Events
        │
        └──────────────► Metadata
```

## Important Notes

- The input NanoAOD file must contain the branches requested by the selected configuration.
- MC processing expects `genWeight` when it is included in `config.SCALARS`.
- Data processing uses `config_data.py` and does not require MC generator weights.
- Trigger selection is only applied when `--apply_trigger` is explicitly enabled.
- The exact object and event selections are defined in the files under `selection/`.
- Before running large Condor campaigns, test the skimmer locally on a small number of files.

## Author

**Bapi Basak**  
**IISER Pune**  
**August 2026**
