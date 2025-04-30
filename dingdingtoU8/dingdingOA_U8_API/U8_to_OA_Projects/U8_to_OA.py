import requests


#获取U8 采购订单列表
def get_POorderList(U8token):

    url = "http://172.16.1.102:8998/purchaseorder/list"
    params = {
        "token": U8token  # 仅传token，其他参数走后端默认值
    }

    response = requests.get(url, params=params)
    #判断response.json()有没有detail字段

    if response.json().get("detail") and response.json()["detail"].startswith("400"):
        return []


    code = response.json()["order_codes"]

    return code


#根据采购订单号获取采购订单详情
def get_POorderDetail(U8token,code):

    url = "http://172.16.1.102:8998/purchaseorder/get"
    data = {
        "code": code,  # 采购订单单据号
        "token": U8token # 传token，其他参数走后端默认值
    }

    response = requests.get(url, params=data)
    purchaseorder = response.json().get("order_codes")
    #返回json格式
    return purchaseorder

#审核U8采购订单
def audit_POorder(U8token,code):

    url = "http://172.16.1.102:8998/purchaseorder/verify"
    data = {
        "voucher_code": code,  # 采购订单单据号
        "token": U8token # 传token，其他参数走后端默认值
    }

    response = requests.get(url, params=data)
    return response.json()

def writhe_OA(form_dataa):
    url = "http://172.16.1.102:8998/createOAPO/oa/submit"
    # data = {
    #     "form_dataa": form_dataa,  # 采购订单单据号
    # }
    response = requests.post(url, json=form_dataa)

    return response.json()

def select_OA_status(process_instance_id):
    url = "http://172.16.1.102:8998/selectOAStatus/oa/status"
    params = {
        "process_instance_id": process_instance_id,  # 采购订单单据号
    }
    response = requests.get(url, params=params)
    return response.json()
