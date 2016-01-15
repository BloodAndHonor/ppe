#coding: utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from mysite.parser import device_change_log,device_info, my_models
from mysite.models import *
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import xlwt
import re
from django.utils.timezone import now, timedelta
import datetime
import hashlib
############
#
# 登陆相关
#
############
# 初始化
def init(request):
	if User.objects.all().count() == 0:
		User.objects.create(name="lyp", password=hashlib.md5("123456").hexdigest())
		# 清空信息
		Config.objects.all().delete()
		Device.objects.all().delete()
		Change.objects.all().delete()
		# 初始化
		Config.objects.create(name='wh_man', value='万利军')
		Config.objects.create(name='location', value='仓库')
		Config.objects.create(name='exp_y', value='6')
		return HttpResponse("初始化成功，用户名 lyp，密码 123456")
	else:
		return HttpResponse("已使用，不符合初始化条件")

# 登录
def login(request):
	if request.method == 'GET':
		return render(request, 'login.html')
	else:
		name = request.POST['username']
		password = request.POST['password']
		check = request.POST.get('check_aban',False)
		count = User.objects.filter(name=name, password=hashlib.md5(password).hexdigest()).count()
		if(count > 0):
			request.session['token'] = 'allowed'
			# 是否需要自动待报废
			if check:
				auto_aban()
			return HttpResponseRedirect('/')
		else:
			return HttpResponse("登陆失败")

# 检查登录状态
def check_login(request):
	if request.session.get('token','forbidden') == 'allowed':
		return True
	return False

# 登出
def logout(request):
	if request.session['token'] == 'allowed':
		del request.session['token']
	return HttpResponseRedirect('/login')

# 修改密码
def chg_pass(request):
	if(not check_login(request)):
		return HttpResponseRedirect('/login')
	if request.method == "GET":
		return render(request, 'password.html', None)
	else:
		newpwd = request.POST['newpwd']
		username = request.POST['username']

		pwd = hashlib.md5(newpwd).hexdigest()
		tmp = User.objects.get(name=username)
		if tmp == None:
			return HttpResponse("用户名不存在")
		else:
			tmp.password = pwd
			tmp.save()
		return  render(request, 'password.html', {'suc':True})
############
#
# 解析excel相关
#
############
#首页
def index(request):
	if(not check_login(request)):
		return HttpResponseRedirect('/login')
	return render(request,'index.html')

# 更新设备信息 success是否执行成功 log 记录 uploaded 上传过文件处理
def upload_device(request):
	if(not check_login(request)):
		return HttpResponseRedirect('/login')
	if request.method == 'POST':
		success,log = device_info.go_f(request.FILES['file'].read())
		# 处理初始化仓库管理员和位置 只要它们值都不是 待定 ，那么这么做就是有效的
		wh_man = Config.objects.get(name="wh_man").value
		location = Config.objects.get(name="location").value
		devs = Device.objects.all().filter(location='待定')
		for dev in devs:
			dev.location = location
			dev.user = wh_man
			dev.save()
		return render(request, 'upload_device.html', {'uploaded':True, 'log':log, 'success':success})
	else:
		return render(request, 'upload_device.html')

# 更新 变更信息
def upload_change(request):
	if(not check_login(request)):
		return HttpResponseRedirect('/login')
	if request.method == 'POST':
		fcont = request.FILES['file'].read()
		# md5
		fmd5 = hashlib.md5(fcont).hexdigest()
		fh = FileHash.objects.filter(value=fmd5)
		# 检查是否已上传
		if fh.count() != 0:
			success, log = False, '[%s] 上传过相同的文件，请核对!' % str(fh[0].in_date)
		else:
			FileHash.objects.create(in_date=now(),value=fmd5)
			success,log = device_change_log.go_f(fcont)
		return render(request, 'upload_change.html', {'uploaded':True, 'log':log, 'success':success})
	else:
		return render(request, 'upload_change.html')

############
#
# 配置相关
#	
#############
def chg_config(request):
	changed = False
	if request.method == 'POST':
		exp_y = request.POST['exp_y']
		# 判断是否为数字
		try:
			int(exp_y)
		except:
			exp_y = '6'
		wh_man = request.POST['wh_man']
		location = request.POST['location']
		tmp = Config.objects.get(name="exp_y")
		tmp.value = exp_y
		tmp.save()
		tmp = Config.objects.get(name="wh_man")
		tmp.value = wh_man
		tmp.save()
		tmp = Config.objects.get(name="location")
		tmp.value = location
		tmp.save()
		changed = True
	else: 
		exp_y = Config.objects.get(name="exp_y").value
		wh_man = Config.objects.get(name="wh_man").value
		location = Config.objects.get(name="location").value
	return render(request, 'config.html', {'exp_y':exp_y, 'wh_man':wh_man, 'location':location, 'changed':changed})

############
#
# 查询相关
#	所有的查询以AJAX＋JSON方式	
#############
#查询设备
@csrf_exempt
def dev_s(request):
	if(not check_login(request)):
		return HttpResponseRedirect('/login')
	if request.method == 'POST':
		number = request.POST['number']
		name = request.POST['name']
		status = request.POST['status']
		user = request.POST['user']
		location = request.POST['location']
		model = request.POST['model']
		# model = ""

		kwargs = {}
		# 解析出来的excel设备编号后面都多了这个，这里做个适配
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

		if model != "":
			kwargs['model'] = model + '\x7f'

		data = serializers.serialize('json', Device.objects.filter(**kwargs))
		return HttpResponse(json.dumps(data), content_type="application/json")
	else:
		return HttpResponseRedirect('/')

@csrf_exempt
def chg(request):
	if(not check_login(request)):
		return HttpResponseRedirect('/login')
	number = request.GET['number']
	return render(request, 'change.html', {"number": number})

@csrf_exempt
def chg_s(request):
	if(not check_login(request)):
		return HttpResponseRedirect('/login')
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
	if(not check_login(request)):
		return HttpResponseRedirect('/login')
	if request.method == 'POST':
		number = request.POST['number']
		name = request.POST['name']
		status = request.POST['status']
		user = request.POST['user']
		location = request.POST['location']

		kwargs = {}
		# 解析出来的excel设备编号后面都多了这个，这里做个适配
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

		if model != "":
			kwargs['model'] = model + '\x7f'

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

##############
#
# 自动待报废： 年限过期的设备自动待报废
#
##############
def auto_aban():
	expire_year = int(Config.objects.get(name="exp_y").value)
	lower_year = now().date().year - expire_year
	month = now().date().month
	day = now().date().day
	try:
		t = datetime.datetime(lower_year, month, day)
	except:
		t = datetime.datetime(lower_year, month, day-1)

	res = Device.objects.filter(in_date__lte=t)
	# print u'报废处理:'
	for item in res:
		# print item.number
		item.status = u'待报废'
		item.save()
	return len(res)

## 手动报废
def aban(request):
	if(not check_login(request)):
		return HttpResponseRedirect('/login')
	num = request.GET['number']
	ddev = Device.objects.filter(number=num)
	if ddev.count() == 1:
		dev = ddev.get()
		if dev.status == u'待报废':
			dev.status = u'报废'
			dev.save()
	return render(request, 'info.html', {"msg": u"仪器编号 "+ num.strip() + u" 的设备报废成功！"})

############
#
# 出厂编号相关
#	
############
@csrf_exempt
def fact_number(request):
	if(not check_login(request)):
		return HttpResponseRedirect('/login')
	if request.method == 'POST':
		number = request.POST['number']
		factory_number = request.POST['fact_num']

		print number, len(number), factory_number
		ddev = Device.objects.filter(number=number)
		dev = ddev.get()
		dev.factory_number = factory_number
		dev.save()
		return HttpResponse("修改成功")
