import os
import pandas as pd
from itertools import combinations
import logging
import os
from pathlib import Path
project_root =str(Path())
FILE_EXTENSIONS=['java', 'py']
def get_pairs(d= project_root+'/storage/systems_converted'):
    x = []
    for (rt, dr, files) in os.walk(d, topdown=True):
            for file in files:
                if file.split('.')[-1] in FILE_EXTENSIONS:
                    tmp = os.path.join(rt, file)
                    #print(tmp[1:])
                    x.append(tmp[:])
                    #print(x)
    res = list(combinations(x, 2))
    #print("pairs : " + str(res))
    tmp = pd.DataFrame(res)
    tmp.to_csv(project_root+'/storage/pairs.csv', index=False, header=None)
    logging.info("****PAIRS SAVED IN-->"+project_root+"/storage/pairs.csv****")
    return tmp
def preprocess_files(p):
    get_pairs(p)
    
if __name__=="__main__":
    tmp = get_pairs(project_root+'/storage/systems_converted')
    