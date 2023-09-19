import pandas as pd
# more to add
def analyze_predictions(args, res):
    # res = pd.read_csv("predictions.csv")
    data = {}
    t = len(res[res["prediction"]=="clone"])
    f = res.shape[0] - t
    t_per = t/res.shape[0]
    f_per = 1-t_per
    data["pos_pairs"] = t
    data["neg_pairs"] = f
    data["pos_per"]= t_per
    data["neg_per"] = f_per
    
    formatted_string = f"Source language:{args.src_lang}\nTarget language:{args.tgt_lang}\nThreshold:{args.threshold}\nNumnber of clone pairs: {data['pos_pairs']}\nNumber of non-clone pairs: {data['neg_pairs']}\nPercentage of clone pairs: {data['pos_per']*100}%\nPercentege of non-clone pairs: {data['neg_per']*100}%"
    return data, formatted_string