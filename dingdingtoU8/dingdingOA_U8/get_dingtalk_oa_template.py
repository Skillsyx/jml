import requests

# 钉钉开放平台API地址
DINGTALK_API_URL = 'https://oapi.dingtalk.com'

# 获取审批模板的API路径
GET_APPROVAL_TEMPLATE_PATH = '/topapi/process/get_by_name'

# 企业CorpId和CorpSecret
CORP_ID = 'dingg4komkiirlidfnag'
CORP_SECRET = 'WcrjxsKA8Jay95sbge_wF5njoK7f6WR7CYqpMswYbIZwv_45xLDq2ZDzjAMWCS0U'

# 获取Access Token
def get_access_token():
    url = f'{DINGTALK_API_URL}/gettoken?corpid={CORP_ID}&corpsecret={CORP_SECRET}'
    response = requests.get(url)
    return response.json().get('access_token')

# 获取审批模板
def get_approval_template(template_name):
    access_token = get_access_token()
    url = f'{DINGTALK_API_URL}{GET_APPROVAL_TEMPLATE_PATH}?access_token={access_token}'
    params = {
        'process_name': template_name,
        'name': template_name
    }
    response = requests.post(url, json=params)
    return response.json()

if __name__ == '__main__':
    template_name = 'test'
    result = get_approval_template(template_name)
    print(result)