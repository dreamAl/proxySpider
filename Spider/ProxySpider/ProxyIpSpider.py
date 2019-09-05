import re
from urllib3.exceptions import NewConnectionError, MaxRetryError
from requests.exceptions import ConnectionError
from Lib.Spider.SpiderBase import SpiderBase
from Lib.Spider.ProxySpider.ProxyMysqlConnection import ProxyMysqlConnection


class ProxyIpSpider:

    def __init__(self, url, page=1):
        self.conn = ProxyMysqlConnection("localhost", "root", "aywan0327", "education")
        self.page = page
        self.url = url
        self.pageHandle()
        self.flag = True

    def pageHandle(self):
        while True:
            if self.page > 2716:
                return
            # url = self.url + str(self.page)
            url = self.url
            if self.dispacth(url):
                self.page += 1
            else:
                continue

    def dispacth(self, url):
        print("正在爬取第%s页" % self.page)
        print("爬取网址:%s" % url)
        ip, proxy_type, proxy_port = self.conn.findOneIp()
        proxy_handle = {proxy_type: proxy_type + "://" + ip + ":" + proxy_port}
        print("使用代理为%s" % proxy_handle[proxy_type])
        try:
            spiderBase = SpiderBase(url, proxies=proxy_handle)
            context = spiderBase.parseContext().decode()
            self.parseData(context)
            return True
        except TimeoutError:
            return self.expection()
        except NewConnectionError:
            return self.expection()
        except MaxRetryError:
            return self.expection()
        except ConnectionError:
            return self.expection()
        except Exception:
            return self.expection()

    def parseData(self, context):
        pattern = re.compile("<tr>(.*?)</tr>", re.S)
        list_res = pattern.findall(context)
        pattern_ip = re.compile('<td data-title="IP">(.*)</td>')
        pattern_port = re.compile('<td data-title="PORT">(.*)</td>')
        pattern_anonymous = re.compile('<td data-title="匿名度">(.*)</td>')
        pattern_type = re.compile('<td data-title="类型">(.*)</td>')
        pattern_adress = re.compile('<td data-title="位置">(.*)</td>')
        pattern_speed = re.compile('<td data-title="响应速度">(.*)</td>')
        pattern_time = re.compile('<td data-title="最后验证时间">(.*)</td>')
        for data in list_res[2:]:
            ip = pattern_ip.search(data).group(1)
            port = pattern_port.search(data).group(1)
            anonymous = pattern_anonymous.search(data).group(1)
            ip_type = pattern_type.search(data).group(1)
            adress = pattern_adress.search(data).group(1)
            speed = pattern_speed.search(data).group(1)
            time = pattern_time.search(data).group(1)
            print("第{}页".format(self.page), ip, port, anonymous, ip_type, adress, speed, time)
            self.conn.insert(ip, port, anonymous, ip_type, adress, speed, time)

    def expection(self):
        self.conn.flag = False
        return self.conn.flag


if __name__ == '__main__':
    p = ProxyIpSpider("https://www.kuaidaili.com/free/inha/", 521)
