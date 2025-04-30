import requests
import json
import ast
from datetime import datetime
from sqlserverdb import SQLServerDB
from U8_to_OA import *  # 包含 get_POorderList, get_POorderDetail, writhe_OA, select_OA_status 等函数
import time

# SQL Server 连接参数
server = '172.16.1.9'
database = 'yx_test'
username = 'sa'
password = 'Ks123456'

# 初始化数据库连接
db = SQLServerDB(server, database, username, password)

# 查询待处理记录（status IS NULL）的 SQL
sql_query = "SELECT * FROM DingDing_U8OrderSync_yx WHERE status IS NULL"

# 获取U8 Token
def get_U8token():
    url = "https://api.yonyouup.com/system/token"
    payload = {
        "from_account": "JML2021",
        "app_key": "opa3616de88da543d8b",
        "app_secret": "ccbe14b95a4f48f994d9ce27d0263c6e"
    }
    response = requests.get(url, params=payload)
    token_json = response.json()

    return token_json['token']['id']

U8token = get_U8token()

# 查询数据库中待处理的订单记录
results = db.query(sql_query)
print("当前待处理记录：", results)

# 提取已存在的订单号列表
existing_orders = [r['OrderNumber'] for r in results] if results else []
print ("已存在的订单号：", existing_orders)

# 如果没有待处理记录，则直接插入新订单数据
if not results:
    polist = get_POorderList(U8token)  # 假设返回订单号列表
    if not polist:
        print("当前没有未审核的订单，无需处理。")
    else:
        print("当前未审核的订单：", polist)
        for order in polist:
            if order in existing_orders:
                # 若订单已经存在，跳过插入
                continue
            now = datetime.now()
            podetails = get_POorderDetail(U8token, order)
            # 将订单详情转换为 JSON 字符串（可选，依据 writhe_OA 函数的要求）
            pos_js = json.dumps(podetails, ensure_ascii=False)
            # 调用 OA 接口写入审批
            abc = writhe_OA(pos_js)
            # 从返回信息中提取 process_instance_id
            process_instance_id = abc.get('成功')['process_instance_id']
            
            sql_insert = """
            INSERT INTO DingDing_U8OrderSync_yx
                (OrderType, OrderNumber, WriteTime, DingTalkInstanceId, Status, Company)
            VALUES 
                (?, ?, ?, ?, ?, ?)
            """
            insert_params = ('采购订单', order, now, process_instance_id, None, '008')
            rows_inserted = db.insert(sql_insert, insert_params)
            print("插入订单 %s, 行数：%s" % (order, rows_inserted))
else:
    # 如果存在待处理记录，先对这些记录做状态更新（审批完成的记录）
    for result in results:
        res = select_OA_status(result['DingTalkInstanceId'])
        print("查询OA状态返回：", res)
        # 如果OA接口返回 success 为 True 且状态为 '审批完成'
        if res.get('success') == True and res.get('status') == '审批完成':
            sql_update = "UPDATE DingDing_U8OrderSync_yx SET status = '审批完成' WHERE DingTalkInstanceId = ?"
            # 注意单个参数要写成元组形式：(value,)
            update_params = (result['DingTalkInstanceId'],)
            rows_updated = db.update(sql_update, update_params)
            print("更新 DingTalkInstanceId %s, 行数：%s" % (result['DingTalkInstanceId'], rows_updated))
            a = audit_POorder(U8token, result['OrderNumber'])
            print("审核采购订单返回：", a)
        else:
            # 对于其他状态，这里不做更新，直接跳过
            continue

    # 再重新获取最新的采购订单列表，插入新订单（排除已存在订单）
# 获取订单列表
    polist = get_POorderList(U8token)
    if not polist:
        print("当前没有未审核的订单，无需处理。")
    else:
        # 如果存在未审核订单，则进行处理
        # 可在这里加上后续获取订单详情、调用 OA 接口、写入数据库等逻辑
        for order in polist:
            if order in existing_orders:
                # 若订单已经存在，跳过插入
                continue
            now = datetime.now()
            podetails = get_POorderDetail(U8token, order)
            pos_js = json.dumps(podetails, ensure_ascii=False)
            abc = writhe_OA(pos_js)
            process_instance_id = abc.get('成功')['process_instance_id']
            sql_insert = """
                INSERT INTO DingDing_U8OrderSync_yx
                    (OrderType, OrderNumber, WriteTime, DingTalkInstanceId, Status, Company)
                VALUES 
                    (?, ?, ?, ?, ?, ?)
            """
            insert_params = ('采购订单', order, now, process_instance_id, None, '008')
            rows_inserted = db.insert(sql_insert, insert_params)
            print("插入订单 %s, 行数：%s" % (order, rows_inserted))
        
# 你可以根据需要在任务中加上 time.sleep() 或其他调度逻辑
db.close()  # 最后关闭数据库连接
