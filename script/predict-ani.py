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
error_coef = [[1.1105949045430998, 1.2250315489649668, 1.1624663484378888],
              [1.0260818839921038, 1.1865922161934563, 1.231211872468265],
              [1.050548377220814, 1.1784174675576982, 1.2420410438007683],
              [1.0922104692475685, 1.2721006985284278, 1.2245291254329698],
              [1.037394263220248, 1.2623742303214258, 1.3081179398812943],
              [1.1407900404634956, 1.2791536945760196, 1.1715997980247506],
              [1.0466306234946834, 1.188701065057391, 1.1587035348501877],
              [1.0945906739528566, 1.2191927363110444, 1.1635610048951694],
              [1.013122567830677, 1.3141024639992862, 1.4059252091752519],
              [0.9616910341494331, 1.2522258435956986, 1.305929320229917],
              [1.2507883038209593, 1.2516938950988823, 2.3732492044929154],
              [1.0654926801160294, 1.3016536061757358, 1.8169699809940378],
              [0.9483784589888786, 1.21667766520012, 1.1907805959123368],
              [1.0332179573280984, 1.2094367921819982, 1.2379634696861086],
              [0.9980865376249891, 1.2911264270306564, 1.2091197942639222],
              [1.0581271945552224, 1.2212219092216403, 1.1935623970967482],
              [1.0869472526872708, 1.1473828134981725, 1.277664823403206],
              [1.0525430702640526, 1.2890833184066577, 1.4786947944389646],
              [1.004408660959923, 1.30913701786743, 1.2075768446761097],
              [1.0886493850462737, 1.1550302032221973, 1.2052335607135771],
              [0.9535649515865271, 1.2664236403181357, 1.1615143903568472],
              [1.113518041745797, 1.186558334497246, 1.2337264478977192],
              [1.1187948579823934, 1.2534865066998429, 1.3428104575163398],
              [1.1079505709962332, 1.232969521253654, 1.24476842442683],
              [1.0690826932472293, 1.2586163094647786, 1.3802307170323456],
              [1.0768171707727696, 1.211379509315513, 1.2335887151452],
              [1.0815178071266485, 1.2409269732204238, 1.2358305037678452],
              [1.1366186068434911, 1.2523159293209452, 1.4738474759841778],
              [1.0429269910472747, 1.2898176895453182, 1.2063202598567975],
              [1.1294559348098874, 1.1851567970751844, 1.5120219773358723],
              [1.0154019304184974, 1.2343723987834936, 1.373507159972077],
              [0.9850205081718558, 1.2706594671172604, 1.285468191747676],
              [1.0471200134263288, 1.2301053421861436, 1.2058551332103082],
              [1.0283775738156504, 1.299612833518413, 2.026825479026411],
              [1.0777090339144462, 1.1825850997653828, 1.476956262642371],
              [1.092137714075717, 1.3355702212108176, 1.5158137561389562],
              [1.1316819094511439, 1.2340258872247767, 1.3008460183171695],
              [1.0844911648223095, 1.2723955777501947, 1.5034917451563228],
              [1.0766705371592131, 1.2308355941453635, 1.1795994767338902],
              [1.0466332466484716, 1.2695788514732038, 1.5925221379223902],
              [1.0305701889542704, 1.2556098818633004, 1.1955531036563947],
              [1.0093128546731434, 1.2418526755728039, 1.1713455839233635],
              [1.1207688626396433, 1.292287982275071, 1.6904427137460112],
              [1.0699191220773712, 1.1826673716236045, 1.2204207641008251],
              [0.996315895540807, 1.2617683169642, 1.2642568103713618],
              [1.0862714851308195, 1.2482598509772744, 1.2443402923512983],
              [1.1075191783687415, 1.2339523610177898, 1.2235195907688288],
              [1.1352922137086423, 1.3221843708798062, 1.1952541450729421],
              [1.0933318365514144, 1.218812483604082, 1.2807884507699867],
              [1.0138730898058028, 1.261488069279915, 1.1870524568422645],
              [1.0957791480230987, 1.1843936825389096, 1.3011026267374677],
              [1.0777668911352078, 1.1952002791079608, 1.2570727687746848]]

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
            days = (datetime.timestamp(datetime.fromisoformat(i['summaryTime'])) - start_timestamp) / 3600 / 24
            y.append(i['score'])
            x.append(days)

        x0 = np.array(x).reshape((-1, 1))
        y0 = np.array(y)
        model = LinearRegression().fit(x0, y0)
        scatter = {"x": x, "y": y}
        latestTime = datetime.fromtimestamp(x[-1] * 24 * 3600 + start_timestamp).strftime("%Y-%m-%d, %H:%M:%S")
        prediction = round((model.intercept_ + model.coef_[0] * duration) * error_coef[k][j])
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
with open('./data/data.json', 'w') as f:
    json.dump(result, f)

# plt.scatter(x, y, s=1)
# plt.plot(x, model.predict(x0), c='r')
# plt.show()
