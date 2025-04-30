# purchaseorder_list_api.py
from fastapi import APIRouter, HTTPException
import requests
from datetime import datetime

router = APIRouter()

@router.get("/list")
def get_unverified_sales_order_list_api(
    from_account: str = "JML2021",
    to_account: str = "JML2021",
    app_key: str = "opa3616de88da543d8b",
    token: str = "",
    ds_sequence: int = 8
):

    return get_unverified_sales_order_list(
        from_account=from_account,
        to_account=to_account,
        app_key=app_key,
        token=token,
        ds_sequence=ds_sequence
    )

def get_unverified_sales_order_list(from_account, to_account, app_key, token, ds_sequence, state="Opening"):
    # Opening  开立
    # Approved  审核
    # Changing  变更

    now = datetime.now()
    date_begin = f"{now.year}-01-01"  # 可根据需要自定义开始日期
    date_end = now.strftime("%Y-%m-%d")
    url = "https://api.yonyouup.com/api/saleorderlist/batch_get"
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
        saleorderlist = data.get("saleorderlist", [])
        order_codes = [order.get("code") for order in saleorderlist]
        return {"order_codes": order_codes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
