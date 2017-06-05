# coding=utf-8

import requests
from lxml import etree
import json
from pymongo import MongoClient
import time

if __name__ == '__main__':

    client = MongoClient('192.168.1.102', 27017)
    db_name = 'doubandongxi'
    db = client[db_name]
    collectionDongxi = db['dongxi']

    def current_milli_time():
        return int(round(time.time() * 1000))


    now = current_milli_time()

    def tomongo(ptitle, ppid, doulistcount, likenum, postnum):
        doc = collectionDongxi.find({"_id": ppid})
        if doc:
            collectionDongxi.update({'_id': ppid},
                                    {'$push': {"douListCounts": {"douListCount": doulistcount, "tern": now}}})

            collectionDongxi.update({'_id': ppid},
                                    {'$push': {"likeNums": {"likeNum": likenum, "tern": now}}})

            collectionDongxi.update({'_id': ppid},
                                    {'$push': {"postNums": {"postNum": postnum, "tern": now}}})
        else:
            collectionDongxi.insert({'_id': ppid,
                                     'title': ptitle,
                                     'douListCounts': [{"douListCount": doulistcount, "tern": now}],
                                     'likeNums': [{'likeNum': likenum, 'tern': now}],
                                     'postNums': [{'postNum': postnum, 'tern': now}]
                                     })

    # 同步加载的前21条数据。暂时使用下方异步加载方式。
    '''
    response = requests.get("https://dongxi.douban.com/search?q=%E9%93%B6%E9%A5%B0")
    text = response.text

    html = etree.HTML(text)

    targeElements = html.xpath("//*[@id='J_CardListBox']/ul/li")
    print len(targeElements)

    for targetElement in targeElements:
        idStr = targetElement.xpath("div[1]/div[2]/div[3]/@data-eqid")[0]
        douListStr = targetElement.xpath("div[1]/div[2]/div[3]/ul/li[1]")[0].text
        likeStr = targetElement.xpath("div[1]/div[2]/div[3]/ul/li[2]")[0].text
        commentStr = targetElement.xpath("div[1]/div[2]/div[3]/ul/li[3]")[0].text

        _id = idStr.replace("'", "")
        _id = idStr.replace("[", "")
        _id = idStr.replace("]", "")

        douList = douListStr[5:]
        like = likeStr[3:]
        comment = commentStr[3:]

        print _id
        print douList
        print like
        print comment
        print "\n"
    '''

    totalCount = 0
    # 异步加载的数据:5000*21≈10w条
    plan = 1480
    for i in range(0, plan, 1):
        time.sleep(5)  # 隔5毫秒请求一次

        start = 21 * i
        url = "https://dongxi.douban.com/j/search?start=" + str(start) + "&kind=3090&sort=1&q=%E9%93%B6%E9%A5%B0"
        response = requests.get(url)

        obj = json.loads(response.text)
        htmlText = obj['html']

        html = etree.HTML(htmlText)
        targeElements = html.xpath("//*[@id='J_CardListBox']/ul/li")

        if len(targeElements) == 0:
            exit(0)

        print len(targeElements)

        loopCount = 0
        for targetElement in targeElements:
            if len(targetElement.xpath("div[@class='card-main']")) == 0:
                continue

            if len(targetElement.xpath("div[@class='card-main']/div[@class='card-bd']")) == 0:
                continue

            title = ""
            if len(targetElement.xpath("div[@class='card-main']/div[@class='card-bd']/h2[@class='story-title']")) != 0:
                title = targetElement.xpath("div[@class='card-main']/div[@class='card-bd']"
                                            "/h2[@class='story-title']/@title")[0]

            pid = ""
            if len(targetElement.xpath("div[@class='card-main']/div[@class='card-bd']/div[@class='story-info']")) == 0:
                continue
            else:
                pid = targetElement.xpath("div[@class='card-main']/div[@class='card-bd']"
                                          "/div[@class='story-info']/@data-eqid")[0]

            if len(targetElement.xpath("div[@class='card-main']/div[@class='card-bd']/div[@class='story-info']"
                                       "/ul[@class='stats-list']")) == 0:
                continue

            douListCountStr = ""
            if len(targetElement.xpath("div[@class='card-main']/div[@class='card-bd']/div[@class='story-info']"
                                       "/ul[@class='stats-list']/li[@class='doulist-count']")) != 0:
                douListCountStr = targetElement.xpath("div[@class='card-main']/div[@class='card-bd']"
                                                      "/div[@class='story-info']"
                                                      "/ul[@class='stats-list']/li[@class='doulist-count']")[0].text

            likeStr = ""
            if len(targetElement.xpath("div[@class='card-main']/div[@class='card-bd']/div[@class='story-info']"
                                       "/ul[@class='stats-list']/li[@class='like']")) != 0:
                likeStr = targetElement.xpath("div[@class='card-main']/div[@class='card-bd']/div[@class='story-info']"
                                              "/ul[@class='stats-list']/li[@class='like']")[0].text

            postStr = ""
            if len(targetElement.xpath("div[@class='card-main']/div[@class='card-bd']/div[@class='story-info']"
                                       "/ul[@class='stats-list']/li[@class='post']")) != 0:
                postStr = targetElement.xpath("div[@class='card-main']/div[@class='card-bd']/div[@class='story-info']"
                                              "/ul[@class='stats-list']/li[@class='post']")[0].text

            '''
            print title
            print pid
            print likeStr
            print postStr
            print douListCountStr
            print "\n"
            '''

            douListCount = douListCountStr[5:]
            likeNum = likeStr[3:]
            postNum = postStr[3:]

            tomongo(title, pid, douListCount, likeNum, postNum)

            loopCount += 1
            totalCount += 1

            '''
            _id = idStr.replace("'", "")
            _id = idStr.replace("[", "")
            _id = idStr.replace("]", "")

            douList = douListStr[5:]
            like = likeStr[3:]
            comment = commentStr[3:]
            print _id
            print douList
            print like
            print comment
            print "\n"
            '''

        print "本次循环取得了:" + str(loopCount) + "条记录"
        print "\n"
        print "=========="

    print "一共取得了:" + str(totalCount) + "条记录"
    client.close()
