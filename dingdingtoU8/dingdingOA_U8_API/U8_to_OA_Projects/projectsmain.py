import requests
import json
import ast
from sqlserverdb import SQLServerDB
from U8_to_OA import * 
import time
from datetime import datetime

server = '172.16.1.9'
database = 'yx_test'
username = 'sa'
password = 'Ks123456'

db = SQLServerDB(server, database, username, password)


sql_query = "select * from DingDing_U8OrderSync_yx where status is null"



#获取U8 token
def get_U8token():
    url = "	https://api.yonyouup.com/system/token"
    payload = {
        "from_account": "JML2021",
        "app_key": "opa3616de88da543d8b",
        "app_secret": "ccbe14b95a4f48f994d9ce27d0263c6e"    
    }
    response = requests.get(url, params=payload)
    print(response.json())

    return response.json()['token']['id']

U8token = get_U8token()

results = db.query(sql_query)
print(results)
if not results:




    # 获取采购订单列表
    polist = get_POorderList(U8token)


    # 获取采购订单详情 并写入OA ，数据库记录
    for order in polist:
        now = datetime.now()

        podetails = get_POorderDetail(U8token, order)


        pos_js = json.dumps(podetails, ensure_ascii=False)



        abc = writhe_OA(pos_js)

        sql_insert = """
        INSERT INTO DingDing_U8OrderSync_yx
            (OrderType, OrderNumber, WriteTime, DingTalkInstanceId, Status, Company)
        VALUES 
            (?, ?, ?, ?, ?, ?)"""
        insert_params = ('采购订单', order, now,abc.get('成功')['process_instance_id'],None,'008')
        rows_inserted = db.insert(sql_insert, insert_params)
        print("插入行数：", rows_inserted)
elif results:
    for result in results:
        res = select_OA_status(result['DingTalkInstanceId'])
        print(res)
        if res.get('success') == True and res.get('status')== '审批完成':
            sql_update = "update DingDing_U8OrderSync_yx set status = '审批完成' where DingTalkInstanceId = ?"
            update_params = (result['DingTalkInstanceId'])
            rows_updated = db.update(sql_update, update_params)
            print("更新行数：", rows_updated)
        else:
            continue

# 获取采购订单列表
    polist = get_POorderList(U8token)


    # 获取采购订单详情 并写入OA ，数据库记录
    for order in polist:
        now = datetime.now()

        podetails = get_POorderDetail(U8token, order)


        pos_js = json.dumps(podetails, ensure_ascii=False)



        abc = writhe_OA(pos_js)

        sql_insert = """
        INSERT INTO DingDing_U8OrderSync_yx
            (OrderType, OrderNumber, WriteTime, DingTalkInstanceId, Status, Company)
        VALUES 
            (?, ?, ?, ?, ?, ?)"""
        insert_params = ('采购订单', order, now,abc.get('成功')['process_instance_id'],None,'008')
        rows_inserted = db.insert(sql_insert, insert_params)
        print("插入行数：", rows_inserted)
    

            



# U8token = get_U8token()


# # 获取采购订单列表
# polist = get_POorderList(U8token)


# # 获取采购订单详情 并写入OA ，数据库记录
# for order in polist:
#     podetails = get_POorderDetail(U8token, order)


#     pos_js = json.dumps(podetails, ensure_ascii=False)
#     print(type(pos_js))


#     abc = writhe_OA(pos_js)
#     print(abc)


