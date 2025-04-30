import snap7
import time
from db_handler import insert_plc_data

def read_plc_data():
    # 创建PLC客户端实例
    plc = snap7.client.Client()
    retry_delay = 5
    attempt = 0  # 初始化重试计数器
    
    while True:  # 无限重试
        try:
            # 连接到PLC
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(f"[{current_time}] 尝试连接到PLC (第{attempt + 1}次尝试)...")
            plc.connect('192.168.1.20', 0, 1)
            print("成功连接到PLC")
            
            db17 = plc.db_read(17, 44, 4)  # DINT占用4字节
            db19 = plc.db_read(19, 10, 2)  # INT占用2字节
            initial_value = int.from_bytes(db17, byteorder='big', signed=True)
            
            while True:
                try:
                   
                    
                    value1 = int.from_bytes(db17, byteorder='big', signed=True)
                    
                    
                    value2 = int.from_bytes(db19, byteorder='big', signed=True)

                    if value2 >= 1000:
                        # 记录抓取时间
                        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        
                        while True:
                            try:
                               
                                value3 = int.from_bytes(db17, byteorder='big', signed=True)
                               
                                value4 = int.from_bytes(db19, byteorder='big', signed=True)

                                if value4 == 0:
                                    # 记录放下时间
                                    now2 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                                    # 插入数据到数据库
                                    insert_plc_data(
                                        initial_value=initial_value,
                                        current_value=value3,
                                        capture_time=now,
                                        drop_time=now2,
                                        production_line='生产线1'
                                    )
                                    break
                                
                                time.sleep(1)
                            except snap7.snap7exceptions.Snap7Exception as e:
                                print(f"读取错误: {str(e)}")
                                time.sleep(1)
                    
                    print(f"DB17.DBD44的值为: {value1}, DB19.DBW10的值为: {value2}")
                    time.sleep(1)  # 每秒读取一次
                    
                except snap7.snap7exceptions.Snap7Exception as e:
                    print(f"读取错误: {str(e)}")
                    time.sleep(1)
                    
            return  # 如果内部循环正常结束，退出函数
                    
        except Exception as e:
            print(f"连接错误 (第{attempt + 1}次尝试): {str(e)}")
            print(f"等待{retry_delay}秒后重试...")
            time.sleep(retry_delay)
            attempt += 1  # 增加重试计数
        finally:
            plc.disconnect()

if __name__ == "__main__":
    read_plc_data()