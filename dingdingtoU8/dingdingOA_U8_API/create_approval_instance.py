from fastapi import APIRouter, HTTPException
import requests

router = APIRouter()

@router.get("/get")
def writhe_OA_Purchaseorder_api(
    process_code: str = "PROC-BFE32FF9-45C3-4EAD-A535-2E154F298663",
    user_id: str = "45415967111121290",
    dept_id: str = "594387273",
    form_data: list = []  # 根据实际需要传入正确格式的数据
):
    # 获取 Access Token
    access_token = get_access_token()
    if not access_token:
        raise HTTPException(status_code=500, detail="无法获取 access_token")
    
    # 提交审批
    result = create_approval_instance(access_token, process_code, user_id, dept_id, form_data)
    
    # 处理结果
    if result.get("errcode") == 0:
        return {"成功": result.get("process_instance_id")}
    else:
        return {"失败": result.get("errmsg")}


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
