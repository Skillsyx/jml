import json
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



# **审批模板信息**
process_code = "PROC-BFE32FF9-45C3-4EAD-A535-2E154F298663"
user_id = "45415967111121290"
dept_id = "594387273"

def get_process_fields(access_token, process_code):
    """ 查询审批模板的表单字段 """
    url = "https://oapi.dingtalk.com/topapi/process/form/get"
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "access_token": access_token
    }
    data = {
        "process_code": process_code
    }
    response = requests.post(url, headers=headers, params=params, json=data)
    return response.json()

# 获取模板字段
process_fields = get_process_fields(access_token, process_code)
print(json.dumps(process_fields, indent=4, ensure_ascii=False))

