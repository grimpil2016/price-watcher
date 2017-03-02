#! /usr/bin/python
# -*- coding:utf-8 -*-

import urllib
from urllib import request
import json
import time
from time import sleep
import os
import urllib.parse
from bs4 import BeautifulSoup
import random
import config.py

class PriceWatcher(object):

	def __init__(self):
		pass

	def watcher(self, products):
		fileHandle = open(products, 'r', encoding='gbk')
		lines = fileHandle.readlines()
		fileHandle.close()
		for line in lines:
			product_id = line.split(' ')[0]
			product_name = line.split(' ')[1][:-1]

			current_price = get_current_price(product_id)
			if current_price is None:
				continue
			
			current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
			new_line = current_price + ' ' + current_time + '\n'
			
			former_price = get_former_price(product_id)
			if former_price is None:
				add_new_line(product_id, new_line)
			elif current_price != former_price:
				add_new_line(product_id, new_line)
				send_notify(product_id, product_name, former_price, current_price)
			sleep_time = random.randint(1,5)
			sleep(sleep_time)

def get_current_price(product_id):
	url = 'http://p.3.cn/prices/mgets?skuIds=J_' + product_id
	
	#response = urlopen(url)
	req = urllib.request.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36')
	response = urllib.request.urlopen(req)
	content = response.read().decode('utf-8')
	result = json.loads(content)
	print(result)

	if type(result) is list:
		current_price = result[0]['p']
		return current_price
	elif type(result) is dict:
		print('Get price if {0}(procuct_id) from API failed. Try to get price from mobile page.'.format(product_id))

		url = 'https://item.m.jd.com/product/' + product_id + '.html'
		response = request.urlopen(url)
		content = response.read().decode('utf-8')
		soup = BeautifulSoup(content, 'html.parser')
		price_node = soup.find('span', id='jdPrice-copy')
		if price_node is not None:
			current_price = price_node.get_text()[1:-1]
			return current_price
		else:
			print('Get price if {0}(procuct_id) from mobile page failed.'.format(product_id))
			return None
	else:
		return None


def get_former_price(product_id):
	file_name = './price/' + product_id + '.txt'
	if os.path.isfile(file_name):
		fh = open(file_name, 'r')
		lines = fh.readlines()
		former_price = lines[-1].split(' ')[0]
		fh.close()
		return former_price
	else:
		fh = open(file_name, 'w')
		fh.close()
		return None

def add_new_line(product_id, new_line):
	file_name = './price/' + product_id + '.txt'
	fh = open(file_name, 'a')	
	fh.write(new_line)
	fh.close()

def send_notify(product_id, product_name, former_price, current_price):
	serverchan_sckey = config.serverchan_sckey
	serverchan_api = 'http://sc.ftqq.com/' + serverchan_sckey +'.send?'
	product_url = 'https://item.jd.com/' + product_id + '.html'
	text = '价格变动通知'
	desp = '京东网\"' + product_name + '\"的价格由' + former_price + '元调整为' + current_price + '元，如需了解详情可打开此链接查看：' + product_url
	request.urlopen(serverchan_api + 'text=' + urllib.parse.quote(text) + '&desp=' + urllib.parse.quote(desp))

if __name__ == '__main__':
	products = 'products.txt'
	price_watcher = PriceWatcher()

	while True:
		print('Price checking start...')
		try:
			price_watcher.watcher(products)
			print(time.ctime())
			print('All price checked!\nWait one hour to do again...\n')
		except:
			print(time.ctime())
			print('Unkonwn error...\n')
		
		sleep(5400)