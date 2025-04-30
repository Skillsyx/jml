from fastapi import APIRouter, HTTPException
import requests

router = APIRouter()

@router.get("/verify")
def verify_api(
    voucher_code: str = "",
    token: str = "",
    from_account: str = "JML2021",
    to_account: str = "JML2021",
    app_key: str = "opa3616de88da543d8b",
    ds_sequence: int = 8
):

    result = verify_sales_order(
        voucher_code=voucher_code,
        token=token,
        from_account=from_account,
        to_account=to_account,
        app_key=app_key,
        ds_sequence=ds_sequence
    )
    if result.get("errcode") != "0":
        raise HTTPException(status_code=400, detail=result.get("errmsg"))
    return result

def verify_sales_order(voucher_code, token, from_account, to_account, app_key, ds_sequence):

    url = "https://api.yonyouup.com/api/saleorder/verify"
    params = {
        "from_account": from_account,
        "to_account": to_account,
        "app_key": app_key,
        "token": token,
        "ds_sequence": ds_sequence
    }
    data = {
        "saleorder": {
            "voucher_code": voucher_code
        }
    }

    try:
        response = requests.post(url, params=params, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        error_detail = str(e)
        if 'response' in locals() and response is not None:
            error_detail += response.text
        raise HTTPException(status_code=500, detail=error_detail)
