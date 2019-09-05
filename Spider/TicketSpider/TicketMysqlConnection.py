from Lib.Util.Ping import pingIp
from Lib.Connection.MysqlConnection import MysqlConnection
from random import randint


class TicketMysqlConnection(MysqlConnection):

    def __init__(self, ip, username, password, database):
        super().__init__(ip, username, password, database)
        self.ip = None
        self.proxy_port = None
        self.proxy_type = None
        self.flag = True

    def insert_qihao(self, *args, **kwargs):
        sql = "INSERT into qihao(qihao,date) VALUES('%s','%s')" % args
        print("执行sql语句：%s" % sql)
        try:
            # 执行SQL语句
            self.cur.execute(sql)
        except Exception as e:
            raise Exception(e)

    def insert_qian_number(self, *args, **kwargs):
        sql = "INSERT into qian_number(qihap_id,one, two, three, four, five) VALUES('%s','%s','%s','%s','%s','%s')" % args
        print("执行sql语句：%s" % sql)
        try:
            # 执行SQL语句
            self.cur.execute(sql)
        except Exception as e:
            raise Exception(e)

    def insert_hou_number(self, *args, **kwargs):
        sql = "INSERT into hou_number(qihao_id,one, two) VALUES('%s','%s','%s')" % args
        print("执行sql语句：%s" % sql)
        try:
            # 执行SQL语句
            self.cur.execute(sql)
        except Exception as e:
            raise Exception(e)

    def insert_money(self, *args, **kwargs):
        sql = "INSERT into money(one_money,one_number, one_zhui_number, one_zhui_money,two_money, two_number, two_zhui_number, two_zhui_money," \
              "sales_money, sum_money, qihao_id)" \
              " VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % args
        print("执行sql语句：%s" % sql)
        try:
            # 执行SQL语句
            self.cur.execute(sql)
        except Exception as e:
            raise Exception(e)

    def delete(self, ip):
        sql = "update proxy set is_delete = 0 where proxy_ip = '%s'" % ip
        try:
            print("执行sql语句：%s" % sql)
            self.cur.execute(sql)
            print("删除ip：%s" % ip)
        except Exception as e:
            raise Exception(e)

    def findCount(self):
        sql = "select count(*) from proxy where is_delete = 1"
        try:
            self.cur.execute(sql)
            count = self.cur.fetchall()[0][0]
            print("总共有%s条代理ip" % count)
            return count
        except Exception as e:
            raise Exception(e)

    def findOneIp(self):
        if self.ip and self.proxy_type and self.proxy_port and self.flag:
            return self.ip, self.proxy_type, self.proxy_port
        else:
            while True:
                count = self.findCount()
                id = randint(0, count)
                sql = "select proxy_ip,proxy_type,proxy_port from proxy where id = %s and is_delete = 1" % id
                print("执行sql语句:%s" % sql)
                try:
                    self.cur.execute(sql)
                    data = self.cur.fetchall()[0]
                    self.ip = data[0]
                    self.proxy_type = data[1]
                    self.proxy_port = data[2]
                    if pingIp(self.ip):
                        return self.ip, self.proxy_type, self.proxy_port
                    else:
                        print("ip：%s不能使用" % self.ip)
                        self.delete(self.ip)
                except Exception as e:
                    raise Exception(e)
