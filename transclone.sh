#!/bin/bash
PROJECT_ROOT=$PWD
CUDA_FLAG=false
transcoder_path=""
SRC_LANG="python"
TGT_LANG="java"
FRAGMENT_TO_CONV=""
THRESHOLD=0
DATA_DIR=$PROJECT_ROOT/storage/
SUBJECT_SYSTEM_DIR=$PROJECT_ROOT/storage/system_converted
ROOT_DIR=$PROJECT_ROOT/
src_gmn_path=$PROJECT_ROOT/gmn/gmn_srcml_bcb.pt
PAIRS_FILE=$PROJECT_ROOT/storage/pairs.csv

# Function to display script usage
function display_usage() {
    echo "Usage: $0 [--cuda] [--transcoder_path <path>] [--src_lang <language>] [--tgt_lang <language>] [--fragment_to_conv <fragment>] [--threshold <value>] [--data <directory>] [--subject_system <directory>] [--root <directory>] [--src_gmn_path <path>] [--pairs <file>]"
}
display_usage
# Run the Python script
python gmn_pipeline.py \
    --cuda $CUDA_FLAG \
    --transcoder_path "$transcoder_path" \
    --src_lang "$SRC_LANG" \
    --tgt_lang "$TGT_LANG" \
    --fragment_to_conv "$FRAGMENT_TO_CONV" \
    --threshold $THRESHOLD \
    --data "$DATA_DIR" \
    --subject_system "$SUBJECT_SYSTEM_DIR" \
    --root "$ROOT_DIR" \
    --src_gmn_path "$src_gmn_path" \
    --pairs "$PAIRS_FILE"