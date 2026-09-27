#!/bin/bash

# ============================================================
#              Developed by Bapi Basak
#                    IISER Pune
#                   August 2026
# ============================================================

# ============================================================
# Arguments
# ============================================================

DATASET="$1"
INPUT="$2"
OUTPUT_DIR="$3"
MAX_ATTEMPTS="${4:-3}"
IS_DATA="${5:-0}"

# ============================================================
# Setup environment
# ============================================================

source /cvmfs/sft.cern.ch/lcg/views/LCG_109/x86_64-el9-gcc15-opt/setup.sh

export PYTHONPATH="$HOME/.local/lib/python3.13/site-packages/:$PYTHONPATH"
export PATH="$HOME/.local/bin/:$PATH"


# ============================================================
# Basic information
# ============================================================

BASENAME=$(basename "$INPUT" .root)

OUTPUT_REMOTE="${OUTPUT_DIR}/${BASENAME}_skim.root"

echo "============================================================"
echo "Dataset       : $DATASET"
echo "Input         : $INPUT"
echo "Output        : $OUTPUT_REMOTE"
echo "Max attempts  : $MAX_ATTEMPTS"
echo "============================================================"


# ============================================================
# Temporary working directory
# ============================================================

WORKDIR=$(mktemp -d)

cleanup()
{
    rm -rf "$WORKDIR"
}

trap cleanup EXIT


# ============================================================
# Retry loop
# ============================================================

for ((attempt=1; attempt<=MAX_ATTEMPTS; attempt++))
do

    echo
    echo "============================================================"
    echo "Attempt $attempt / $MAX_ATTEMPTS"
    echo "============================================================"


    # --------------------------------------------------------
    # Local output
    # --------------------------------------------------------

    OUTPUT_LOCAL="${WORKDIR}/${BASENAME}_skim.root"

    rm -f "$OUTPUT_LOCAL"


    # --------------------------------------------------------
    # Run skimmer
    # --------------------------------------------------------
    echo "Running nano_reduce.py..."

    if [ "$IS_DATA" = "1" ]; then
        CONFIG="core/config_data.py"
    else
        CONFIG="core/config.py"
    fi

    SKIMMER_ARGS=(
        --input "$INPUT"
        --output "$OUTPUT_LOCAL"
        --config "$CONFIG"
        --apply_pixelSeed
        --apply_bJet_tagger
        --apply-jet-selection
        --apply-electron-selection
        --apply-muon-selection
        --apply-photon-selection
        --apply-event-selection
    )

    if [ "$IS_DATA" = "1" ]; then
        SKIMMER_ARGS+=(
            --apply_trigger
            --data
        )
    fi

    if python3 nano_reduce.py "${SKIMMER_ARGS[@]}"
    then
        echo "nano_reduce.py completed successfully."
    else
        echo "ERROR: nano_reduce.py failed."


        if [ "$attempt" -lt "$MAX_ATTEMPTS" ]; then
            echo "Retrying in 10 seconds..."
            sleep 10
            continue
        fi

        echo "Maximum attempts reached."
        exit 1
    fi


    # --------------------------------------------------------
    # Check local output
    # --------------------------------------------------------

    if [ ! -s "$OUTPUT_LOCAL" ]; then

        echo "ERROR: Output file is missing or empty."

        if [ "$attempt" -lt "$MAX_ATTEMPTS" ]; then
            echo "Retrying in 10 seconds..."
            sleep 10
            continue
        fi

        echo "Maximum attempts reached."
        exit 1

    fi


    # --------------------------------------------------------
    # Copy output to EOS
    # --------------------------------------------------------

    echo "Copying output to EOS..."

    if xrdcp -f \
        "$OUTPUT_LOCAL" \
        "$OUTPUT_REMOTE"
    then

        echo "xrdcp completed successfully."

    else

        echo "ERROR: xrdcp failed."

        if [ "$attempt" -lt "$MAX_ATTEMPTS" ]; then
            echo "Retrying in 10 seconds..."
            sleep 10
            continue
        fi

        echo "Maximum attempts reached."
        exit 1

    fi


    # --------------------------------------------------------
    # Verify output on EOS
    # --------------------------------------------------------

    EOS_PATH="${OUTPUT_REMOTE#root://eosuser.cern.ch}"

    echo "Verifying EOS output..."

    if xrdfs root://eosuser.cern.ch stat "$EOS_PATH"
    then

        echo
        echo "============================================================"
        echo "JOB SUCCESS"
        echo "============================================================"
        echo "Dataset : $DATASET"
        echo "Input   : $INPUT"
        echo "Output  : $OUTPUT_REMOTE"
        echo "Attempt : $attempt"
        echo "============================================================"

        exit 0

    else

        echo "ERROR: EOS output verification failed."

        if [ "$attempt" -lt "$MAX_ATTEMPTS" ]; then
            echo "Retrying in 10 seconds..."
            sleep 10
            continue
        fi

        echo "Maximum attempts reached."
        exit 1

    fi

done


exit 1
