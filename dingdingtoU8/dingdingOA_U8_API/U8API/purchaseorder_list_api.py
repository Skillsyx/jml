# purchaseorder_list_api.py
from fastapi import APIRouter, HTTPException
import requests
from datetime import datetime

router = APIRouter()

@router.get("/list")
def get_unverified_purchase_order_list_api(
    from_account: str = "JML2021",
    to_account: str = "JML2021",
    app_key: str = "opa3616de88da543d8b",
    token: str = "",
    ds_sequence: int = 8
):
    """
    查询在用友系统中未审核的采购订单列表
    """
    return get_unverified_purchase_order_list(
        from_account=from_account,
        to_account=to_account,
        app_key=app_key,
        token=token,
        ds_sequence=ds_sequence
    )

def get_unverified_purchase_order_list(from_account, to_account, app_key, token, ds_sequence, state="开立"):
    """
    从用友开放平台接口，获取特定状态（默认“开立”）的采购订单列表
    """
    now = datetime.now()
    date_begin = f"{now.year}-01-01"  # 可根据需要自定义开始日期
    date_end = now.strftime("%Y-%m-%d")
    url = "https://api.yonyouup.com/api/purchaseorderlist/batch_get"
    params = {
        "from_account": from_account,
        "to_account": to_account,
        "app_key": app_key,
        "token": token,
        "ds_sequence": ds_sequence,
        "page_index": 1,
        "rows_per_page": 8000,
        "date_begin": date_begin,
        "date_end": date_end,
        "state": state
        
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get("errcode") != "0":
            raise HTTPException(status_code=400, detail=data.get("errmsg", "接口返回错误"))
        purchaseorderlist = data.get("purchaseorderlist", [])
        order_codes = [order.get("code") for order in purchaseorderlist]
        if not order_codes:
            return {"order_codes": []}  # 如果没有订单，返回空列
        return {"order_codes": order_codes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
