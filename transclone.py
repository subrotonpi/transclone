import os,sys, logging
from codegen_sources.model.translate import preprocess_system
from src.pair_creation import preprocess_files
from src.analysis import analyze_predictions
from gmn.run_inference_gmn import detect_clones
from pathlib import Path
import argparse

project_root =str(Path())
print(project_root)
parser = argparse.ArgumentParser()
parser.add_argument("--cuda", default=False)
#transcoder
parser.add_argument("--transcoder_path", type=str, default="")
parser.add_argument("--src_lang", type=str, default="python")
parser.add_argument("--tgt_lang",type=str, default="java")
parser.add_argument("--fragment_to_conv", type=str, default=None)
#srcml_gmn
parser.add_argument("--threshold", default=0)
parser.add_argument("--data", default=project_root+'/storage/')
parser.add_argument("--subject_system", default= project_root+'/storage/systems_converted')
parser.add_argument('--root' , default=project_root+'/')
parser.add_argument('--src_gmn_path' , default= project_root+'/gmn/gmn_srcml_clcdsa.pt')
parser.add_argument("--pairs",default= project_root+'/storage/pairs.csv')
args = parser.parse_args()
logging.info(args)
# quit()
#preprocess_system
preprocess_system(args, args.src_lang, args.tgt_lang)
logging.info('***saved in /storage/systems_converted***')
#preprocess_files
pairs = preprocess_files(args.subject_system)
logging.info('***generated Pairs***')
#detect_clones
_, res_df = detect_clones(args.subject_system, args.pairs, args)
logging.info('***saved in: storage/predictions***')
#analyze_predictions
print(res_df)
_, fstring = analyze_predictions(args, res_df)
logging.info(fstring)