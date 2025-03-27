import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#from catboost import CatBoostRegressor, Pool
from sklearn.model_selection import train_test_split
import scipy.stats as stats

import re
from ua_parser import user_agent_parser

def month_format(date):
    month = str(date)[4:6]
    return month

def day_format(date):
    day = str(date)[6:8]
    return day

def hour_format(date):
    hour = str(date)[8:10]
    return hour

def phone_or_web(user_agent_str):
    if 'Android' in user_agent_str or 'iPhone' in user_agent_str or 'iPad' in user_agent_str:
        return 'phone'
    else:
        return 'web'


def parse_user_agent(ua):
    if pd.isna(ua):  # Проверка на NaN
        return {
            'device_type': 'Unknown',
        }

    # Парсим User-Agent с помощью ua-parser
    parsed = user_agent_parser.Parse(ua)

    # Определяем тип устройства
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


data_columns = [
    "Bid ID", "Timestamp", "Log type", "iPinYou ID", "User-Agent", "IP",
    "Region", "City", "Ad exchange", "Domain", "URL", "Anonymous URL ID",
    "Ad slot ID", "Ad slot width", "Ad slot height", "Ad slot visibility",
    "Ad slot format", "Ad slot floor price", "Creative ID", "Bidding price",
    "Paying price", "Key page URL", "Advertiser ID", "User Tags", "All paying price"
]


data = pd.read_csv('data/all_data_iPinYou', sep="\t")

print("Количество строк в датасете: ", len(data))
conversions = data[data['Log type'] == 3]

data['Device'] = data['User-Agent'].apply(parse_user_agent)

conversion_counts = conversions.groupby('Device').size()
print(conversion_counts)

mobile_conv_count = conversion_counts.get('Mobile', 0)
desktop_conv_count = conversion_counts.get('Desktop', 0)
print(mobile_conv_count, desktop_conv_count)

total_mobile_count = data[(data['Device'] == 'Mobile') & (data['Log type'] == 1)].shape[0]
total_desktop_count = data[(data['Device'] == 'Desktop') & (data['Log type'] == 1)].shape[0]
print(total_mobile_count, total_desktop_count)
#доли конверсий
conv_mobile = mobile_conv_count / total_mobile_count
conv_desktop = desktop_conv_count / total_desktop_count

p_pool = (mobile_conv_count + desktop_conv_count) / (total_mobile_count + total_desktop_count)
z_stat = (conv_mobile - conv_desktop) / ((p_pool * (1 - p_pool) * (1 / total_mobile_count + 1 / total_desktop_count)) ** 0.5)
sns.histplot(data, bins=30, kde=True)
plt.show()
p_value = stats.norm.sf(abs(z_stat))

#stat, pval = ztest(count, nobs, alternative='smaller')


print(f"Z-статистика: {z_stat}")
print(f"p-value: {p_value}")

#рисую усы
if p_value < 0.05:
    print("Отвергаем")
else:
    print("Нет оснований отвергать")
