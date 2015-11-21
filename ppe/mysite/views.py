#coding: utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from mysite.parser import device_change_log,device_info
from mysite.models import *
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

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

		print kwargs
		data = serializers.serialize('json', Device.objects.filter(**kwargs))
		return HttpResponse(json.dumps(data), content_type="application/json")
	else:
		return HttpResponseRedirect('/')

