# -*- coding: utf-8 -*-
import scrapy
from tjnuNews.items import TjnunewsItem


class TinunewsspiderSpider(scrapy.Spider):
    name = 'tinuNewsSpider'
    allowed_domains = ['https://weibo.com/']#规定抓取范围，防止小爬虫失控
    
    url="https://weibo.com/p/1005055308619220/follow?relate=fans&page="#需要构造的连接
    offset=1
    start_urls = ["https://weibo.com/p/1005055308619220/follow?relate=fans&page=1"]#开始抓取的页面

    def parse(self, response):
        for each in response.xpath("li[@class='follow_item S_line2']"):
        	item = TjnunewsItem()
        	try:
        		item["NickName"]=each.xpath("//div[@class='info_name W_fb W_f14']").extract()[0]
        		yield item
        	except IndexError:
        		pass

        if self.offset<5:
        	self.offset+=1
        yield scrapy.Request(self.url+str(self.offset),callback=self.parse,dont_filter=True)
