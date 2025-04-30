import requests

# 钉钉企业应用信息
CORP_ID = "dingg4komkiirlidfnag"
CORP_SECRET = "WcrjxsKA8Jay95sbge_wF5njoK7f6WR7CYqpMswYbIZwv_45xLDq2ZDzjAMWCS0U"

def get_access_token():
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


def get_user_id_by_mobile(access_token, mobile):
    url = "https://oapi.dingtalk.com/topapi/v2/user/getbymobile"
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "access_token": access_token
    }
    data = {
        "mobile": mobile  # 这里填写用户的手机号
    }
    response = requests.post(url, headers=headers, params=params, json=data)
    return response.json()

# 替换为你的钉钉手机号
mobile_number = "18556785498"
user_info = get_user_id_by_mobile(access_token, mobile_number)

if user_info.get("errcode") == 0:
    user_id = user_info.get("result", {}).get("userid")
    print("用户ID:", user_id)
else:
    print("获取用户ID失败:", user_info.get("errmsg"))
