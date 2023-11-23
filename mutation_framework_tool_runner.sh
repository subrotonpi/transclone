#!/bin/bash

# $1 = system directory
# $2 = language {java, c, cs, py}
# $3 = frameowkr install dir
# $4 = tool dir
# $5 = fragmnet type (function|block)
# $6 = tool runner directory
# $7 = minlines

cd /home/egk204/projects/transclone
source venv/bin/activate
# echo $pwd
PROJECT_ROOT=/home/egk204/projects/transclone

fclones=$(python3 transclone.py \
    --root $PROJECT_ROOT/ \
    --cuda False \
    --transcoder_path "" \
    --src_lang python \
    --tgt_lang java \
    --fragment_to_conv "" \
    --threshold 0 \
    --data $PROJECT_ROOT/storage \
    --subject_system /home/egk204/projects/MutationInjectionFramework/sotred/mutantbase \
    --src_gmn_path $PROJECT_ROOT/gmn/gmn_srcml_clcdsa.pt \
    --pairs $PROJECT_ROOT/storage/pairs.csv 2>&1 | tail -n 1) # can be done better here! 
echo $fclones
