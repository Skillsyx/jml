import json
import requests

class DingTalkAPI:
    """ 钉钉 API 封装类 """
    
    def __init__(self, corp_id, corp_secret):
        """
        初始化 DingTalk API
        :param corp_id: 钉钉企业 Corp ID
        :param corp_secret: 钉钉企业应用 Secret
        """
        self.corp_id = corp_id
        self.corp_secret = corp_secret
        self.access_token = self.get_access_token()

    def get_access_token(self):
        """ 获取 Access Token """
        url = "https://oapi.dingtalk.com/gettoken"
        params = {
            "appkey": self.corp_id,
            "appsecret": self.corp_secret
        }
        response = requests.get(url, params=params)
        data = response.json()
        if data.get("errcode") == 0:
            print("✅ 获取 Access Token 成功")
            return data.get("access_token")
        else:
            print("❌ 获取 Access Token 失败:", data.get("errmsg"))
            return None

    def get_approval_status(self, process_instance_id):
        """ 查询审批实例状态 """
        url = "https://oapi.dingtalk.com/topapi/processinstance/get"
        headers = {"Content-Type": "application/json"}
        params = {"access_token": self.access_token}
        data = {"process_instance_id": process_instance_id}
        
        response = requests.post(url, headers=headers, params=params, json=data)
        result = response.json()

        if result.get("errcode") == 0:
            instance_status = result["process_instance"]["status"]
            status_mapping = {
                "RUNNING": "审批进行中",
                "COMPLETED": "审批完成",
                "CANCELED": "审批已取消",
                "TERMINATED": "审批被终止"
            }
            return f"✅ 审批实例状态: {status_mapping.get(instance_status, '未知状态')}"
        else:
            return f"❌ 查询失败: {result.get('errmsg')}"

    def get_user_id_by_mobile(self, mobile):
        """ 通过手机号获取用户 ID """
        url = "https://oapi.dingtalk.com/topapi/v2/user/getbymobile"
        headers = {"Content-Type": "application/json"}
        params = {"access_token": self.access_token}
        data = {"mobile": mobile}
        
        response = requests.post(url, headers=headers, params=params, json=data)
        result = response.json()
        
        if result.get("errcode") == 0:
            return result.get("result", {}).get("userid")
        else:
            print("❌ 获取用户 ID 失败:", result.get("errmsg"))
            return None

    def get_user_info(self, user_id):
        """ 获取用户部门信息 """
        url = "https://oapi.dingtalk.com/topapi/v2/user/get"
        headers = {"Content-Type": "application/json"}
        params = {"access_token": self.access_token}
        data = {"userid": user_id}
        
        response = requests.post(url, headers=headers, params=params, json=data)
        result = response.json()
        
        if result.get("errcode") == 0:
            return result.get("result", {}).get("dept_id_list", [])
        else:
            print("❌ 获取用户部门失败:", result.get("errmsg"))
            return None
