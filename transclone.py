import os,sys, logging, shutil
from codegen_sources.model.translate import preprocess_system_translate
from src.helpers import get_all_functions
from src.pair_creation import preprocess_files
from src.analysis import analyze_predictions
from gmn.run_inference_gmn import detect_clones
from pathlib import Path
import pandas as pd
import argparse
import subprocess

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

# #remove systems_converted content or create the folder
# if os.path.exists(args.systems_converted):
#     shutil.rmtree(args.systems_converted)
#     os.mkdir(args.systems_converted)
# else:
#     os.mkdir(args.systems_converted)
# #preprocess_system
def preprocess_system(subject_system, args):
    sys_name = subject_system.split("/")[-1]
    script_path = "nicad_function_extraction.sh"
    subprocess.run(["bash", script_path, sys_name])
    functions_java = get_all_functions(f"{args.data}/{sys_name}_functions_java.xml")
    functions_py = get_all_functions(f"{args.data}/{sys_name}_functions_py.xml")
    # print(functions_java.columns) 
    functions_java.to_csv(f"{args.data}/functions_java.csv", index=False)
    py_to_java =  preprocess_system_translate(args, functions_py)
    py_to_java.to_csv(f"{args.data}/py_to_java.csv", index=False)
    functions_py.to_csv(f"{args.data}/functions_py.csv", index=False)
    # print(py_to_java)
    return pd.concat([functions_java, py_to_java])
    
files = preprocess_system(args.subject_system, args)
logging.info('***transcoder phase done***')

# # #preprocess_files
# pairs = preprocess_files(args.systems_converted) #directory
pairs = preprocess_files(files) #functions
logging.info('***generated pairs***')
# #detect_clones
_, res_df = detect_clones(args)
logging.info('***saved in: storage/predictions***')
# #analyze_predictions
# # print(res_df.head())
_, fstring = analyze_predictions(args, res_df)
logging.info(fstring)


# /Path/to/File1.java,5,10,/Path/to/File2,20,25\