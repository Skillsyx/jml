import requests

# 钉钉 Access Token 配置
CORP_ID = "dingg4komkiirlidfnag"
CORP_SECRET = "WcrjxsKA8Jay95sbge_wF5njoK7f6WR7CYqpMswYbIZwv_45xLDq2ZDzjAMWCS0U"

def get_access_token():
    url = "https://oapi.dingtalk.com/gettoken"
    params = {"appkey": CORP_ID, "appsecret": CORP_SECRET}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        print("Access Token 返回结果：", data)
        return data.get("access_token")
    except Exception as e:
        print("access_token 获取失败：", e)
        return None

def select_instance_status(access_token, process_instance_id):
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
    try:
        response = requests.post(url, headers=headers, params=params, json=data)
        response.raise_for_status()
        result = response.json()
        print("审批状态返回结果：", result)
        return result
    except Exception as e:
        print("审批状态查询失败：", e)
        return {"errcode": -1, "errmsg": str(e)}

def test_oa_status(process_instance_id):
    token = get_access_token()
    if not token:
        print("❌ 获取 access_token 失败")
        return

    result = select_instance_status(token, process_instance_id)

    if result.get("errcode") == 0:
        status = result["process_instance"]["status"]
        status_mapping = {
            "RUNNING": "审批进行中",
            "COMPLETED": "审批完成",
            "CANCELED": "审批已取消",
            "TERMINATED": "审批被终止"
        }
        print("审批状态：", status_mapping.get(status, "未知状态"))
    else:
        print("❌ 查询失败：", result.get("errmsg"))

# ✅ 替换为你要测试的实例 ID
if __name__ == "__main__":
    test_oa_status("PUU2NDsiQtipm9ch5oi4nw04501744161771")
