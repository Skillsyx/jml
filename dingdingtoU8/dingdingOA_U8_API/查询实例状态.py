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

def get_approval_status(access_token, process_instance_id):
    """ 查询审批实例状态 """
    url = "https://oapi.dingtalk.com/topapi/processinstance/get"
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "access_token": access_token
    }
    data = {
        "process_instance_id": process_instance_id
    }
    response = requests.post(url, headers=headers, params=params, json=data)
    return response.json()

# **审批实例 ID**
process_instance_id = "PUU2NDsiQtipm9ch5oi4nw04501744161771"

# **查询审批状态**
result = get_approval_status(access_token, process_instance_id)


# **解析结果**
if result.get("errcode") == 0:
    instance_status = result["process_instance"]["status"]
    status_mapping = {
        "RUNNING": "审批进行中",
        "COMPLETED": "审批完成",
        "CANCELED": "审批已取消",
        "TERMINATED": "审批被终止"
    }
    print(f"审批实例状态: {status_mapping.get(instance_status, '未知状态')}")
else:
    print(f"❌ 查询失败: {result.get('errmsg')}")
