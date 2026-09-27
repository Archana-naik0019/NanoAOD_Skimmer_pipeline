# ============================================================
#              Developed by Bapi Basak
#                    IISER Pune
#                   August 2026
# ============================================================


#!/usr/bin/env python3

import argparse
import json
import os
import subprocess
from pathlib import Path


# ============================================================
# Configuration
# ============================================================

DEFAULT_JSON = (
    "/eos/user/b/bbapi/"
    "My_Analysis/2024_efficiency_study/"
    "Backgrounds/configs/sample_BKG_2024.json"
)

EOS_BASE = (
    "/eos/user/b/bbapi/"
    "My_Analysis/2024_efficiency_study/"
    "Backgrounds/Skimmer"
)

EXECUTABLE = "run_skimmer.sh"

# EOS directory for Condor stdout/stderr/log files
CONDOR_LOG_BASE = (
    "root://eosuser.cern.ch//"
    "eos/user/b/bbapi/"
    "My_Analysis/2024_efficiency_study/"
    "Backgrounds/Skimmer/condor_logs"
)


# ============================================================
# Arguments
# ============================================================

parser = argparse.ArgumentParser(
    description="Submit one NanoAOD skimming job per ROOT file."
)

parser.add_argument(
    "--dataset",
    nargs="+",
    help=(
        "One or more dataset keys from the JSON file. "
        "Example: --dataset TTto2L2Nu TTtoLNu2Q TTG1Jets"
    )
)

parser.add_argument(
    "--all",
    action="store_true",
    help="Submit jobs for all datasets in the JSON file."
)

parser.add_argument(
    "--json",
    default=DEFAULT_JSON,
    help="Input JSON file."
)

parser.add_argument(
    "--retries",
    type=int,
    default=3,
    help="Number of retries inside run_skimmer.sh."
)

parser.add_argument(
    "--data",
    action="store_true",
    help="Run the skimmer in data mode (--apply_trigger --data)."
)

args = parser.parse_args()


# ============================================================
# Checks
# ============================================================

if args.retries < 1:
    raise ValueError("--retries must be >= 1")

if not os.path.isfile(EXECUTABLE):
    raise FileNotFoundError(
        f"Cannot find {EXECUTABLE}"
    )

if not os.path.isfile("nano_reduce.py"):
    raise FileNotFoundError(
        "Cannot find nano_reduce.py"
    )

if not os.path.isfile(args.json):
    raise FileNotFoundError(
        f"Cannot find JSON file: {args.json}"
    )

if args.dataset is None and not args.all:
    parser.error(
        "You must provide either --dataset or --all."
    )

if args.dataset is not None and args.all:
    parser.error(
        "Use either --dataset or --all, not both."
    )


# ============================================================
# Read JSON
# ============================================================

with open(args.json) as f:
    datasets = json.load(f)


# ============================================================
# Determine datasets to submit
# ============================================================

if args.all:

    selected_datasets = list(datasets.keys())

else:

    selected_datasets = args.dataset

    # Check that all requested datasets exist
    missing_datasets = [
        dataset
        for dataset in selected_datasets
        if dataset not in datasets
    ]

    if missing_datasets:

        print()
        print("ERROR: The following datasets were not found:")
        print()

        for dataset in missing_datasets:
            print(f"  {dataset}")

        print()
        print("Available datasets:")

        for dataset in datasets:
            print(f"  {dataset}")

        print()

        raise SystemExit(1)


# ============================================================
# Print global information
# ============================================================

print()
print("=" * 70)
print("NanoAOD Skimmer Condor Submission")
print("=" * 70)
print(f"JSON file       : {args.json}")
print(f"Datasets        : {len(selected_datasets)}")
print(f"Retries per job : {args.retries}")
print(f"Data mode       : {args.data}")
print()

for dataset in selected_datasets:
    print(f"  - {dataset}")

print("=" * 70)
print()


# ============================================================
# Function to submit one dataset
# ============================================================

def submit_dataset(dataset):

    print()
    print("-" * 70)
    print(f"Preparing dataset: {dataset}")
    print("-" * 70)

    # --------------------------------------------------------
    # Get input files
    # --------------------------------------------------------

    input_files = datasets[dataset]

    if not input_files:

        print(
            f"WARNING: Dataset '{dataset}' contains no files."
        )

        return False

    # --------------------------------------------------------
    # EOS output directory
    # --------------------------------------------------------

    eos_output_dir = (
        f"{EOS_BASE}/{dataset}"
    )

    os.makedirs(eos_output_dir, exist_ok=True)

    eos_output_remote = (
        "root://eosuser.cern.ch//"
        f"{eos_output_dir.lstrip('/')}"
    )

    # --------------------------------------------------------
    # Condor log directory
    # --------------------------------------------------------

    condor_log_dir = (
        f"{CONDOR_LOG_BASE}/{dataset}"
    )

    # --------------------------------------------------------
    # Local Condor directory
    # --------------------------------------------------------

    submit_dir = Path(
        f"condor_{dataset}"
    )

    submit_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # Print dataset information
    # --------------------------------------------------------

    print(
        f"Dataset          : {dataset}"
    )

    print(
        f"Number of files  : {len(input_files)}"
    )

    print(
        f"Retries per job  : {args.retries}"
    )

    print(
        f"EOS output       : {eos_output_remote}"
    )

    print(
        f"Condor logs      : {condor_log_dir}"
    )

    print(
        f"Submit directory : {submit_dir}"
    )

    # ========================================================
    # Create argument file
    # ========================================================

    argument_file = (
        submit_dir /
        "arguments.txt"
    )

    with open(argument_file, "w") as f:
        for input_file in input_files:

            data_flag = "1" if args.data else "0"

            f.write(
                f"{dataset} "
                f"{input_file} "
                f"{eos_output_remote} "
                f"{args.retries} "
                f"{data_flag}\n"
            )

    print(
        f"Argument file    : {argument_file}"
    )

    # ========================================================
    # Create Condor submit file
    # ========================================================

    submit_file = (
        submit_dir /
        "submit.sub"
    )

    with open(submit_file, "w") as f:

        # ----------------------------------------------------
        # Executable
        # ----------------------------------------------------

        f.write(
            f"executable = "
            f"{os.path.abspath(EXECUTABLE)}\n"
        )

        f.write(
            "arguments = $(ARGS)\n\n"
        )

        # ----------------------------------------------------
        # Condor stdout/stderr
        # ----------------------------------------------------

        f.write(
            f"output = "
            f"{dataset}.$(ClusterId).$(ProcId).out\n"
        )

        f.write(
            f"error = "
            f"{dataset}.$(ClusterId).$(ProcId).err\n"
        )

        f.write(
            f"log = "
            f"{submit_dir}/"
            f"{dataset}.$(ClusterId).log\n"
        )

        # ----------------------------------------------------
        # Send stdout/stderr to EOS
        # ----------------------------------------------------

        f.write(
            f"output_destination = "
            f"{condor_log_dir}\n\n"
        )

        # ----------------------------------------------------
        # Environment
        # ----------------------------------------------------

        f.write(
            "getenv = True\n"
        )

        f.write(
            "use_x509userproxy = true\n\n"
        )

        # ----------------------------------------------------
        # Resources
        # ----------------------------------------------------

        f.write(
            "request_cpus = 1\n"
        )

        f.write(
            "request_memory = 4096\n\n"
        )

        # ----------------------------------------------------
        # Job flavour
        # ----------------------------------------------------

        f.write(
            '+JobFlavour = "workday"\n\n'
        )

        # ----------------------------------------------------
        # Dataset identification
        # ----------------------------------------------------

        f.write(
            f'+SkimmerDataset = "{dataset}"\n\n'
        )

        # ----------------------------------------------------
        # Condor retry / hold behaviour
        # ----------------------------------------------------

        f.write(
            "on_exit_remove = "
            "(ExitBySignal == False) && "
            "(ExitCode == 0)\n"
        )

        f.write(
            "on_exit_hold = "
            "(ExitBySignal == True) || "
            "(ExitCode != 0)\n"
        )

        f.write(
            "periodic_hold = "
            "(JobStatus == 7) && "
            "((CurrentTime - EnteredCurrentStatus) > 300)\n"
        )

        f.write(
            'periodic_hold_reason = '
            '"Job stuck suspended >5m"\n'
        )

        f.write(
            "periodic_release = "
            "(JobStatus == 5) && "
            "((CurrentTime - EnteredCurrentStatus) > 60)\n"
        )

        f.write(
            "max_retries = 10\n"
        )

        f.write(
            "requirements = "
            "Machine =!= LastRemoteHost\n\n"
        )

        # ----------------------------------------------------
        # Transfer executable + nano_reduce.py + packages
        # ----------------------------------------------------

        f.write(
            "should_transfer_files = YES\n"
        )

        f.write(
            "when_to_transfer_output = ON_EXIT\n"
        )

        f.write(
            "transfer_input_files = "
            f"{os.path.abspath(EXECUTABLE)},"
            f"{os.path.abspath('nano_reduce.py')},"
            f"{os.path.abspath('core')},"
            f"{os.path.abspath('selection')}\n\n"
        )

        # ----------------------------------------------------
        # Queue
        # ----------------------------------------------------

        f.write(
            f"queue ARGS from {argument_file}\n"
        )

    print(
        f"Submit file     : {submit_file}"
    )

    # ========================================================
    # Submit using spool
    # ========================================================

    print()
    print(
        f"Submitting {len(input_files)} jobs..."
    )

    subprocess.run(
        [
            "condor_submit",
            "-spool",
            str(submit_file)
        ],
        check=True
    )

    print()
    print(
        f"Successfully submitted dataset: {dataset}"
    )

    return True


# ============================================================
# Submit all requested datasets
# ============================================================

successful_datasets = []
failed_datasets = []

for dataset in selected_datasets:

    try:

        success = submit_dataset(dataset)

        if success:
            successful_datasets.append(dataset)
        else:
            failed_datasets.append(dataset)

    except Exception as e:

        print()
        print(
            f"ERROR while submitting '{dataset}':"
        )

        print(
            f"  {e}"
        )

        failed_datasets.append(dataset)


# ============================================================
# Final summary
# ============================================================

print()
print("=" * 70)
print("SUBMISSION COMPLETE")
print("=" * 70)

print()
print(
    f"Datasets requested : {len(selected_datasets)}"
)

print(
    f"Datasets submitted : {len(successful_datasets)}"
)

print(
    f"Datasets failed    : {len(failed_datasets)}"
)

print()

if successful_datasets:

    print("Successfully submitted:")

    for dataset in successful_datasets:
        print(f"  ✓ {dataset}")

    print()


if failed_datasets:

    print("Failed:")

    for dataset in failed_datasets:
        print(f"  ✗ {dataset}")

    print()


print("=" * 70)
