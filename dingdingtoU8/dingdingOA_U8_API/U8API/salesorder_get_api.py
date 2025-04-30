# salesorder_list_api.py
from fastapi import APIRouter, HTTPException
import requests
from datetime import datetime

router = APIRouter()

@router.get("/get")
def get_sales_order_get_api(
    from_account: str = "JML2021",
    to_account: str = "JML2021",
    app_key: str = "opa3616de88da543d8b",
    token: str = "",
    ds_sequence: int = 8,
    code: str = ""
):

    return get_sales_order_get(
        from_account=from_account,
        to_account=to_account,
        app_key=app_key,
        token=token,
        ds_sequence=ds_sequence,
        ids=code
    )

def get_sales_order_get(from_account, to_account, app_key, token, ds_sequence, ids):

   
    url = "	https://api.yonyouup.com/api/saleorder/get"
    params = {
        "from_account": from_account,
        "to_account": to_account,
        "app_key": app_key,
        "token": token,
        "ds_sequence": ds_sequence,
        "id": ids
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get("errcode") != "0":
            raise HTTPException(status_code=400, detail=data.get("errmsg", "接口返回错误"))
        saleorder = data.get("saleorder")
        
        return {"order_codes": saleorder}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
