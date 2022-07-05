import time
import numpy as np
from sklearn.linear_model import LinearRegression
import requests
from datetime import datetime
import json


# crontab task
event_id = 241
mr = requests.get(url="https://api.matsurihi.me/mltd/v1/events/{}".format(event_id)).json()
start = mr["schedule"]["beginDate"]
end = mr["schedule"]["endDate"]
start_timestamp = datetime.timestamp(datetime.fromisoformat(start))
end_timestamp = datetime.timestamp(datetime.fromisoformat(end))
duration = (end_timestamp - start_timestamp) / 3600 / 24
meta = {"name": mr["name"], "type": mr["type"]}
regression_all = []
for k in range(52):
    endpoint = "https://api.matsurihi.me/mltd/v1/events/{}/rankings/logs/idolPoint/{}/10,100,1000".format(event_id,
                                                                                                          k + 1)
    r = requests.get(url=endpoint)
    data = r.json()
    regression = []
    for j in range(len(data)):
        x = []
        y = []
        for i in data[j]['data']:
            y.append(i['score'])
            x.append((datetime.timestamp(datetime.fromisoformat(i['summaryTime'])) - start_timestamp) / 3600 / 24)
        x0 = np.array(x).reshape((-1, 1))
        y0 = np.array(y)
        model = LinearRegression().fit(x0, y0)
        scatter = {"x": x, "y": y}
        latestTime = datetime.fromtimestamp(x[-1] * 24 * 3600 + start_timestamp).strftime("%Y-%m-%d, %H:%M:%S")
        prediction = round(model.intercept_ + model.coef_[0] * duration)
        remain = round(duration - x[-1], 2)
        last = {"idol_id": k + 1,
                "latestTime": latestTime,
                "remain": remain,
                "latestScore": y[-1],
                "prediction": prediction,
                "scatter": scatter}
        regression.append(last)
    regression_all.append(regression)
    time.sleep(0.5)
result = {"meta": meta, "regression_all": regression_all}
with open('../data/data.json', 'w') as f:
    json.dump(result, f)

# plt.scatter(x, y, s=1)
# plt.plot(x, model.predict(x0), c='r')
# plt.show()
