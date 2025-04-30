from fastapi import APIRouter, HTTPException, Body
import requests
import json
from typing import Any, Union
from sqlserverdb import SQLServerDB

router = APIRouter()

@router.post("/oa/submit")
def writhe_OA_Purchaseorder_api(
    process_code: str = 'PROC-BFE32FF9-45C3-4EAD-A535-2E154F298663',
    user_id: str = '45415967111121290',
    dept_id: str = '594387273',
    form_dataa: Union[dict, str] = Body(...)
):
    # SQL Server 连接参数
    server = '172.16.1.9'
    database = 'yx_test'
    username = 'sa'
    password = 'Ks123456'

    # 初始化数据库连接
    db = SQLServerDB(server, database, username, password)
    # 如果传入的是字符串，则尝试转换为字典
    if isinstance(form_dataa, str):
        try:
            header = json.loads(form_dataa)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"form_dataa 转换失败: {e}")
    elif isinstance(form_dataa, dict):
        header = form_dataa
    else:
        raise HTTPException(status_code=400, detail="form_dataa 格式不正确")
    
    # 下面进行后续处理...
    # 获取 Access Token
    access_token = get_access_token()
    if not access_token:
        raise HTTPException(status_code=500, detail="无法获取 access_token")

    # 构建主表数据
    total_amount = sum(float(item.get("sum", 0)) for item in header.get("entry", []))
    form_data = [
        {"name": "业务类型", "value": header.get("purchase_type_name", "无")},
        {"name": "单据编号", "value": header.get("code", "无")},
        {"name": "单据日期", "value": header.get("date", "2022-01-01")},
        {"name": "供应商名称", "value": header.get("vendorname", "无")},
        {"name": "收货地址", "value": "123"},
        {"name": "部门", "value": header.get("deptname", "无")},
        {"name": "业务员", "value": header.get("maker", "无")},
        {"name": "币种", "value": "人民币"},
        {"name": "制单人", "value": header.get("maker", "无")},
        {"name": "总金额", "value": f"{float(total_amount):.2f}"}
    ]

    # 构建子表数据
    sub_form_data_list = []
    for entry in header.get("entry", []):
        # 查询中间表数据
        query = f"""
            select a.cInvCode,b.dPODate,b.iQuantity,cu.cuantity from (
            select max(id)id,cInvCode from tempdb..yx_podindanzhixing008 group by cInvCode
            )a
            left join tempdb..yx_podindanzhixing008 b on a.id =b.id	
            left join (select cInvCode ,sum(iQuantity)cuantity from ufdata_008_2021..CurrentStock group by cInvCode) cu on a.cInvCode = cu.cInvCode
            where a.cInvCode = '{entry.get("inventorycode", "无")}'
        """
        result = db.query(query)
        sub_form_data_list.append([
            {"name": "存货名称", "value": entry.get("inventoryname", "无")},
            {"name": "数量", "value": f"{round(float(entry.get('quantity', '1423428')), 2):.2f}"},
            {"name": "含税单价", "value": f"{round(float(entry.get('taxprice', '1423428')), 2):.2f}"},
            # {"name": "无税单价", "value": f"{round(float(entry.get('price', '1423428')), 2):.2f}"},
            # {"name": "税率", "value": f"{round(float(entry.get('taxrate', '13')), 2):.2f}"},
            # {"name": "无税金额", "value": f"{round(float(entry.get('money', '1423428')), 2):.2f}"},
            # {"name": "税额", "value": f"{round(float(entry.get('tax', '1423428')), 2):.2f}"},
            {"name": "价税合计", "value": f"{round(float(entry.get('sum', '1423428')), 2):.2f}"},
            # {"name": "交期", "value": entry.get("arrivedate", "2022-01-01")}
            {"name": "上次采购日期", "value": str(result[0]["dPODate"]) if result else ""},
            {"name": "上次采购数量", "value": str(f"{round(float(result[0]["iQuantity"]),2):.2f}") if result else "0.00"},
            {"name": "库存数量", "value": str(f"{round(float(result[0]['cuantity']),2):.2f}") if result else "0.00"},
        ])
    
    sub_form_json = json.dumps(sub_form_data_list, ensure_ascii=False)
    form_data.append({
        "name": "表格",
        "value": sub_form_json
    })

    # 提交审批
    result = create_approval_instance(access_token, process_code, user_id, dept_id, form_data)

    if result.get("errcode") == 0:
        return {"成功": result}
    else:
        return {"失败": {"result": result, "form_data": form_data}}
    
    db.close()

def get_access_token():
    url = "https://oapi.dingtalk.com/gettoken"
    params = {"appkey": CORP_ID, "appsecret": CORP_SECRET}
    try:
        response = requests.get(url, params=params)
        return response.json().get("access_token")
    except Exception as e:
        print("access_token 获取失败：", e)
        return None

def create_approval_instance(access_token, process_code, user_id, dept_id, form_data):
    url = "https://oapi.dingtalk.com/topapi/processinstance/create"
    headers = {"Content-Type": "application/json"}
    params = {"access_token": access_token}
    data = {
        "process_code": process_code,
        "originator_user_id": user_id,
        "dept_id": dept_id,
        "form_component_values": form_data
    }
    try:
        response = requests.post(url, headers=headers, params=params, json=data)
        if not response.text.strip():
            return {"errcode": -1, "errmsg": "接口返回空响应"}
        return response.json()
    except Exception as e:
        print("钉钉返回内容异常：", e)
        return {"errcode": -1, "errmsg": "非JSON响应"}

# 钉钉 Access Token 配置信息
CORP_ID = "dingg4komkiirlidfnag"
CORP_SECRET = "WcrjxsKA8Jay95sbge_wF5njoK7f6WR7CYqpMswYbIZwv_45xLDq2ZDzjAMWCS0U"
