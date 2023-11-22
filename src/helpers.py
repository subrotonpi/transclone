import pandas as pd
import re
def get_all_functions(xml_file):
    with open(xml_file, "r", encoding = "ISO-8859-1") as file:
        file_text = file.read()        
    results = []
    pattern = re.compile(r"<source.*?>(.|\n)*?<\/source>", re.MULTILINE)
    for match in pattern.finditer(file_text):
        grabbed_texts = file_text[match.start(): match.end()]
        sources = sources = re.finditer(r"<source.*?file=\"(.*?)\".*?startline=\"(.*?)\".*?endline=\"(.*?)\".*?>(.*?)<\/source>", grabbed_texts, re.DOTALL)        
        for source in sources:
            source_link = source.group(1)
            start_line = source.group(2)
            end_line = source.group(3)
            source_code = source.group(4)

            results.append([source_link, source_code, start_line, end_line]) 
               
    return pd.DataFrame(results,columns =["file_path","code", "start", "end"])
