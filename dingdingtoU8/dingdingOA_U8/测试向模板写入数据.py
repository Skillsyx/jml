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

def create_approval_instance(access_token, process_code, user_id, dept_id, form_data):
    """ 向指定模板提交审批数据 """
    url = "https://oapi.dingtalk.com/topapi/processinstance/create"
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "access_token": access_token
    }
    data = {
        "process_code": process_code,  # 审批模板 Code
        "originator_user_id": user_id,  # 申请人 UserID
        "dept_id": dept_id,  # 部门 ID
        "form_component_values": form_data  # 审批表单数据
    }
    
    response = requests.post(url, headers=headers, params=params, json=data)
    return response.json()

# **审批模板信息**
process_code = "PROC-BFE32FF9-45C3-4EAD-A535-2E154F298663"
user_id = "45415967111121290"
dept_id = "594387273"

# **主表单字段**
form_data = [
    {"name": "业务类型", "value": "备品备件采购"},  # ✅ 必填
    {"name": "单据编号", "value": "CGDD250342112"},
    {"name": "单据日期", "value": "2025-03-06"},
    {"name": "供应商名称", "value": "苏州腾诚机电设备有限公司"},
    {"name": "收货地址", "value": "123"},
    {"name": "部门", "value": "质量"},    
    {"name": "业务员", "value": "查汝婷"},
    {"name": "币种", "value": "无"},
    {"name": "制单人", "value": "查汝婷"},
    
    # **✅ 必填字段：总金额**
    {"name": "总金额", "value": "12000"}  # ⚠️ 这个字段必须填写，否则会报错
]

# **子表单（表格字段）**
sub_form_data = [
    [
        {"name": "销售订单号", "value": "SO-20250306001"},
        {"name": "存货名称", "value": "电机"},
        {"name": "数量", "value": "5"},
        {"name": "含税单价", "value": "1000"},
        {"name": "无税单价", "value": "900"},
        {"name": "税率", "value": "10"},
        {"name": "无税金额", "value": "4500"},
        {"name": "税额", "value": "500"},
        {"name": "价税合计", "value": "5000"},
        {"name": "交期", "value": "2025-03-10"}
    ],
    [
        {"name": "销售订单号", "value": "SO-20250306002"},
        {"name": "存货名称", "value": "变频器"},
        {"name": "数量", "value": "2"},
        {"name": "含税单价", "value": "5000"},
        {"name": "无税单价", "value": "4500"},
        {"name": "税率", "value": "10"},
        {"name": "无税金额", "value": "9000"},
        {"name": "税额", "value": "1000"},
        {"name": "价税合计", "value": "10000"},
        {"name": "交期", "value": "2025-03-12"}
    ]
]

# **转换成 JSON 字符串**
sub_form_json = json.dumps(sub_form_data, ensure_ascii=False)

# **添加子表单数据**
form_data.append({
    "name": "表格",  # ⚠️ 这个名称必须和你的钉钉模板字段匹配
    "value": sub_form_json  # 子表单数据需要转换为 JSON 字符串
})

# **提交审批**
result = create_approval_instance(access_token, process_code, user_id, dept_id, form_data)

# **输出结果**
if result.get("errcode") == 0:
    print(f"✅ 审批提交成功，实例 ID: {result['process_instance_id']}")
else:
    print(f"❌ 审批提交失败: {result.get('errmsg')}")
