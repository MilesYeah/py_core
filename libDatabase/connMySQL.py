import pymysql

from handlerLogger import logger

"""
host
user
password
database
port
"""


class ConnMySQL(object):
    def __init__(self, host, user, password, database=None, port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port

    # 实现with方法
    def __enter__(self):
        try:
            # 建立数据库连接
            self.db = pymysql.Connect(host=host,
                                      user=user,
                                      password=password,
                                      database=database,
                                      port=int(port))

            # 使用 cursor 方法获取操作游标，得到一个可以执行sql语句，并且操作结果为字典返回的游标
            self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
            # self.cursor = self.db.cursor()
        except TimeoutError as e:
            logger.error(f'数据库链接超时请检查：{e}')
            raise TimeoutError(f'数据库链接超时请检\n{e}')
        except IndentationError as e:
            logger.error('数据库链接用户名不存在请检查')
            raise IndentationError(f"数据库链接用户名不存在请检查\n{e}")
        except pymysql.err.OperationalError as e:
            logger.error(f'用户名或密码错误请检查\n{e}')
            raise pymysql.err.OperationalError('用户名或密码错误请检查')

        return self

    # 自动关闭
    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            # 关闭游标
            self.cursor.close()
            # 关闭连接
            self.db.close()
        except Exception as e:
            logger.error(f"数据库关闭失败：{e}")

    def execute(self, sql: str):
        """
        更新 、 删除、 新增
        :param sql:
        :return:
        """
        try:
            # 使用 execute 操作 sql
            rows = self.cursor.execute(sql)
            # 提交事务
            self.db.commit()
            return rows
        except Exception as e:
            logger.error(f"数据库连接失败，失败原因{e}")
            # 如果事务异常，则回滚数据
            self.db.rollback()

    # 查询单条数据并且返回 可以通过sql查询指定的值 也可以通过索引去选择指定的值
    def fetch_one(self, sql, name=None):
        # 修改返回值为数组键值对
        try:
            # 按照sql进行查询
            self.cursor.execute(sql)
            if name is None:
                # 返回一条数据 还有 all size（自己控制）
                sql_data = self.cursor.fetchone()
                return sql_data
            elif name is not None:
                sql_data = self.cursor.fetchone()
                return sql_data[name]
        except pymysql.err.ProgrammingError as e:
            logger.error(f"请检查sql是否正确 sql={sql}")
            raise e

    def fetch_all(self, sql):  # 查询多条数据并且返回
        try:
            # 按照sql进行查询
            self.cursor.execute(sql)
            # 返回一条数据 还有 all size（自己控制）
            sql_data = self.cursor.fetchall()
        except pymysql.err.ProgrammingError as e:
            logger.error(f"请检查sql是否正确 sql={sql}")
            raise e
        return sql_data

    def insert_data(self, sql):
        cursor = self.db.cursor()
        try:
            # 执行sql
            cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
        except pymysql.err.ProgrammingError as e:
            logger.error(f"请检查sql是否正确 sql={sql}")
            raise e

    def update_data(self, sql):
        cursor = self.db.cursor()
        try:
            # 执行sql
            cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
        except pymysql.err.ProgrammingError as e:
            logger.error(f"请检查sql是否正确 sql={sql}")
            raise e

    def delete(self, sql, params=()):
        pass


if __name__ == '__main__':
    host, user, password, database, port = "192.168.123.57", "root", "Aa123456", "school",  3306

    sql = "select ID from tem_platform.ip_district where P_ID = 10801;"
    with ConnMySQL(host, user, password, database, port) as db:
        value = db.fetch_all(sql)
    print(value)
