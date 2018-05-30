# 获取爬虫地址
def getUrlOfSogou(catalogName, page=1):
    info = [
        'http://pic.sogou.com/pics?query=',
        catalogName,
        '&reqType=ajax&start=',
        str(page)
    ]
    return ''.join(info)
