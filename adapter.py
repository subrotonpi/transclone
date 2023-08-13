import subprocess
from os import path

thispath = path.dirname(__file__)#str(Path(__file__))

import os,sys, logging
from codegen_sources.model.translate import convert_systems
from src.pair_creation import get_pairs
from gmn.run_inference_gmn import run
from pathlib import Path
project_root =str(Path())



def pinku(context, *args, **kwargs):
    #convert
	src = 'python'
	tgt = 'java'
    
	convert_systems(src, tgt)
	logging.info('***saved in /storage/systems_converted***')
 

 
	return output