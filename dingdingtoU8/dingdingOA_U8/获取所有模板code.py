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

def get_all_workflow_templates(access_token, user_id):
    """ 分页获取所有工作流模板 """
    url = "https://oapi.dingtalk.com/topapi/process/listbyuserid"
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "access_token": access_token
    }

    all_templates = []
    next_cursor = 0  # 初始偏移量

    while True:
        data = {
            "userid": user_id,  # 替换成你的用户 ID
            "offset": next_cursor,  # 记录分页位置
            "size": 20  # 一次最多获取 20 条
        }
        response = requests.post(url, headers=headers, params=params, json=data)
        result = response.json()

        if result.get("errcode") == 0:
            process_list = result.get("result", {}).get("process_list", [])
            all_templates.extend(process_list)  # 添加到总列表
            next_cursor = result.get("result", {}).get("next_cursor")

            if not next_cursor:  # 没有更多数据了，跳出循环
                break
        else:
            print("获取模板失败:", result.get("errmsg"))
            break

    return all_templates

# 替换你的钉钉用户 ID
user_id = "45415967111121290"
workflow_templates = get_all_workflow_templates(access_token, user_id)

# **整理输出所有模板**
if workflow_templates:
    print("\n📌 **所有工作流模板列表**")
    for process in workflow_templates:
        print(f"模板名称: {process['name']}, 模板 Code: {process['process_code']}")
else:
    print("❌ 未获取到任何模板")
