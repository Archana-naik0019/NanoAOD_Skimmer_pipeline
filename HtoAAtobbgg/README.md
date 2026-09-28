# H → AA → bbγγ Analysis Skimming

This directory contains the **analysis-specific skimming configuration** used for the **Higgs → AA → bbγγ** analysis.

The skimming pipeline processes input **NanoAOD ROOT files** and retains only the NanoAOD branches required by the analysis. The branches to be retained are specified separately for **MC** and **data** samples.

### Configuration Files

* **MC samples:** [`HtoAAtobbgg/config.py`](https://github.com/Bapi2X22/NanoAOD_Skimmer_pipeline/blob/main/HtoAAtobbgg/config.py)
* **Data samples:** [`HtoAAtobbgg/config_data.py`](https://github.com/Bapi2X22/NanoAOD_Skimmer_pipeline/blob/main/HtoAAtobbgg/config_data.py)

The resulting skimmed files contain **only the branches configured in the corresponding configuration file**.

---

## Object and Event Selection

In addition to NanoAOD branch pruning, the skimmer can apply **object-level selections** and **event-level selections**.

These selections are defined in:

* [`HtoAAtobbgg/object_selection.py`](https://github.com/Bapi2X22/NanoAOD_Skimmer_pipeline/blob/main/HtoAAtobbgg/object_selection.py)
* [`HtoAAtobbgg/event.py`](https://github.com/Bapi2X22/NanoAOD_Skimmer_pipeline/blob/main/HtoAAtobbgg/event.py)

The selections are enabled through command-line arguments passed to [`nano_reduce.py`](https://github.com/Bapi2X22/NanoAOD_Skimmer_pipeline/blob/main/nano_reduce.py).

### Available Selection Options

```text
--apply-jet-selection
--apply-electron-selection
--apply-muon-selection
--apply-photon-selection
--apply-event-selection
--apply-pixelSeed
--apply-bJet-tagger
--apply-trigger
```

The individual object selections can be enabled independently, allowing the skimmer to be used at different stages of the analysis workflow.

---

# How to Run

## 1. Interactive Run

The skimmer can be run interactively on a single ROOT file or a small test sample.

### 1.1 NanoAOD Branch Pruning Only

To run the skimmer **without applying any object or event selections** and only retain the branches specified in the configuration:

```bash
python3 nano_reduce.py \
    --input <input_file.root> \
    --output <output_file.root> \
    --config HtoAAtobbgg/config.py
```

---

### 1.2 Apply Photon Selection

To apply the photon selection defined in [`object_selection.py`](https://github.com/Bapi2X22/NanoAOD_Skimmer_pipeline/blob/main/HtoAAtobbgg/object_selection.py):

```bash
python3 nano_reduce.py \
    --input <input_file.root> \
    --output <output_file.root> \
    --config HtoAAtobbgg/config.py \
    --object_selection_file HtoAAtobbgg/object_selection.py \
    --apply-photon-selection
```

Similarly, the other object selections can be enabled using:

```text
--apply-jet-selection
--apply-electron-selection
--apply-muon-selection
```

---

### 1.3 Apply Object and Event Selection

To apply both object-level and event-level selections:

```bash
python3 nano_reduce.py \
    --input <input_file.root> \
    --output <output_file.root> \
    --config HtoAAtobbgg/config.py \
    --object_selection_file HtoAAtobbgg/object_selection.py \
    --apply-photon-selection \
    --event_selection_file HtoAAtobbgg/event.py \
    --apply-event-selection
```

The event-selection logic is defined in [`HtoAAtobbgg/event.py`](https://github.com/Bapi2X22/NanoAOD_Skimmer_pipeline/blob/main/HtoAAtobbgg/event.py).

---

### 1.4 Data Processing with HLT Selection

For **data**, use `config_data.py` and enable the data-specific configuration using the `--data` option.

Example:

```bash
python3 nano_reduce.py \
    --input <input_file.root> \
    --output <output_file.root> \
    --data \
    --config HtoAAtobbgg/config_data.py \
    --object_selection_file HtoAAtobbgg/object_selection.py \
    --apply-photon-selection \
    --event_selection_file HtoAAtobbgg/event.py \
    --apply-event-selection \
    --apply-trigger
```

When `--apply-trigger` is enabled, the skimmer applies the **logical OR of the trigger bits defined in `HtoAAtobbgg/config_data.py`**.

---

## Additional Selection Options

The following optional selections can also be enabled.

### Pixel Seed Veto

```bash
--apply-pixelSeed
```

### b-Jet Tagging

```bash
--apply-bJet-tagger
```

These options can be combined with the object and event selections described above.

---

# 2. HTCondor Submission

For large-scale processing, jobs can be submitted to **HTCondor** using `submit_skimmer.py`.

The datasets to be processed are specified in a JSON configuration file such as `samples.json`.

### Submit Selected Datasets

```bash
python3 submit_skimmer.py \
    --dataset <dataset_name> \
    --json samples.json
```

Here:

* `--dataset` specifies the dataset(s) to be processed.
* `--json` specifies the JSON file containing the dataset definitions.

For example:

```bash
python3 submit_skimmer.py \
    --dataset DYto2E50 \
    --json samples.json
```

---

# Important Notes

### Input Branches

The input NanoAOD files **must contain all branches requested by the selected configuration file**.

If a requested branch is missing from the input NanoAOD, the skimming process will fail.

### MC Samples

For MC processing, `genWeight` is required when it is included in:

```python
config.SCALARS
```

The corresponding generator-weight information is retained in the skimmed output.

### Data Samples

Data processing uses:

```text
HtoAAtobbgg/config_data.py
```

MC generator weights such as `genWeight` are **not required for data**.

### Trigger Selection

Trigger selection is **not applied by default**.

It is enabled explicitly using:

```bash
--apply-trigger
```

When enabled, the trigger selection uses the trigger paths configured in:

```text
HtoAAtobbgg/config_data.py
```

For multiple trigger paths, the selection corresponds to their **logical OR**.

### Cutflow and Metadata

Cutflow information for the HLT trigger and other event-selection requirements is stored in the:

```text
Metadata
```

TTree of the output ROOT file.

This allows the number of events surviving each selection step to be inspected after processing.

---

# Analysis Workflow

The overall workflow can be summarized as:

```text
                    Input NanoAOD
                          │
                          ▼
              ┌──────────────────────┐
              │   Configuration      │
              │                      │
              │  config.py (MC)      │
              │  config_data.py      │
              │  (Data)              │
              └──────────┬───────────┘
                         │
                         ▼
                Branch Selection
                         │
                         ▼
              ┌──────────────────────┐
              │ Object Selection     │
              │                      │
              │ • Jets               │
              │ • Electrons          │
              │ • Muons              │
              │ • Photons             │
              │ • b-Jet tagging      │
              │ • Pixel seed veto    │
              └──────────┬───────────┘
                         │
                         ▼
                Event Selection
                         │
                         ▼
                 Trigger Selection
                    (Data only)
                         │
                         ▼
                  Skimmed NanoAOD
                         │
                         ▼
                  Metadata / Cutflow
```

---

# Author

**Bapi Basak**
**IISER Pune**

*August 2026*

