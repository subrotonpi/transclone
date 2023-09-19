import os,sys, logging, shutil
from codegen_sources.model.translate import preprocess_system
from src.pair_creation import preprocess_files
from src.analysis import analyze_predictions
from gmn.run_inference_gmn import detect_clones
from pathlib import Path
import argparse

project_root = str(Path().absolute())
# print("project_root", project_root)
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
parser.add_argument("--subject_system", default= project_root+'/storage/systems/')
parser.add_argument('--root' , default=project_root+'/')
parser.add_argument('--src_gmn_path' , default= project_root+'/gmn/gmn_srcml_clcdsa.pt')
parser.add_argument("--pairs",default= project_root+'/storage/pairs.csv')
args = parser.parse_args()

args.systems_converted = args.root+'storage/systems_converted/'
logging.info(args)

#remove systems_converted content or create the folder
# if os.path.exists(args.systems_converted):
#     shutil.rmtree(args.systems_converted)
#     os.mkdir(args.systems_converted)
# else:
#     os.mkdir(args.systems_converted)
#preprocess_system
# preprocess_system(args, args.src_lang, args.tgt_lang)
logging.info('***saved in /storage/systems_converted***')
#preprocess_files
pairs = preprocess_files(args.systems_converted)
logging.info('***generated Pairs***')
#detect_clones
_, res_df = detect_clones(args)
logging.info('***saved in: storage/predictions***')
#analyze_predictions
# print(res_df.head())
_, fstring = analyze_predictions(args, res_df)
logging.info(fstring)