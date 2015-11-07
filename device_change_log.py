#!/usr/bin/env python
#coding: utf-8

'''
Author: Hover Winter(hoverwinter@gmail.com)
Function: parse device_change_log, update & insert records
Exported:
	go(filename): main function to finish all things
	devs: a list of all change records from excel files
'''
import xlrd
from models import DeviceChange
import MySQLdb
from constants import *
import os

devs = []

# 解析Excel文件
def _resolve(filename):
	data = xlrd.open_workbook(filename)

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

		devs.append(DeviceChange(*table.row_values(i)))

	for i in devs:
		i.dev_print()

# 保存资产变更记录
def _store(conn):
	cur = conn.cursor()
	for item in devs:
		cur.execute(item.sql())
	conn.commit()
	cur.close()

# 更新设备信息	
def _update(conn):
	cur = conn.cursor()
	for item in devs:
		count = cur.execute('select * from device_info where number = "%s"' % item.number)
		if count != 1:
			print "设备编号: %s 不存在该设备的纪录" % item.number
		else:
			sql = 'update device_info set location = "%s", user = "%s"' % (item.new_location, item.new_user)
			cur.execute(sql)
	conn.commit()
	cur.close()

# 主函数
def go(filename):
	if not os.path.exists(filename):
		print "文件不存在"
		exit(-1)

	# 如果不指定 charset 为 utf8 ，则插入中文时 mysql-python 报错
	conn= MySQLdb.connect(host=HOST, port = PORT, user=USER, passwd=PASSWD, db=DB, charset="utf8")
	
	_resolve(filename)
	_store(conn)
	_update(conn)

	conn.close()

if __name__ == '__main__':
	filename = u'固定资产/2015年3月31日固定资产转移登记表.xlsx'
	go(filename)
