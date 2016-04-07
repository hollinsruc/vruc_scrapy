# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class GradeItem(scrapy.Item):
	# 课程名称
	name = scrapy.Field()
	# 课程类别
	ctype = scrapy.Field()
	# 教师
	teacher = scrapy.Field()
	# 学分
	credit = scrapy.Field()
	# 绩点
	point = scrapy.Field()
 
