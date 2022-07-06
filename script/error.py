import json

with open('../data/data2.json') as f:
    data = json.load(f)
    error_list = []
    for i in range(52):
        reg = data["regression_all"][i]
        error = []
        for j in range(len(reg)):
            e = reg[j]["latestScore"] / reg[j]["prediction"]
            error.append(e)
        error_list.append(error)
print(len(error_list))
