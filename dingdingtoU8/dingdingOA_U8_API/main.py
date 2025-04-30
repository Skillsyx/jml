# main.py
from fastapi import FastAPI
import uvicorn

# 从两个模块里引入 APIRouter 实例
from purchaseorder_list_api import router as purchaseorder_list_router
from purchaseorder_verify_api import router as purchaseorder_verify_router
from purchaseorder_get_api import router as purchaseorder_get_router
from purchaserequisition_list_api import router as purchaserequisition_list_router
from purchaserequisition_get_api import router as purchaserequisition_get_router
from purchaserequisition_verify_api import router as purchaserequisition_verify_router
from salesorder_list_api import router as salesorder_list_router
from salesorder_verify_api import router as salesorder_verify_router
from salesorder_get_api import router as salesorder_get_router
from department_get_api import router as department_get_router
from create_approval_instance import router as create_approval_instance_router
from select_oa_status import router as select_oa_status_router



app = FastAPI()

# 这里统一挂载路由
# 采购订单模块
app.include_router(purchaseorder_list_router, prefix="/purchaseorder", tags=["PurchaseOrderList"])
app.include_router(purchaseorder_verify_router, prefix="/purchaseorder", tags=["PurchaseOrderVerify"])
app.include_router(purchaseorder_get_router, prefix="/purchaseorder", tags=["PurchaseOrderGet"])
#采购申请模块
app.include_router(purchaserequisition_list_router, prefix="/purchaserequisition", tags=["PurchaseRequisitionList"])
app.include_router(purchaserequisition_get_router, prefix="/purchaserequisition", tags=["PurchaseRequisitionGet"])
app.include_router(purchaserequisition_verify_router, prefix="/purchaserequisition", tags=["PurchaseRequisitionVerify"])
#销售订单模块
app.include_router(salesorder_list_router, prefix="/salesorder", tags=["SalesOrderList"])
app.include_router(salesorder_verify_router, prefix="/salesorder", tags=["SalesOrderVerify"])
app.include_router(salesorder_get_router, prefix="/salesorder", tags=["SalesOrderGet"])
#部门模块
app.include_router(department_get_router, prefix="/department", tags=["DepartmentGet"])

#钉钉OA
app.include_router(create_approval_instance_router, prefix="/createOAPO", tags=["CreateApprovalInstance"])
#查询实例状态
app.include_router(select_oa_status_router, prefix="/selectOAStatus", tags=["SelectOAStatus"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8998, reload=True)
