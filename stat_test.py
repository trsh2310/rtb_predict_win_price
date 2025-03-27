import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import levene, bartlett, ttest_ind, mannwhitneyu
import seaborn as sns

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

data_columns = [
    "Bid ID", "Timestamp", "Log type", "iPinYou ID", "User-Agent", "IP",
    "Region", "City", "Ad exchange", "Domain", "URL", "Anonymous URL ID",
    "Ad slot ID", "Ad slot width", "Ad slot height", "Ad slot visibility",
    "Ad slot format", "Ad slot floor price", "Creative ID", "Bidding price",
    "Paying price", "Key page URL", "Advertiser ID", "User Tags", "All paying price"
]
data = pd.read_csv('data/data_iPinYou', sep="\t", header = None, names = data_columns)
data.drop_duplicates()
count_dup = data.duplicated().sum()
print(count_dup)
print(data.nunique())

data = data.dropna(subset=['User-Agent', "All paying price"])
data['Device'] = data['User-Agent'].apply(phone_or_web)
data = data[data["Log type"] == 2]
"""plt.figure(figsize=(8,6))
sns.histplot(data['Device'], bins=1000)
plt.show()"""

clk_mobile = data[data['Device'] == 'phone']["All paying price"]
clk_desktop = data[data['Device'] == 'web']["All paying price"]

levene_stat, levene_p = levene(clk_mobile, clk_desktop)
print(f"Тест Левена: статистика = {levene_stat}, p-значение = {levene_p}")

t_stat, p_value = ttest_ind(clk_mobile, clk_desktop, equal_var=(levene_p >= 0.05), alternative='less')
print(f"t-статистика: {t_stat}, p-значение: {p_value}")

mann_u_stat, mann_p_value = mannwhitneyu(clk_mobile, clk_desktop, alternative='less')
print(f"Манн-Уитни U-тест: статистика = {mann_u_stat}, p-значение = {mann_p_value}")

alpha = 0.05
if p_value < alpha:
    print("Результат t-теста: клики на мобильных устройствах дешевле (p < 0.05).")
else:
    print("Результат t-теста: нет статистически значимого различия (p >= 0.05).")

if mann_p_value < alpha:
    print("Результат U-теста: клики на мобильных устройствах дешевле (p < 0.05).")
else:
    print("Результат U-теста: нет статистически значимого различия (p >= 0.05).")