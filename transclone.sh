#!/bin/bash
source venv/bin/activate

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
    --fragment_to_conv "" \
    --threshold 0 \
    --data $PROJECT_ROOT/storage \
    --subject_system $PROJECT_ROOT/storage/systems/config \
    --src_gmn_path $PROJECT_ROOT/gmn/gmn_srcml_clcdsa.pt \
    --pairs $PROJECT_ROOT/storage/pairs.csv 2>&1 | tee output.log