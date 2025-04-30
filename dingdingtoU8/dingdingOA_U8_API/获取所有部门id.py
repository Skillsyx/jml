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

def get_all_departments(access_token):
    url = "https://oapi.dingtalk.com/department/list"
    params = {
        "access_token": access_token
    }
    response = requests.get(url, params=params)
    return response.json()

access_token = get_access_token()
if access_token:
    departments = get_all_departments(access_token)
    if departments.get("errcode") == 0:
        # 遍历返回的部门列表，输出每个部门的 ID 和名称
        for dept in departments.get("department", []):
            print("部门ID:", dept.get("id"), "名称:", dept.get("name"))
    else:
        print("获取部门信息失败:", departments.get("errmsg"))
else:
    print("无法获取 access_token")
