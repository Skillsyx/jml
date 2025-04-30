import requests

# 钉钉企业应用信息
CORP_ID = "dingg4komkiirlidfnag"
CORP_SECRET = "WcrjxsKA8Jay95sbge_wF5njoK7f6WR7CYqpMswYbIZwv_45xLDq2ZDzjAMWCS0U"

def get_access_token():
    """ 获取 Access Token """
    url = "https://oapi.dingtalk.com/gettoken"
    params = {
        "appkey": CORP_ID,
        "appsecret": CORP_SECRET
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data.get("errcode") == 0:
        return data.get("access_token")
    else:
        print("获取 access_token 失败:", data.get("errmsg"))
        return None

access_token = get_access_token()
print("Access Token:", access_token)
user_id = "45415967111121290"

def get_user_info(access_token, user_id):
    url = "https://oapi.dingtalk.com/topapi/v2/user/get"
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "access_token": access_token
    }
    data = {
        "userid": user_id
    }
    response = requests.post(url, headers=headers, params=params, json=data)
    return response.json()

user_info = get_user_info(access_token, user_id)
print("部门 ID:", user_info.get("result", {}).get("dept_id_list", []))
