import pyodbc

class SQLServerDB:
    def __init__(self, server, database, username, password, driver='{ODBC Driver 17 for SQL Server}'):
        """
        初始化数据库连接

        参数:
            server: 服务器地址
            database: 数据库名称
            username: 用户名
            password: 密码
            driver: ODBC 驱动，默认为 {ODBC Driver 17 for SQL Server}
        """
        self.connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        self.conn = None
        self.connect()

    def connect(self):
        """ 建立数据库连接 """
        try:
            self.conn = pyodbc.connect(self.connection_string)
            # 设置自动提交为 False，可根据需求控制事务
            self.conn.autocommit = False
        except Exception as e:
            print("连接数据库失败:", e)
            raise

    def query(self, sql, params=None):
        """
        执行查询操作，并返回结果列表（每条结果为一个字典）。

        参数:
            sql: 查询 SQL 语句
            params: 可选的参数元组或列表

        返回:
            [ {字段名: 值, ...}, ... ]
        """
        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            results = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            data = [dict(zip(columns, row)) for row in results]
            cursor.close()
            return data
        except Exception as e:
            print("查询执行失败:", e)
            raise

    def execute(self, sql, params=None):
        """
        执行 INSERT/UPDATE/DELETE 等非查询 SQL 语句。

        参数:
            sql: SQL 语句
            params: 可选的参数元组或列表

        返回:
            受影响的行数
        """
        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            affected = cursor.rowcount
            self.conn.commit()
            cursor.close()
            return affected
        except Exception as e:
            self.conn.rollback()
            print("执行 SQL 失败:", e)
            raise

    def insert(self, sql, params):
        """
        执行插入操作

        参数:
            sql: 插入 SQL 语句
            params: 插入数据的参数元组或列表

        返回:
            受影响的行数
        """
        return self.execute(sql, params)

    def update(self, sql, params):
        """
        执行更新操作

        参数:
            sql: 更新 SQL 语句
            params: 更新数据的参数元组或列表

        返回:
            受影响的行数
        """
        return self.execute(sql, params)

    def close(self):
        """ 关闭数据库连接 """
        if self.conn:
            self.conn.close()
