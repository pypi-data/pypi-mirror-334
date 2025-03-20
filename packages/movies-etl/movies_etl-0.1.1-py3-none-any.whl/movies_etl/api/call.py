import os
import requests
import pandas as pd

BASE_URL = "http://kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json"
API_KEY = os.getenv("MOVIES_API_KEY")
    
def gen_url(dt="20120101", url_param={}):
    url = f"{BASE_URL}?key={API_KEY}&targetDt={dt}"
    for k, v in url_param.items():
        url += f"&{k}={v}"
    
    return url

def call_api(dt="20120101", url_param={}):
    url = gen_url(dt, url_param)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        result = data['boxOfficeResult']['dailyBoxOfficeList']
        return result
    else:
        return None

def list2df(data, dt="20120101"):
    num_cols = [
        "rnum", "rank", "rankInten",
        "salesAmt", "salesShare", "salesInten", "salesChange", "salesAcc",
        "audiCnt", "audiInten", "audiChange",
        "scrnCnt", "showCnt"
    ]
    
    df = pd.DataFrame(data)
    df[num_cols] = df[num_cols].apply(pd.to_numeric)
    df["dt"] = dt
    
    return df

def save_df(df, base_path, partition=['dt']) -> str:
    df.to_parquet(base_path, partition_cols=partition)
    save_path = f"{base_path}/dt={df.at[0, 'dt']}"
    
    return save_path