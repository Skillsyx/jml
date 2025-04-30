import requests

# API 访问参数
from_account = "JML2021"
to_account = "JML2021"
app_key = "opa3616de88da543d8b"
token = "ea551e110f21411f86691844d34ccde3"
order_id = "CGDD250342112"  # 替换为实际的订单编号
ds_sequence = 8  # 数据源序号，可选

# 构造 URL
url = f"https://api.yonyouup.com/api/purchaseorder/get?from_account={from_account}&to_account={to_account}&app_key={app_key}&token={token}&id={order_id}&ds_sequence={ds_sequence}"

# 发送请求
response = requests.get(url)

# 解析响应
if response.status_code == 200:
    order_data = response.json()
    print(order_data)  # 输出订单信息
else:
    print("请求失败:", response.status_code, response.text)
