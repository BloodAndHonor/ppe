#!/usr/bin/env python
#coding: utf-8

import xlrd
from mysite.parser.constants import *

class DeviceChange:
	# 放弃 serial 即 设备序列号
	def __init__(self, log_date, name, number, count, unit, serial, old_location, new_location, old_user, new_user):
		self.log_date = xlrd.xldate.xldate_as_datetime(log_date, 0)
		self.name = name
		if isinstance(number, float):
			self.number = int(number)
		else:
			self.number = number.strip()
		self.count = int(count)
		self.unit = unit
		self.old_location = old_location
		self.new_location = new_location
		self.old_user = old_user
		self.new_user = new_user

	def dev_print(self):
		print self.log_date, self.name, self.number, self.count, self.unit, self.old_location, self.new_location, self.old_user, self.new_user

	def sql(self):
		return 'insert into mysite_change values(NULL, "%s","%s","%s",%s,"%s","%s","%s","%s","%s")' % (self.log_date, self.name, self.number,self.count, self.unit, self.old_location, self.new_location, self.old_user, self.new_user)

class DeviceInfo:
	# 忽略 使用单位 合同号 免税证号 信息采集号
	def __init__(self, department, number, name, category_number, model, specification, price, vender, buy_date, status, funds_category, use_direction, device_source, use_person, handby_person, record_person, input_person, in_date, document_number, location, remarks, funds_card, contact_number, no_tax_number, info_gather_number):
		self.number = number
		self.name = name
		self.category_number = category_number
		self.model = model
		self.specification = specification
		self.price = price
		self.vender = vender	# 生产厂商
		self.buy_date = xlrd.xldate.xldate_as_datetime(buy_date, 0)
		self.status = status
		self.funds_category = funds_category
		self.use_direction = use_direction	#使用方向
		self.device_source = device_source
		self.use_person = use_person
		self.handby_person = handby_person
		self.record_person = record_person
		self.input_person = input_person
		self.in_date = xlrd.xldate.xldate_as_datetime(in_date, 0)
		self.document_number = document_number	#  单据号
		self.location = INIT_LOCATION
		self.remarks = remarks
		self.funds_card = funds_card
		self.user = INIT_USER

	def dev_print(self):
		print self.number,self.name,self.category_number,self.model,self.specification,self.price,self.vender,self.buy_date,self.status,self.funds_category,self.use_direction, self.device_source

	def sql(self):
		# insert IGNORE 主键重复则忽略改记录
		return 'insert ignore into mysite_device values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","")' % (
			self.number,
			self.name,
			self.category_number,
			self.model ,
			self.specification,
			self.price,
			self.vender,
			self.buy_date,
			self.status,
			self.funds_category ,
			self.use_direction,
			self.device_source ,
			self.use_person ,
			self.handby_person ,
			self.record_person ,
			self.input_person ,
			self.in_date ,
			self.document_number ,
			self.location,
			self.remarks,
			self.funds_card,
			self.user
		)
