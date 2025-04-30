import time
import threading
import redis

# 连接 Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

class TokenManager:
    def __init__(self):
        self.token_key = "shared_api_token"  # Redis 键名
        self.schedule_token_refresh()  # 启动 Token 刷新任务

    def get_token(self):
        """ 获取新的 Token 并存入 Redis """
        token = "new_token_value"  # 这里替换为实际的 Token 获取逻辑
        print("Token 已更新:", token)
        redis_client.setex(self.token_key, 7200 - 300, token)  # 设置 Redis 过期时间
        return token

    def schedule_token_refresh(self):
        """ 定时刷新 Token """
        self.get_token()
        threading.Timer(7200 - 300, self.schedule_token_refresh).start()  # 定时刷新 Token

    def get_current_token(self):
        """ 从 Redis 读取当前 Token """
        return redis_client.get(self.token_key)

# 启动 Token 监听
token_manager = TokenManager()

# 主线程继续执行其他操作
while True:
    time.sleep(10)  # 模拟其他业务逻辑
    print("当前 Token:", token_manager.get_current_token())
