from ding_api import DingTalkAPI

# **初始化 API**
ding_api = DingTalkAPI(
    corp_id="dingg4komkiirlidfnag",
    corp_secret="WcrjxsKA8Jay95sbge_wF5njoK7f6WR7CYqpMswYbIZwv_45xLDq2ZDzjAMWCS0U"
)

# **获取审批状态**
process_instance_id = "H5aBCJ4hSVW7Tmq485KLSQ04501741306798"
print(ding_api.get_approval_status(process_instance_id))

# **通过手机号获取用户 ID**
mobile_number = "18556785498"
user_id = ding_api.get_user_id_by_mobile(mobile_number)
print("用户 ID:", user_id)

# **获取用户部门**
if user_id:
    dept_info = ding_api.get_user_info(user_id)
    print("用户部门 ID:", dept_info)
