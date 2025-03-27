import pandas as pd

def load_file(filepath):
    return pd.read_csv(filepath, sep="\t", header = None, names = data_columns)

data_columns = [
    "Bid ID", "Timestamp", "Log type", "iPinYou ID", "User-Agent", "IP",
    "Region", "City", "Ad exchange", "Domain", "URL", "Anonymous URL ID",
    "Ad slot ID", "Ad slot width", "Ad slot height", "Ad slot visibility",
    "Ad slot format", "Ad slot floor price", "Creative ID", "Bidding price",
    "Paying price", "Key page URL", "Advertiser ID", "User Tags"
]

files = [
    "imp.20130606.txt",
    "imp.20130607.txt",
    "imp.20130608.txt",
    "imp.20130609.txt",
    "imp.20130610.txt",
    "imp.20130611.txt",
    "imp.20130612.txt"
]
data_files = [load_file(file) for file in files]
data = pd.concat(data_files)



data.to_csv('imp_data_iPinYou', sep='\t', index=False)
