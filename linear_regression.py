import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split

data = pd.read_csv('data/final_data.csv', sep=",", header=0)

data = data[data['Advertiser ID'] == 3386]
data = data[data['Paying price'] > 0]

def parse_timestamp(ts):
    ts_str = str(ts)
    year = int(ts_str[:4])
    month = int(ts_str[4:6])
    day = int(ts_str[6:8])
    hour = int(ts_str[8:10])
    return pd.Timestamp(year=year, month=month, day=day, hour=hour)

data['Timestamp'] = data['Timestamp'].apply(parse_timestamp)
data['Hour'] = data['Timestamp'].dt.hour
data['Weekday'] = data['Timestamp'].dt.weekday

columns_to_drop = [
    "Bid ID", "iPinYou ID", "User-Agent", "IP", "URL", "Log type", "Timestamp",
    "Anonymous URL ID", "Creative ID", "Key page URL", "Ad slot ID", "Advertiser ID", 'All paying price', "Bidding price", "User Tags"
]

data = data.drop(columns=columns_to_drop, errors='ignore')

categorical_features = ['City', 'Region', 'Ad exchange', 'Ad slot visibility', 'Ad slot format', "Hour", "Weekday", "Domain", "os", "device", "device_type", "browser"]

for col in categorical_features:
    data[col] = data[col].fillna("missing").astype('category').cat.codes

X = data.drop(columns=['Paying price'], errors='ignore')
y = data['Paying price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)

predictions = model.predict(X_test)

mse = mean_squared_error(y_test, predictions)
mae = mean_absolute_error(y_test, predictions)
print(f'MSE: {mse}, MAE: {mae}')
