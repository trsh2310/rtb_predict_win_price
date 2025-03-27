import pandas as pd
import os

data_dir = "/Users/kate_trsh/untitled folder"
data = pd.read_csv('data/imp_data.txt', sep="\t", header = 0)

data_columns = [
    "Bid ID", "Timestamp", "Log type", "iPinYou ID", "User-Agent", "IP",
    "Region", "City", "Ad exchange", "Domain", "URL", "Anonymous URL ID",
    "Ad slot ID", "Ad slot width", "Ad slot height", "Ad slot visibility",
    "Ad slot format", "Ad slot floor price", "Creative ID", "Bidding price",
    "Paying price", "Key page URL", "Advertiser ID", "User Tags", "All paying price"
]
columns_to_drop = [
    "iPinYou ID",  "IP", "Domain", "URL", "Log type",
    "Anonymous URL ID", "Creative ID", "Key page URL", "Ad slot ID", 'All paying price'
]
data = data.drop(columns=columns_to_drop, errors='ignore')
output_file_path = os.path.join(data_dir, "imp_data_prep.txt")
data.to_csv(output_file_path, index=False, sep='\t')

print(f"сохранен в файл: {output_file_path}")