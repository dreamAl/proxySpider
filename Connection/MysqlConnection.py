import pymysql


class MysqlConnection():

    def __init__(self, ip, username, password, database):
        self.conn = pymysql.connect(ip, username, password, database)
        self.cur = self.conn.cursor()
        self.conn.autocommit(True)

    def close(self):
        self.cur.close()
        self.conn.close()

    def insert(self, *args, **kwargs):
        pass

    def delect(self, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        pass

    def select(self, *args, **kwargs):
        pass
