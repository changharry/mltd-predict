import time
import numpy as np
from sklearn.linear_model import LinearRegression
import requests
from datetime import datetime
import json

# crontab task
event_id = 339
mr = requests.get(url="https://api.matsurihi.me/mltd/v1/events/{}".format(event_id)).json()
start = mr["schedule"]["beginDate"]
end = mr["schedule"]["endDate"]
start_timestamp = datetime.timestamp(datetime.fromisoformat(start))
end_timestamp = datetime.timestamp(datetime.fromisoformat(end))
duration = (end_timestamp - start_timestamp) / 3600 / 24
meta = {"name": mr["name"], "type": mr["type"]}
regression_all = []
error_coef = [[1.1105949045430998, 1.227981796201434, 1.1624663484378888],
              [1.0549046663924022, 1.1899222056702372, 1.231211872468265],
              [1.050548377220814, 1.1784174675576982, 1.2420410438007683],
              [1.0922104692475685, 1.2721006985284278, 1.270892577586763],
              [1.0736990263175397, 1.2623742303214258, 1.3081179398812943],
              [1.1407900404634956, 1.2791536945760196, 1.1715997980247506],
              [1.0861213870893296, 1.2180994795705316, 1.183472405667727],
              [1.0947647704696863, 1.2191927363110444, 1.1635610048951694],
              [1.0844265781339133, 1.3141024639992862, 1.4059252091752519],
              [1.0860189077205156, 1.2522258435956986, 1.305929320229917],
              [1.2507883038209593, 1.32154573869915, 2.7996109754583456],
              [1.0654926801160294, 1.3016536061757358, 2.272685891162346],
              [1.1057342781396908, 1.231037459250108, 1.2210071761873795],
              [1.097802432624174, 1.2094367921819982, 1.3018006060626954],
              [1.0851055027734617, 1.2911264270306564, 1.2091197942639222],
              [1.0821687417369277, 1.2212219092216403, 1.2892989631884333],
              [1.0869472526872708, 1.1726212926387694, 1.277664823403206],
              [1.0578469708071099, 1.2890833184066577, 1.5875649823248077],
              [1.004408660959923, 1.30913701786743, 1.2478584476775463],
              [1.0886493850462737, 1.2067504970778669, 1.2052335607135771],
              [1.0607324180873479, 1.2664236403181357, 1.1615143903568472],
              [1.113518041745797, 1.186558334497246, 1.2337264478977192],
              [1.1187948579823934, 1.2929510846021819, 1.465741811175337],
              [1.1079505709962332, 1.232969521253654, 1.24476842442683],
              [1.0690826932472293, 1.2586163094647786, 1.389377211271165],
              [1.0808003632961787, 1.211379509315513, 1.2335887151452],
              [1.0815178071266485, 1.2409269732204238, 1.2469029539429912],
              [1.1366186068434911, 1.281952457061006, 1.5103445681613001],
              [1.0429269910472747, 1.2898176895453182, 1.2288233413620513],
              [1.1294559348098874, 1.240206672942844, 1.6236193178756801],
              [1.104925167007513, 1.2343723987834936, 1.486644040276478],
              [1.083887261123146, 1.2706594671172604, 1.285468191747676],
              [1.0972786545412667, 1.2301053421861436, 1.2058551332103082],
              [1.0879849206949708, 1.299612833518413, 2.5280562937907707],
              [1.0904023437236314, 1.2597234133392734, 1.476956262642371],
              [1.092137714075717, 1.3355702212108176, 1.6423536983548914],
              [1.1316819094511439, 1.2340258872247767, 1.33961553874364],
              [1.1210385705357495, 1.2723955777501947, 1.5034917451563228],
              [1.0831135530282439, 1.2308355941453635, 1.1795994767338902],
              [1.0858901760781774, 1.2695788514732038, 1.725513275903376],
              [1.032472075269361, 1.2556098818633004, 1.1955531036563947],
              [1.0919453800125485, 1.2834433787449784, 1.1713455839233635],
              [1.1207688626396433, 1.292287982275071, 1.734895653176525],
              [1.0699191220773712, 1.212485219658612, 1.2204207641008251],
              [1.1056727837238505, 1.2982179209873401, 1.3087904869380673],
              [1.0862714851308195, 1.2482598509772744, 1.275698109773537],
              [1.1075191783687415, 1.2339523610177898, 1.2501331668509046],
              [1.1352922137086423, 1.3221843708798062, 1.2267145095264567],
              [1.105802972650458, 1.218812483604082, 1.2807884507699867],
              [1.0714145753947117, 1.261488069279915, 1.1991720125513219],
              [1.0958864679776918, 1.1843936825389096, 1.3011026267374677],
              [1.1024200174222607, 1.2075253828707602, 1.2570727687746848]]

for k in range(52):
    endpoint = "https://api.matsurihi.me/mltd/v1/events/{}/rankings/logs/idolPoint/{}/10,100,1000".format(event_id,
                                                                                                          k + 1)
    r = requests.get(url=endpoint)
    data = r.json()
    regression = []
    for j in range(len(data)):
        if len(data[j]['data']) == 0:
            break
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

