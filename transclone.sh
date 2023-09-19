#!/bin/bash
PROJECT_ROOT=$PWD
# Function to display script usage
function display_usage() {
    echo "Usage: $0 [--cuda] [--transcoder_path <path>] [--src_lang <language>] [--tgt_lang <language>] [--fragment_to_conv <fragment>] [--threshold <value>] [--data <directory>] [--subject_system <directory>] [--root <directory>] [--src_gmn_path <path>] [--pairs <file>]"
}
display_usage

python3 transclone.py \
    --root $PROJECT_ROOT/ \
    --cuda False \
    --transcoder_path "" \
    --src_lang python \
    --tgt_lang java \
    --fragment_to_conv None \
    --threshold 0 \
    --data $PROJECT_ROOT/storage/ \
    --subject_system $PROJECT_ROOT/storage/systems/ \
    --src_gmn_path $PROJECT_ROOT/gmn/gmn_srcml_clcdsa.pt \
    --pairs $PROJECT_ROOT/storage/pairs.csv


# CUDA_FLAG=False
# TRANSCODER_PATH=./
# SRC_LANG="python"
# TGT_LANG="java"
# THRESHOLD=0
# DATA_DIR=$PROJECT_ROOT/storage/
# SUBJECT_SYSTEM_DIR=$PROJECT_ROOT/storage/system_converted/
# ROOT_DIR=$PROJECT_ROOT/
# SRC_GMN_PATH=$PROJECT_ROOT/gmn/gmn_srcml_clcdsa.pt
# PAIRS_FILE=$PROJECT_ROOT/storage/pairs.csv
# FRAGMENT_TO_CONV=./
# Run the Python script
# python3 transclone.py \
#     --cuda $CUDA_FLAG \
#     --transcoder_path $TRANSCODER_PATH \
#     --src_lang $SRC_LANG \
#     --tgt_lang $TGT_LANG \
#     --fragment_to_conv $FRAGMENT_TO_CONV \
#     --threshold $THRESHOLD \
#     --data $DATA_DIR \
#     --subject_system $SUBJECT_SYSTEM_DIR \
#     --root $ROOT_DIR \
#     --src_gmn_path $SRC_GMN_PATH \
#     --pairs $PAIRS_FILE
