# -*- coding: utf-8 -*-
import scrapy
from tjnu.items import TjnuItem


class TjnunewsSpider(scrapy.Spider):
	name = 'tjnunews'
	allowed_domains = ['tjnu.edu.cn']
	offset = 1
	url ="http://www.tjnu.edu.cn/sdyw/"
	
	start_urls = [url+str(offset)+'.htm']

	#对单个页面进行处理
	def parse(self, response):

		for each in response.xpath("//li[@class='sdyw_li ']"):	
			item = TjnuItem()
			
			date = each.xpath("./span/text()").extract() #已经将日期抽取出来了
			text = each.xpath("./a/text()").extract() #获取了标题
			#item["data"] = data
			item["date"] = date
			item["text"] = text
			yield item
			
		if self.offset<75:
			self.offset +=1
		yield scrapy.Request(self.url+str(self.offset)+'.htm',callback = self.parse)