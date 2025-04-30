from fastapi import APIRouter, HTTPException, Body
import requests
import json
from typing import Any, Union

router = APIRouter()

@router.get("/oa/status")
def select_OA_status_api(
    process_instance_id: str = "",

):
    
    # 获取 Access Token
    access_token = get_access_token()
    if not access_token:
        raise HTTPException(status_code=500, detail="无法获取 access_token")

    result = select_instance_status(access_token, process_instance_id)

    
# **解析结果**
    if result.get("errcode") == 0:
        instance_status = result["process_instance"]["status"]
        status_mapping = {
            "RUNNING": "审批进行中",
            "COMPLETED": "审批完成",
            "CANCELED": "审批已取消",
            "TERMINATED": "审批被终止"
        }
        return ({status_mapping.get(instance_status, '未知状态')})
    else:
        return("查询失败")

  

def get_access_token():
    url = "https://oapi.dingtalk.com/gettoken"
    params = {"appkey": CORP_ID, "appsecret": CORP_SECRET}
    try:
        response = requests.get(url, params=params)
        return response.json().get("access_token")
    except Exception as e:
        print("access_token 获取失败：", e)
        return None

def select_instance_status(access_token, process_instance_id):
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


# 钉钉 Access Token 配置信息
CORP_ID = "dingg4komkiirlidfnag"
CORP_SECRET = "WcrjxsKA8Jay95sbge_wF5njoK7f6WR7CYqpMswYbIZwv_45xLDq2ZDzjAMWCS0U"
