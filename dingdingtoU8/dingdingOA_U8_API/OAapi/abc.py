from fastapi import APIRouter, HTTPException
import requests
import json
import ast


# 钉钉企业应用信息
CORP_ID = "dingg4komkiirlidfnag"
CORP_SECRET = "WcrjxsKA8Jay95sbge_wF5njoK7f6WR7CYqpMswYbIZwv_45xLDq2ZDzjAMWCS0U"

def get_access_token():
    """获取 Access Token"""
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

def create_approval_instance(access_token, process_code, user_id, dept_id, form_data):
    """向指定模板提交审批数据"""
    url = "https://oapi.dingtalk.com/topapi/processinstance/create"
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "access_token": access_token
    }
    data = {
        "process_code": process_code,  # 审批模板 Code
        "originator_user_id": user_id,   # 申请人 UserID
        "dept_id": dept_id,              # 部门 ID
        "form_component_values": form_data  # 审批表单数据
    }
    
    response = requests.post(url, headers=headers, params=params, json=data)
    return response.json()



process_code  = "PROC-BFE32FF9-45C3-4EAD-A535-2E154F298663"
user_id  = "45415967111121290"
dept_id = "594387273"
form_dataa = """{
    'code': 'CGDD250212106',
    'date': '2025-02-27',
    'operation_type_code': '普通采购',
    'state': '开立',
    'purchase_type_code': '11',
    'purchase_type_name': '一次性耗材采购',
    'vendorcode': '011041',
    'vendorname': '昆山巴城晟希服装加工厂',
    'vendorabbname': '昆山巴城晟希服装加工厂',
    'deptcode': '05101',
    'deptname': '人事行政',
    'maker': '查汝婷',
    'define1': '票到付款',
    'define2': '陆运',
    'define12': '增值税发票：',
    'define13': '企业标准',
    'remark': '票到后付款，交期：订单审批后30天',
    'entry': [
        {
            'inventorycode': '72000410',
            'inventoryname': '夏季工作服',
            'inventorystd': '短袖',
            'unitname': '件',
            'quantity': '60.0000000000',
            'arrivedate': '2025-04-30',
            'price': '33.9805000000',
            'taxprice': '35.000000',
            'money': '2038.8300',
            'tax': '61.1700',
            'sum': '2100.0000',
            'taxrate': '3.000000',
            'rowno': '1'
        },
        {
            'inventorycode': '32-33-LZ-0040',
            'inventoryname': '龙珠 辊涂白色底漆',
            'inventorystd': 'UV-E01',
            'unitname': '千克',
            'quantity': '120.0000000000',
            'arrivedate': '2025-02-27',
            'price': '44.2478000000',
            'taxprice': '50.000000',
            'money': '5309.7300',
            'tax': '690.2700',
            'sum': '6000.0000',
            'taxrate': '13.000000',
            'rowno': '2'
        }

    ]
}"""



# 获取 Access Token
access_token = get_access_token()
if not access_token:
    raise HTTPException(status_code=500, detail="无法获取 access_token")

header = ast.literal_eval(form_dataa)
print(type(header))
print(type(form_dataa))
total_amount = sum(float(item["sum"]) for item in header.get("entry", []))

# **主表单字段**
form_data = [
    {"name": "业务类型", "value": header.get("purchase_type_name")},
    {"name": "单据编号", "value": header.get("code")},
    {"name": "单据日期", "value": header.get("date")},
    {"name": "供应商名称", "value": header.get("vendorname")},
    {"name": "收货地址", "value": ""},
    {"name": "部门", "value": header.get("deptname")},
    {"name": "业务员", "value": header.get("personname", "无")},
    {"name": "币种", "value": "人民币"},
    {"name": "制单人", "value": header.get("maker")},
    {"name": "总金额", "value": total_amount}
]

body = header.get("entry", [])
sub_form_data_list = []

for entry in body:
    sub_form_data = [
        {"name": "存货名称", "value": entry.get("inventoryname")},
        {"name": "数量", "value": entry.get("quantity")},
        {"name": "含税单价", "value": entry.get("taxprice")},
        {"name": "无税单价", "value": entry.get("price")},
        {"name": "税率", "value": entry.get("taxrate")},
        {"name": "无税金额", "value": entry.get("money")},
        {"name": "税额", "value": entry.get("tax")},
        {"name": "价税合计", "value": entry.get("sum")},
        {"name": "交期", "value": entry.get("arrivedate")}
    ]
    sub_form_data_list.append(sub_form_data)

# print(sub_form_data_list)

sub_form_json = json.dumps(sub_form_data_list, ensure_ascii=False)

form_data.append({
    "name": "表格",  # 这个名称必须和钉钉模板字段匹配
    "value": sub_form_json  # 子表单数据需要转换为 JSON 字符串
})

# 提交审批
result = create_approval_instance(access_token, process_code, user_id, dept_id, form_data)

# 处理结果
print(result)
