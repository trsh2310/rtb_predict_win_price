import pandas as pd
import os
data_columns = [
    "Bid ID", "Timestamp", "Log type", "iPinYou ID", "User-Agent", "IP",
    "Region", "City", "Ad exchange", "Domain", "URL", "Anonymous URL ID",
    "Ad slot ID", "Ad slot width", "Ad slot height", "Ad slot visibility",
    "Ad slot format", "Ad slot floor price", "Creative ID", "Bidding price",
    "Paying price", "Key page URL", "Advertiser ID", "User Tags"
]
col_to_drop = ["Bid ID", "Key page URL"]
data_dir = "/Users/kate_trsh/untitled folder/data"

bid_files = [f for f in os.listdir(data_dir) if f.startswith('imp.201306')]

dfs = []
for file in bid_files:
    df = pd.read_csv(
        os.path.join(data_dir, file),
        sep='\t',
        header=None,
        names=data_columns,
        engine='python'
    )
    dfs.append(df)


data = pd.concat(dfs, ignore_index=True)

import re
from ua_parser import user_agent_parser


def parse_user_agent(ua):
    if pd.isna(ua): 
        return {
            'device_type': 'Unknown',
        }


    parsed = user_agent_parser.Parse(ua)

    device_type = 'Other'

    if 'Mobile' in parsed['device']['family']:
        device_type = 'Mobile'

    elif 'Tablet' in parsed['device']['family']:
        device_type = 'Mobile'
    elif 'Bot' in parsed['user_agent']['family']:
        device_type = 'Other'
    elif parsed['os']['family'] in ('Windows', 'Mac OS X', 'Linux'):
        device_type = 'Desktop'

    return {
        'device_type': device_type,
    }

def prefilter_ua(ua):
    if pd.isna(ua):
        return 'Unknown'
    if re.search(r"(iPhone|Android|Mobile)", ua, re.IGNORECASE):
        return 'Mobile'
    elif re.search(r"(Tablet|iPad)", ua, re.IGNORECASE):
        return 'Tablet'
    elif re.search(r"(Windows NT|Macintosh|Linux)", ua, re.IGNORECASE):
        return 'Desktop'
    elif re.search(r"(Bot|Spider|Crawler)", ua, re.IGNORECASE):
        return 'Bot'
    else:
        return 'Other'


data['device_type_prefilter'] = data['User-Agent'].apply(prefilter_ua)

unique_uas = data['User-Agent'].dropna().unique()
parsed_uas = {ua: parse_user_agent(ua) for ua in unique_uas}

data[['device', 'os', 'browser', 'device_type', 'is_mobile']] = data['User-Agent'].map(parsed_uas).apply(pd.Series)

data.drop(columns=['device_type_prefilter', "Bid ID", "Key page URL"], inplace=True)

print(data.head())

output_file_path = os.path.join(data_dir, "season2_imp.txt")
data.to_csv(output_file_path, index=False, sep='\t')

print(f"Объединенные данные сохранены в файл: {output_file_path}")