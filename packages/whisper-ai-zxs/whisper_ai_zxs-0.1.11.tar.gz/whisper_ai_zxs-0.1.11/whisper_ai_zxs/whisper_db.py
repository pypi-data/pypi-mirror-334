import pymysql

class WhisperDB:
    def __init__(self):
        self.connection = pymysql.connect(host='172.27.0.4',
                                          user='RPA',
                                          password='Zxs123',
                                          database='zxs_order')

    def query(self, sql, params=None):
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, params or ())
            return cursor.fetchall()
        finally:
            cursor.close()  # 确保游标关闭

    def commit(self):
        self.connection.commit()

    def get_cursor(self):
        return self.connection.cursor()

    def close(self):
        self.connection.close()

    # 实现上下文管理协议
    def __enter__(self):
        # 返回数据库连接对象本身（或其他资源）
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # 在退出时自动关闭连接
        self.close()
        # 如果有异常，可以处理
        if exc_type:
            print(f"Error: {exc_value}")