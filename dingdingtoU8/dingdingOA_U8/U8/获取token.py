import requests

# 你的参数
from_account = "JML2021"
app_key = "opa3616de88da543d8b"
app_secret = "ccbe14b95a4f48f994d9ce27d0263c6e"

# 构造 URL
url = f"https://api.yonyouup.com/system/token?from_account={from_account}&app_key={app_key}&app_secret={app_secret}"

# 发送请求
response = requests.get(url)

# 解析响应
if response.status_code == 200:
    token_data = response.json()
    print(token_data)  # 打印获取的 token
else:
    print("请求失败:", response.status_code, response.text)
# token ea551e110f21411f86691844d34ccde3