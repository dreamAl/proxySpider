from Lib.Util.Ping import pingIp
from Lib.Connection.MysqlConnection import MysqlConnection
from random import randint
import traceback

class ProxyMysqlConnection(MysqlConnection):

    def __init__(self, ip, username, password, database):
        super().__init__(ip, username, password, database)
        self.ip = None
        self.proxy_port = None
        self.proxy_type = None
        self.flag = True

    def insert(self, *args, **kwargs):
        sql = "INSERT into proxy(proxy_ip,proxy_port,proxy_anonymous,proxy_type,proxy_address,proxy_speed,proxy_time," \
              "is_delete) VALUES('%s','%s','%s','%s','%s','%s','%s',1)" % args
        print("执行sql语句：%s" % sql)
        try:
            # 执行SQL语句
            self.cur.execute(sql)
        except:
            print("Error: unable to fetch data")

    def delete(self, ip):
        sql = "update proxy set is_delete = 0 where proxy_ip = '%s'" % ip
        try:
            print("执行sql语句：%s" % sql)
            self.cur.execute(sql)
            print("删除ip：%s" % ip)
        except:
            print("data delete error")

    def findCount(self):
        sql = "select id from proxy where is_delete = 1"
        try:
            self.cur.execute(sql)
            ret = self.cur.fetchall()
            count = ret[0][0]
            print("总共有%s条代理ip" % count)
            return count
        except:
            print("data find error")

    def findOneIp(self):
        if self.ip and self.proxy_type and self.proxy_port and self.flag:
            return self.ip, self.proxy_type, self.proxy_port
        else:
            while True:
                id = self.findCount()
                sql = "select proxy_ip,proxy_type,proxy_port from proxy where id = %s and is_delete = 1" % id
                print("执行sql语句:%s" % sql)
                try:
                    self.cur.execute(sql)
                    ret = self.cur.fetchall()
                    print(ret),11111111111111
                    data = ret[0]
                    self.ip = data[0]
                    self.proxy_type = data[1]
                    self.proxy_port = data[2]
                    if pingIp(self.ip):
                        return self.ip, self.proxy_type, self.proxy_port
                    else:
                        print("ip：%s不能使用" % self.ip)
                        self.delete(self.ip)
                except Exception as e:
                    traceback.print_exc()
                    print("data opearte error")
