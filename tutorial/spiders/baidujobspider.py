import scrapy


class BaiduJobsSpider(scrapy.Spider):
    name = "baiduspider"
    urls = [
        'https://dongxi.douban.com/search?q=%E9%93%B6%E9%A5%B0'
    ]

    def start_requests(self):

        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print "=================="
        print response.url.split("&")
        print response.body
        print "=================="
        self.log("saved file succ")

        '''
        /html/body/div[@id='wrapper']
        /div[@id='content']
        /div[@class='grid-16-8 clearfix']
        /div[@class='article']
        /div[@id='J_CardListBox']
        /ul[@class='cardList largecard']
        /*[@id="J_CardListBox"]/ul/li[1]
        '''

        # dou = ["//*[@id='J_CardListBox']/ul/li[1]/div[1]/div[2]/div[3]/ul/li[1]",
        # "//*[@id='J_CardListBox']/ul/li[1]/div[1]/div[2]/div[3]/ul/li[2]",
        # "//*[@id='J_CardListBox']/ul/li[1]/div[1]/div[2]/div[3]/ul/li[3]"]

