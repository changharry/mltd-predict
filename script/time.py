from datetime import datetime

start_timestamp = datetime.timestamp(datetime.fromisoformat("2023-06-30T00:00:00+09:00"))
days = (datetime.timestamp(datetime.fromisoformat("2023-06-30T05:00:00+09:00")) - start_timestamp) / 3600 / 24
latestTime = datetime.fromtimestamp(days * 24 * 3600 + start_timestamp).strftime("%Y-%m-%d, %H:%M:%S")
print(latestTime)