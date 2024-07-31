import time
import numpy as np
from sklearn.linear_model import LinearRegression
import requests
from datetime import datetime
import json

# crontab task
# 10,40 * * * * cd mltd-predict && venv/bin/python script/predict.py
event_id = 343
mr = requests.get(url="https://api.matsurihi.me/mltd/v1/events/{}".format(event_id)).json()
start = mr["schedule"]["beginDate"]
end = mr["schedule"]["endDate"]
start_timestamp = datetime.timestamp(datetime.fromisoformat(start))
end_timestamp = datetime.timestamp(datetime.fromisoformat(end))
duration = (end_timestamp - start_timestamp) / 3600 / 24
meta = {"name": mr["name"], "type": mr["type"]}
err = duration
error_coef = 1.3

endpoint = "https://api.matsurihi.me/mltd/v1/events/{}/rankings/logs/eventPoint/100,2500,5000,10000,25000,50000".format(
    event_id)
r = requests.get(url=endpoint)
data = r.json()
regression = []

for j in range(len(data)):
    x = []
    y = []
    if len(data[j]['data']) == 0:
        continue
    for i in data[j]['data']:
        days = (datetime.timestamp(datetime.fromisoformat(i['summaryTime'])) - start_timestamp) / 3600 / 24
        y.append(i['score'])
        x.append(days)

    x0 = np.array(x).reshape((-1, 1))
    y0 = np.array(y)
    model = LinearRegression().fit(x0, y0)
    scatter = {"x": x, "y": y}
    latestTime = datetime.fromtimestamp(x[-1] * 24 * 3600 + start_timestamp).strftime("%Y-%m-%d, %H:%M:%S")
    prediction = round((model.intercept_ + model.coef_[0] * duration) * error_coef)
    remain = round(duration - x[-1], 2)
    last = {"latestTime": latestTime,
            "remain": remain,
            "latestScore": y[-1],
            "prediction": prediction,
            "scatter": scatter}
    regression.append(last)
time.sleep(0.5)
result = {"meta": meta, "regression": regression}
with open('./data/data.json', 'w') as f:
    json.dump(result, f)
