import pyodbc
import time

def insert_plc_data(initial_value, current_value, capture_time, drop_time, production_line):
    # 数据库连接参数
    server = '172.16.1.9'
    database = 'YX_test'
    username = 'sa'
    password = 'Ks123456'
    
    # 构建连接字符串
    conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    
    try:
        # 建立数据库连接
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        # 准备SQL插入语句
        sql = """INSERT INTO PLC_Run_Records_yx 
               (InitialValue, CurrentValue, CaptureTime, DropTime, ProductionLine)
               VALUES (?, ?, ?, ?, ?)"""
        
        # 执行插入操作
        cursor.execute(sql, (initial_value, current_value, capture_time, drop_time, production_line))
        conn.commit()
        
        print("数据插入成功")
        
    except pyodbc.Error as e:
        print(f"数据库错误: {str(e)}")
    except Exception as e:
        print(f"发生错误: {str(e)}")
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

def main():
    # 测试插入函数
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    insert_plc_data(
        initial_value=100,
        current_value=200,
        capture_time=current_time,
        drop_time=current_time,
        production_line='测试生产线'
    )

if __name__ == "__main__":
    main()