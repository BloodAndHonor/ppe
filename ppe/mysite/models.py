#coding: utf-8
from django.db import models
import json

# 用户
class User(models.Model):
	name = models.CharField(max_length=20)
	password = models.CharField(max_length=40)

# 设备
class Device(models.Model):
	number = models.CharField(max_length=15, primary_key=True)
	name = models.CharField(max_length=20)
	category_number = models.CharField(max_length=10)
	model = models.CharField(max_length=50)
	specification = models.CharField(max_length=50)
	price = models.CharField(max_length=10)
	vender = models.CharField(max_length=50)
	buy_date = models.DateTimeField()
	status = models.CharField(max_length=15)
	funds_category = models.CharField(max_length=15)
	use_direction = models.CharField(max_length=15)
	device_source = models.CharField(max_length=15)
	use_person = models.CharField(max_length=10)
	handby_person = models.CharField(max_length=10)
	record_person = models.CharField(max_length=10)
	input_person = models.CharField(max_length=10)
	in_date = models.DateTimeField()
	document_number = models.CharField(max_length=20)
	location = models.CharField(max_length=20)
	remarks = models.CharField(max_length=50)
	funds_card = models.CharField(max_length=50)
	user = models.CharField(max_length=50)

# 变更
class Change(models.Model):
	log_date = models.DateTimeField()
	name = models.CharField(max_length=20)
	number = models.CharField(max_length=20)
	count = models.IntegerField()
	unit = models.CharField(max_length=5)
	old_location = models.CharField(max_length=20)
	new_location = models.CharField(max_length=20)
	old_user = models.CharField(max_length=10)
	new_user = models.CharField(max_length=10)

# MD5
class FileHash(models.Model):
	in_date = models.DateTimeField()
	value = models.CharField(max_length=35)
	ftype = models.IntegerField(default=0) #0 变更 其它备用

# 配置
class Config(models.Model):
	name = models.CharField(max_length=10, primary_key=True)
	value = models.CharField(max_length=10)