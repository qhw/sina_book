#!/usr/bin/python
#coding=utf8
import urllib, urllib2
from BeautifulSoup import *
import chardet

def utf8(res):
	res = res.encode("utf8")
	return res

def code(res):
	gb = ("gb2312", "GB2312", "gb18030", "GB18030", "GBK", "gbk")
	utf = ("utf8", "UTF8", "utf-8", "UTF-8")

	encode = chardet.detect(res)["encoding"]
	print encode
	if res:
		try:
			if encode in gb:
				res = res.encode("utf8")
				return res
			elif encode in utf:
				return res
			elif encode not in gb and encode not in utf:
				try:
					res = res.decode(encode).encode("utf8")
					return res
				except:
					print "未知编码"
		except:
			print "转换编码错误"

def search():
	url = "http://vip.book.sina.com.cn/s.php?k=%D0%ED%D6%AA%D4%B6&s_type=2&s_pub=1&dpc=1"

	urlbase = "http://vip.book.sina.com.cn/s.php?"

	key = u"许知远"
	s_type = 2
	s_pub = 1
	dpc = 1

	#while True:
	#	key = raw_input("输入搜索作者名的关键字:")
	#	if key == "":
	#		print "你输入为空，请重新输入:"
	#		continue
	#	else:
	#		break
	
	key = key.encode('gb2312')
	data = {"k":key, "s_type":s_type, "s_pub":s_pub, "dpc":dpc}
	data = urllib.urlencode(data)
	url = urlbase + data
	req = urllib2.Request(url)
	req.add_header('Referer', 'http://vip.book.sina.com.cn/')
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:8.0.1) Gecko/20110101 Firefox/8.0.1')

	res = urllib2.urlopen(req).read()

	base_url = "http://vip.books/sina.com.cn"
	soup = BeautifulSoup(unicode(res, 'GBK'))
	div = soup.findAll('div', {"class":"content"})[0]
	li = div.findAll('li')
	for li1 in li:
		book_info = li1.findAll('a', {"class":"f14blackB"})[0]
		title = book_info.contents  #书名
		url = book_info["href"] #书的链接
		#书的图片
		img_url = li1.findAll('img', {"width":80,"height":112})[0]["src"]

		b_info = li1.findAll('div', {"class":"blkInfo"})[0]
		b_info_p = b_info.findAll('p')
		b_info_p_a = b_info_p[0].findAll('a')
		print "书名:", utf8(title[0])
		print "作者:", utf8(b_info_p_a[0].contents[0])
		print "书的链接", base_url + url
		print "书的图片",img_url
		print "出版社:", utf8(b_info_p[3].findAll('a')[0].contents[0])
		print "简介:", utf8(b_info_p[1].contents[0])
		
def book():
	url = "http://vip.book.sina.com.cn/book/index_181118.html"

	base_url = "http://vip.book.sina.com.cn/book/"

	req = urllib2.Request(url)
	req.add_header('Referer','http://vip.book.sina.com.cn/')
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:8.0.1) Gecko/20110101 Firefox/8.0.1')
	res = urllib2.urlopen(req).read()

	soup = BeautifulSoup(unicode(res,'GBK'))
	
	parts = soup.findAll('div', {"class":"blk_03"})
	for part in parts:
		part_introduction = part.findAll('p')[1].contents[0]
		part_title = part.find("h3").contents[0]
		part_zhangjie = part.findAll('a')
		for _part in part_zhangjie:
			url =  base_url + _part["href"]
			print url
			neirong(url)
		print utf8(part_title)
		print utf8(part_introduction)
		#break

def neirong(url):
	req = urllib2.Request(url)
	res = urllib2.urlopen(req).read()
	soup = BeautifulSoup(unicode(res, 'GBK'))
	contents = soup.find('div', {"id":"contTxt"}).contents
	time = soup.findAll('em')[1].contents[0]
	print '更新时间', time
	for content in contents: 
		if len(content.contents):
			print content.contents[0]
search()
book()
