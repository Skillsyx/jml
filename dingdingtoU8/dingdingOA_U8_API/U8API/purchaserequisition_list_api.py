# purchaseorder_list_api.py
from fastapi import APIRouter, HTTPException
import requests
from datetime import datetime

router = APIRouter()

@router.get("/list")
def get_unverified_porequisition_list_api(
    from_account: str = "JML2021",
    to_account: str = "JML2021",
    app_key: str = "opa3616de88da543d8b",
    token: str = "",
    ds_sequence: int = 8
):

    return get_unverified_porequisition_list(
        from_account=from_account,
        to_account=to_account,
        app_key=app_key,
        token=token,
        ds_sequence=ds_sequence
    )

def get_unverified_porequisition_list(from_account, to_account, app_key, token, ds_sequence, cvoucherstate="开立"):

    now = datetime.now()
    date_begin = f"{now.year}-01-01"  # 可根据需要自定义开始日期
    date_end = now.strftime("%Y-%m-%d")
    url = "	https://api.yonyouup.com/api/purchaserequisitionlist/batch_get"
    params = {
        "from_account": from_account,
        "to_account": to_account,
        "app_key": app_key,
        "token": token,
        "ds_sequence": ds_sequence,
        "date_begin": date_begin,
        "date_end": date_end,
        "cvoucherstate": cvoucherstate
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get("errcode") != "0":
            raise HTTPException(status_code=400, detail=data.get("errmsg", "接口返回错误"))
        purchaserequisitionlist = data.get("purchaserequisitionlist", [])
        order_codes = [order.get("code") for order in purchaserequisitionlist]
        return {"requisition_order_codes": order_codes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
