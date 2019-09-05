import os


def pingIp(ip):
    ret = os.popen("ping %s" % ip).read()
    if "TTL" in ret and "ms" in ret:
        return True
    else:
        return False
