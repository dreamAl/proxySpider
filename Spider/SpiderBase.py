import requests


class SpiderBase(object):

    def __init__(self, url,**kwargs):
        self.url = url
        self.kwargs = kwargs

    @property
    def request(self):
        return requests

    def getContext(self, url):
        request = self.request.get(url,self.kwargs).content
        return request

    def parseContext(self):
        context = self.getContext(self.url)
        return context

    def writeText(self, fileName, data):
        with open(fileName, "wb")as f:
            f.write(data)


if __name__ == '__main__':
    s = SpiderBase("https://www.kuaidaili.com/free/inha/1/")
    s.parseContext()
    s.writeText("1.html", s.parseContext())
