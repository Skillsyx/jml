import requests



# url = "	https://api.yonyouup.com/system/token"
# payload = {
#     "from_account": "JML2021",
#     "app_key": "opa3616de88da543d8b",
#     "app_secret": "ccbe14b95a4f48f994d9ce27d0263c6e"
# }

# response = requests.get(url, params=payload)
# print(response.json())


# url = "http://172.16.1.102:8998/purchaseorder/get"
# data = {
#     "code": "CGDD250342112",  # 采购订单单据号
#     "token": "b371ec65476c4a89ab94997511c486dd" # 传token，其他参数走后端默认值
# }

# response = requests.get(url, params=data)
# print("Status code:", response.json())

url = "http://172.16.1.102:8998/department/get"
data = {
    "token" : "b371ec65476c4a89ab94997511c486dd",
    "depcode": "04505",  # 部门编号

}
response = requests.get(url, params=data)
print("Status code:", response.json())


# url = "http://172.16.1.102:8998/salesorder/list"
# data = {
#     "token": "b371ec65476c4a89ab94997511c486dd", # 传token，其他参数走后端默认值
#     # "voucher_code":"QGD250320004"
# }

# response = requests.get(url, params=data)
# print("Status code:", response.json())


# url = "http://172.16.1.102:8998/salesorder/verify"
# data = {
#     "token": "d3b71721c0754ed7b7b73b968e721324", # 传token，其他参数走后端默认值
#     "voucher_code":"XSDD250311297"
# }

# response = requests.get(url, params=data)
# print("Status code:", response.json())


# url = "http://172.16.1.102:8998/salesorder/get"
# data = {
#     "token": "d3b71721c0754ed7b7b73b968e721324", # 传token，其他参数走后端默认值
#     "code":"XSDD250311297"
# }

# response = requests.get(url, params=data)
# print("Status code:", response.json())





