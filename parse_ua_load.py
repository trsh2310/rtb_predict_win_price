import pandas as pd
import os
from user_agents import parse

input_file = "data/imp_data.txt"
ua_parsed_file = "data/user_agent_parsed.csv"
final_output_file = "data/final_data.csv"


data = pd.read_csv(input_file, sep="\t", header=0)


if os.path.exists(ua_parsed_file):
    ua_parsed = pd.read_csv(ua_parsed_file)
else:

    unique_ua = data['User-Agent'].dropna().unique()

    def parse_ua(ua):
        ua_obj = parse(ua)
        if ua_obj.is_mobile:
            device_type = 'Mobile'
        elif ua_obj.is_tablet:
            device_type = 'Tablet'
        elif ua_obj.is_pc:
            device_type = 'Desktop'
        elif ua_obj.is_bot:
            device_type = 'Bot'
        else:
            device_type = 'Other'
        return {
            'User-Agent': ua,
            'device': ua_obj.device.family,
            'os': ua_obj.os.family,
            'browser': ua_obj.browser.family,
            'device_type': device_type
        }
    parsed_data = [parse_ua(ua) for ua in unique_ua]

    ua_parsed = pd.DataFrame(parsed_data)

    ua_parsed.to_csv(ua_parsed_file, index=False)

data = data.merge(ua_parsed, on="User-Agent", how="left")
data.drop(columns=["User-Agent"], inplace=True)
data.to_csv(final_output_file, index=False)