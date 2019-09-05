import re
from urllib3.exceptions import NewConnectionError, MaxRetryError
from requests.exceptions import ConnectionError
from Lib.Spider.SpiderBase import SpiderBase
from Lib.Spider.TicketSpider.TicketMysqlConnection import TicketMysqlConnection
from Lib.Spider.ProxySpider.ProxyMysqlConnection import ProxyMysqlConnection
from lxml import etree
import traceback


class TicketNumber:

    def __init__(self, page):
        self.proxy_conn = ProxyMysqlConnection("localhost", "root", "aywan0327", "education")
        self.conn = TicketMysqlConnection("localhost", "root", "aywan0327", "ticket")
        self.page = 'history_%s.jspx?_ltype=dlt' % page
        self.baseUrl = 'http://www.lottery.gov.cn/historykj/'

        self.url = '%s%s' % (self.baseUrl, self.page)
        self.pageHandle()
        self.flag = True

    def pageHandle(self):
        while True:
            context = self.dispacth(url=self.url)
            html = etree.HTML(context)
            self.parseData(html)
            nextPage = html.xpath('//div[@class="page"]/div/a[3]/@href')
            if not nextPage:
                break
            nextPage = nextPage[0]
            self.page = re.search('_(\d+)', nextPage).group(1)
            self.url = "%s%s" % (self.baseUrl, nextPage)
            self.url = self.url.split('&')[0]

        # while True:
        #     if self.page > 94:
        #         return
        #     url = self.url
        #     if self.dispacth(url):
        #         self.page += 1
        #     else:
        #         continue

    def dispacth(self, url):
        print("正在爬取第%s页" % str(self.page))
        print("爬取网址:%s" % url)
        ip, proxy_type, proxy_port = self.proxy_conn.findOneIp()
        proxy_handle = {proxy_type: proxy_type + "://" + ip + ":" + proxy_port}
        print("使用代理为%s" % proxy_handle[proxy_type])
        try:
            spiderBase = SpiderBase(url, proxies=proxy_handle)
            context = spiderBase.parseContext().decode()
            return context
        except TimeoutError as e:
            traceback.print_exc()
            return self.expection(e)
        except NewConnectionError as e:
            traceback.print_exc()
            return self.expection(e)
        except MaxRetryError as e:
            traceback.print_exc()
            return self.expection(e)
        except ConnectionError as e:
            traceback.print_exc()
            return self.expection(e)
        except Exception as e:
            raise Exception(e)

    def parseData(self, html):
        node_lists = html.xpath('//div[@class="result"]/table/tbody/tr')
        for id, node_list in enumerate(node_lists):
            qihao = str(node_list.xpath('./td[1]/text()')[0])
            qian_one = int(node_list.xpath('./td[2]/text()')[0])
            qian_two = int(node_list.xpath('./td[3]/text()')[0])
            qian_three = int(node_list.xpath('./td[4]/text()')[0])
            qian_four = int(node_list.xpath('./td[5]/text()')[0])
            qian_five = int(node_list.xpath('./td[6]/text()')[0])
            hou_one = int(node_list.xpath('./td[7]/text()')[0])
            hou_two = int(node_list.xpath('./td[8]/text()')[0])
            one_number = int(node_list.xpath('./td[9]/text()')[0].replace(',', ''))
            one_money = str(node_list.xpath('./td[10]/text()')[0].replace(',', ''))
            one_zhui_number = int(node_list.xpath('./td[11]/text()')[0].replace(',', ''))
            one_zhui_money = str(node_list.xpath('./td[12]/text()')[0].replace(',', ''))
            two_number = int(node_list.xpath('./td[13]/text()')[0].replace(',', ''))
            two_money = str(node_list.xpath('./td[14]/text()')[0].replace(',', ''))
            two_zhui_number = int(node_list.xpath('./td[15]/text()'.replace(',', ''))[0])
            two_zhui_money = str(node_list.xpath('./td[16]/text()')[0].replace(',', ''))
            sales_money = str(node_list.xpath('./td[18]/text()')[0].replace(',', ''))
            sum_money = str(node_list.xpath('./td[19]/text()')[0].replace(',', ''))
            date = str(node_list.xpath('./td[20]/text()')[0])
            self.conn.insert_qihao(qihao, date)
            qihao_id = id + 1
            self.conn.insert_qian_number(qihao_id, qian_one, qian_two, qian_three, qian_four, qian_five)
            self.conn.insert_hou_number(qihao_id, hou_one, hou_two)
            self.conn.insert_money(one_money, one_number, one_zhui_number, one_zhui_money, two_money, two_number,
                                   two_zhui_number, two_zhui_money, sales_money, sum_money, qihao_id)

    def expection(self, e):
        self.conn.flag = False
        self.proxy_conn.flag = False
        print("[ERROR]:%s" % e)
        return self.conn.flag


if __name__ == '__main__':
    p = TicketNumber(1)
