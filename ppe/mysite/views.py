#coding: utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from mysite.parser import device_change_log,device_info
from mysite.models import *
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import xlwt
import re

############
#
# 登陆相关
#
############
# 初始化
def init(request):
	User.objects.create(name="lyp", password="123456")
	return HttpResponse("初始化成功")

# 登录
def login(request):
	if request.method == 'GET':
		return render(request, 'login.html')
	else:
		name = request.POST['username']
		password = request.POST['password']
		count = User.objects.filter(name=name, password=password).count()
		if(count > 0):
			request.session['token'] = 'allowed'
			return HttpResponseRedirect('/')
		else:
			return HttpResponse("登陆失败")

# 检查登录状态
def check_login(request):
	if request.session.get('token','forbidden') == 'allowed':
		return True
	return HttpResponseRedirect("/login")

# 登出
def logout(request):
	if request.session['token'] == 'allowed':
		del request.session['token']
	return HttpResponseRedirect('/login')

############
#
# 解析excel相关
#
############
#首页
def index(request):
	check_login(request)
	return render(request,'index.html')

# 更新设备信息 success是否执行成功 log 记录 uploaded 上传过文件处理
def upload_device(request):
	check_login(request)
	if request.method == 'POST':
		success,log = device_info.go_f(request.FILES['file'].read())
		return render(request, 'upload_device.html', {'uploaded':True, 'log':log, 'success':success})
	else:
		return render(request, 'upload_device.html')

# 更新 变更信息
def upload_change(request):
	check_login(request)
	if request.method == 'POST':
		success,log = device_change_log.go_f(request.FILES['file'].read())
		return render(request, 'upload_change.html', {'uploaded':True, 'log':log, 'success':success})
	else:
		return render(request, 'upload_change.html')

############
#
# 查询相关
#	所有的查询以AJAX＋JSON方式	
#############
#查询设备
@csrf_exempt
def dev_s(request):
	check_login(request)
	if request.method == 'POST':
		number = request.POST['number']
		name = request.POST['name']
		status = request.POST['status']
		user = request.POST['user']
		location = request.POST['location']

		kwargs = {}
		# 解析出来的excel设备编号后面都多了这个，这里做个适配
		# 原因待查
		if number != "":
			kwargs['number'] = number + '\x7f'

		if name != "":
			kwargs['name'] = name

		if status != "":
			kwargs['status'] = status

		if user != "":
			kwargs['user'] = user

		if location != "":
			kwargs['location'] = location

		data = serializers.serialize('json', Device.objects.filter(**kwargs))
		return HttpResponse(json.dumps(data), content_type="application/json")
	else:
		return HttpResponseRedirect('/')

@csrf_exempt
def chg(request):
	check_login(request)
	number = request.GET['number']
	return render(request, 'change.html', {"number": number})

@csrf_exempt
def chg_s(request):
	check_login(request)
	number = request.POST['number'].strip()
	# 去掉查询中的 \x7f 也算是一个适配
	if number.find('\x7f'):
		number = number[:-1]

	data = serializers.serialize('json', Change.objects.filter(number=number))
	return HttpResponse(json.dumps(data), content_type="application/json")

##########
#
# 导出相关
#
##########
def export_dev(request):
	check_login(request)
	if request.method == 'POST':
		number = request.POST['number']
		name = request.POST['name']
		status = request.POST['status']
		user = request.POST['user']
		location = request.POST['location']

		kwargs = {}
		# 解析出来的excel设备编号后面都多了这个，这里做个适配
		# 原因待查
		if number != "":
			kwargs['number'] = number + '\x7f'

		if name != "":
			kwargs['name'] = name

		if status != "":
			kwargs['status'] = status

		if user != "":
			kwargs['user'] = user

		if location != "":
			kwargs['location'] = location

		data = Device.objects.filter(**kwargs)

		# 数据写入excel
		w = xlwt.Workbook(encoding='utf-8')
		ws = w.add_sheet('sheet-1')
		ws.write(0,0,u'设备编号')
		ws.write(0,1,u'设备名称')
		ws.write(0,2,u'分类号')
		ws.write(0,3,u'型号')
		ws.write(0,4,u'规格')
		ws.write(0,5,u'单价')
		ws.write(0,6,u'厂家')
		ws.write(0,7,u'购置日期')
		ws.write(0,8,u'现状')
		ws.write(0,9,u'经费科目')
		ws.write(0,10,u'使用方向')
		ws.write(0,11,u'使用人')
		ws.write(0,12,u'使用地点')
		ws.write(0,13,u'备注')

		row = 1
		for item in data:
			ws.write(row,0, item.number)
			ws.write(row,1, item.name)
			ws.write(row,2, item.category_number)
			ws.write(row,3, item.model)
			ws.write(row,4, item.specification)
			ws.write(row,5, item.price)
			ws.write(row,6, item.vender)
			ws.write(row,7, str(item.buy_date))
			ws.write(row,8, item.status)
			ws.write(row,9, item.funds_category)
			ws.write(row,10, item.use_direction)
			ws.write(row,11, item.user)
			ws.write(row,12, item.location)
			ws.write(row,13, item.remarks)
			row = row + 1

		response = HttpResponse(content_type="application/vnd.ms-excel") #解决ie不能下载的问题
		response['Content-Disposition'] ='attachment; filename=export.xls' #解决文件名乱码/不显示的问题
		w.save(response)
		return response
		# 导出
	else:
		return HttpResponseRedirect('/')