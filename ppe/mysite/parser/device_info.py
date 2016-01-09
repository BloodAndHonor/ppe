#!/usr/bin/env python
#coding: utf-8

'''
Author: Hover Winter(hoverwinter@gmail.com)
Function: parse device_info, insert records
Exported:
	go(filename): main function to finish all things
	devs: a list of all device records from excel files
'''
import xlrd
from mysite.parser.my_models import DeviceInfo
import MySQLdb
from mysite.parser.constants import *
import os

devs = []

# 解析Excel文件
def _resolve(data):
	table = data.sheets()[0]

	for i in range(3, table.nrows):
		if DEBUG:
			print "解析Excel的结果："
			for j in table.row_values(i):
				if isinstance(j, unicode):
					print j.encode('utf-8'),
				else:
					print j,
			print

		devs.append(DeviceInfo(*table.row_values(i)))

	if DEBUG:
		for i in devs:
			i.dev_print()

# 保存设备基本信息
def _store(conn):
	cur = conn.cursor()
	for item in devs:
		cur.execute(item.sql())
	conn.commit()
	cur.close()

# 主函数
def go(filename):
	if not os.path.exists(filename):
		print "文件不存在"
		exit(-1)

	# 如果不指定 charset 为 utf8 ，则插入中文时 mysql-python 报错
	conn= MySQLdb.connect(host=HOST, port=PORT, user=USER, passwd=PASSWD, db=DB, charset="utf8")
	
	_resolve(filename)
	_store(conn)

	conn.close()

def go_f(filecontent):
	try:
		conn= MySQLdb.connect(host=HOST, port = PORT, user=USER, passwd=PASSWD, db=DB, charset="utf8")
	except Exception,e:
		return False,"建立数据库连接失败"

	try:
		data = xlrd.open_workbook(file_contents=filecontent)
	except:
		return False,"打开Excel文件失败"

	try:
		_resolve(data)
	except:
		return False,"解析文件出错，请检查格式"

	try:
		_store(conn)
	except Exception,e:
		print e
		return False,"数据库操作失败"

	conn.close()
	return True,"解析文件，并更新信息成功"

if __name__ == '__main__':
	filename = u'固定资产/设备信息.xlsx'
	go(filename)
