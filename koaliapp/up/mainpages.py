#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session

from up.models import *
import json
from django.template.loader import get_template
from django.template import Context
import re
import sys

reload(sys)

sys.setdefaultencoding('utf8')

#获取省份列表
def getProvinceList(request):
	response={}
	obj_list = list(ProvinceList.objects.all().values('id','name'))
	response['data'] = obj_list
	response['status'] = 0
	response['message'] = 'ok'

	return HttpResponse(json.dumps(response, ensure_ascii = False))

#获取城市列表
def getCityList(request):
	response={}
	if 'pid' in request.GET:
		obj_list = list(CityList.objects.filter(province_id=request.GET['pid']).values('id','name'))
		response['data'] = obj_list
		response['status'] = 0
		response['message'] = 'ok'
	else:
		response['data'] = None
		response['status'] = 404
		response['message'] = 'miss some parameter'

	return HttpResponse(json.dumps(response, ensure_ascii = False))	

#获取学校列表
def getSchoolList(request):
	response={}
	if 'pid' in request.GET:
		obj_list = list(SchoolList.objects.filter(province_id=request.GET['pid']).values('id','name'))
		response['data'] = obj_list
		response['status'] = 0
		response['message'] = 'ok'
	else:
		response['data'] = None
		response['status'] = 404
		response['message'] = 'miss some parameter'

	return HttpResponse(json.dumps(response, ensure_ascii = False))	

#获取专业分类列表
def getMajorClassfied(request):
	response={}
	obj_list = list(majorClassfied.objects.all().values('id','name').order_by('id'))
	response['data'] = obj_list
        response['status'] = 0
        response['message'] = 'ok'

        return HttpResponse(json.dumps(response, ensure_ascii = False))

#获取专业列表
def getMajorList(request):
	response={}
	if 'cid' in request.GET['cid']:
		cid = int(request.GET['cid'])
		obj_list = list(majorList.objects.filter(classfied_id=cid).values('id','name'))
		response['data'] = obj_list
        	response['status'] = 0
        	response['message'] = 'ok'
        
        return HttpResponse(json.dumps(response, ensure_ascii = False))

#返回用户基本信息
def getBaseInfo(request):
        response={}
        if 'uid' in request.GET:
		user_img = BasedInfo.objects.get(id=request.GET['uid']).headImg.url
                user_detail = DetailInfo.objects.get(account_id=request.GET['uid'])
                            
                obj = {}
                obj['id'] = user_detail.account_id
                obj['name'] = user_detail.name
		obj['headImg'] = 'http://120.25.12.205%s' %(user_img)
		obj['gender'] = user_detail.sex
                obj['province'] = user_detail.province
                obj['city'] = user_detail.city
                obj['nationality'] = user_detail.nationality
                obj['school'] = user_detail.school
		obj['major'] = user_detail.major
                obj['company'] = user_detail.workingCompany
		obj['position'] = user_detail.position
                obj['year'] = user_detail.year


                response['data'] = obj
                response['status'] = 0
                response['message'] = 'ok'
        else:
                response['data'] = None
                response['staus'] = 404
                response['message'] = 'miss some parameter'

        return HttpResponse(json.dumps(response, ensure_ascii = False))

#获取用户联系方式
def getConnectInfo(request):
	response={}
	if 'uid' in request.GET:
		connect = ConnectInfo.objects.get(account_id=request.GET['uid'])
		obj={}
		obj['phone'] = connect.phone
		obj['mail'] = connect.mail
		obj['QQ'] = connect.QQ
		response['data'] = obj
		response['message'] = 'ok'
		response['status'] = 0
	else:
                response['data'] = None
                response['staus'] = 404
                response['message'] = 'miss some parameter'

        return HttpResponse(json.dumps(response, ensure_ascii = False))

@csrf_exempt
#修改用户联系方式
def changeConnectInfo(request):
	response={}
	if 'uid' in request.POST:
		connect = ConnectInfo.objects.get(account_id=request.POST['uid'])
		if 'QQ' in request.POST:
			connect.QQ = request.POST['QQ']
		if 'phone' in request.POST:
			connect.phone = request.POST['phone']
		if 'mail' in request.POST:
			connect.mail = request.POST['mail']
		connect.save()
		
		response['message'] = 'ok'
                response['status'] = 0
        else:
                response['staus'] = 404
                response['message'] = 'miss some parameter'

        return HttpResponse(json.dumps(response, ensure_ascii = False))

@csrf_exempt
#修改用户基本信息
def changeBaseInfo(request):
	response={}
	if 'uid' in request.POST:
		user = DetailInfo.objects.get(account_id=request.POST['uid'])
		
		if 'name' in request.POST:
			user.name = request.POST['name']
		if 'gender' in request.POST:
			user.sex = request.POST['gender']
		if 'province' in request.POST:
			user.province = request.POST['province']
		if 'city' in request.POST:
			user.city = request.POST['city']
		if 'school' in request.POST:
			user.school = request.POST['school']
		if 'major' in request.POST:
			user.major = request.POST['major']
		if 'company' in request.POST:
			user.workingCompany = request.POST['company']
		if 'position' in request.POST:
			user.position = request.POST['position']
		if 'year' in request.POST:
			user.year = request.POST['year']

		user.save()

		response['data'] = None
                response['status'] = 0
                response['message'] = 'ok'
        else:
                response['data'] = None
                response['staus'] = 404
                response['message'] = 'miss some parameter'

        return HttpResponse(json.dumps(response, ensure_ascii = False))
#返回用户信息页
def userView(request):
	response={}
	if 'uid' in request.GET and request.GET['form']=='创业者' or request.GET['form']=='poineer':
		user = DetailInfo.objects.get(account_id=request.GET['uid'])
		user_img = BasedInfo.objects.get(id=request.GET['uid']).headImg.url
		user_project = poineeringTag.objects.get(account_id=request.GET['uid'])
		user_visualbility = visualbility.objects.get(account_id=request.GET['uid'])
		
		obj = {}
		obj['id'] = user.id
		obj['name'] = user.name
		obj['headImg'] = 'http://120.25.12.205%s' %(user_img)
		obj['item'] = user_project.name
		obj['direction1'] = user_project.direction1
		obj['direction2'] = user_project.direction2
		obj['stage'] = user_project.stage
		visual_list = [user_visualbility.executiveSum,user_visualbility.product,user_visualbility.competition,user_visualbility.sales,user_visualbility.businessModel,
				user_visualbility.teamManagement,user_visualbility.implementationPlan,user_visualbility.finacing,user_visualbility.opportunitiesAndRisks]
		obj['visualbility'] = visual_list

		response['status'] = 0
		response['message'] = 'ok'
		response['data'] = obj

	elif 'uid' in request.GET and request.GET['form']=='投资者' or request.GET['form']=='investor':
		user = DetailInfo.objects.get(account_id=request.GET['uid'])
                user_img = BasedInfo.objects.get(id=request.GET['uid']).headImg.url
                user_project = investmentInfo.objects.get(account_id=request.GET['uid'])

		obj = {}
		obj['id'] = user.id
                obj['name'] = user.name
                obj['headImg'] = 'http://120.25.12.205%s' %(user_img)
                obj['company'] = user_project.company
                obj['stage'] = user_project.stage
                obj['summary'] = user_project.summary
		obj['phase'] = user_project.phase
		obj['assembly'] = user_project.assembly
		obj['address'] = user_project.mail
		obj['direction1'] = user_project.direction1
		obj['direction2'] = user_project.direction2

		response['status'] = 0
                response['message'] = 'ok'
                response['data'] = obj
		
	else:
		response['data'] = None
                response['staus'] = 404
                response['message'] = 'miss some parameter'

        return HttpResponse(json.dumps(response, ensure_ascii = False))
		
#创业圈主页
def poineeringCircle(request):
	response={}
	if 'p' in request.GET and 'number' in request.GET:
		p = int(request.GET['p']) * 6
		number = int(request.GET['number'])
		#如果有筛选条件
		if number>0:
			if 'condition' in request.GET:
				condition_list = request.GET.getlist('condition')
				obj_list = []
				#筛选出每个符合筛选条件的条目
				num = p/len(condition_list)
				for i in range(0,len(condition_list)):
					Industry = industry.objects.get(id = condition_list[i])
					obj_set = Industry.item.exclude(name='').exclude(name=None).order_by('last_modified')[num:num+6/len(condition_list)]
					for item in obj_set:
						if item not in obj_list:
							obj = {}
							obj['name'] = item.name
							obj['founder'] = item.account.name
							obj['id'] = item.account.id
							obj['headImg'] = 'http://120.25.12.205%s' %(item.account.headImg.url)
							obj['startDate'] = item.startDate.strftime('%Y-%m-%d')
							obj['province'] = DetailInfo.objects.get(account_id=item.account_id).province
							obj['city'] = DetailInfo.objects.get(account_id=item.account_id).city
							obj['summary'] = item.summary
							obj['stage'] = item.stage
							obj['fund'] = item.fund
							obj['direction1'] = item.direction1
							obj['direction2'] = item.direction2
							obj_list.append(obj)
				response['message'] = 'ok'
				response['data'] =  obj_list
				response['status'] = 0
				
				return HttpResponse(json.dumps(response, ensure_ascii = False))
			else:
				response['message'] = 'miss some parameter'
				response['data'] =  None
				response['status'] = 404

				return HttpResponse(json.dumps(response, ensure_ascii = False))
		else:
			obj_set = poineeringTag.objects.exclude(name='').exclude(name=None).order_by('last_modified')[p:p+6]
			obj_list = []
			for item in obj_set:
				obj = {}
				obj['name'] = item.name
                               	obj['founder'] = item.account.name
                               	obj['id'] = item.account.id
                               	obj['headImg'] = 'http://120.25.12.205%s' %(item.account.headImg.url)
                               	obj['startDate'] = item.startDate.strftime('%Y-%m-%d')
                               	obj['summary'] = item.summary
                               	obj['stage'] = item.stage
				obj['fund'] = item.fund
				obj['province'] = DetailInfo.objects.get(account_id=item.account_id).province
                                obj['city'] = DetailInfo.objects.get(account_id=item.account_id).city
                               	obj['direction1'] = item.direction1
                               	obj['direction2'] = item.direction2
				obj_list.append(obj)
			response['message'] = 'ok'
			response['data'] =  obj_list
			response['status'] = 0

			return HttpResponse(json.dumps(response, ensure_ascii = False))
	else:
		response['message'] = 'miss some parameter'
		response['data'] =  None
		response['status'] = 404
		
		return HttpResponse(json.dumps(response, ensure_ascii = False))

#投资圈主页
def investingCircle(request):
	response={}
	if 'p' in request.GET:
		p = int(request.GET['p'])*6
		obj_set = investmentInfo.objects.exclude(company='').exclude(company=None)[p:p+6]
		obj_list = []
		for item in obj_set:
			obj = {}
			obj['id'] = item.account.id
			obj['company'] = item.company
			obj['stage'] = item.stage
			obj['name'] = item.account.name
			obj['address'] = item.mail
			obj['headImg'] = "http://120.25.12.205%s"%(item.account.headImg.url)
			obj['summary'] = item.summary
			obj['province'] = DetailInfo.objects.get(account_id=item.account_id).province
			obj['city'] = DetailInfo.objects.get(account_id=item.account_id).city
			obj['direction1'] = item.direction1
			obj['direction2'] = item.direction2
			obj_list.append(obj)
		response['message'] = 'ok'
		response['status'] = 0
		response['data'] = obj_list
	else:
		response['message'] = 'miss some parameter'
                response['data'] =  None
                response['status'] = 404

        return HttpResponse(json.dumps(response, ensure_ascii = False))
		 
#获取行业选项
def industryList(request):
	response={}
	response['data'] = list(industry.objects.all().order_by('id').values('id','name'))
        response['status'] = 0
        response['message'] = 'ok'
	return HttpResponse(json.dumps(response, ensure_ascii = False))

#搜索
def search(request):
	response={}
	if 'contain' in request.GET and 'p' in request.GET:
                contain = request.GET['contain']
		p = int(request.GET['p'])*6
		obj_set = poineeringTag.objects.filter(name__contains=contain).all()
		obj = {}
		obj_list = []
		for item in obj_set:
			obj['name'] = item.name
                        obj['founder'] = item.account__name
                        obj['id'] = item.account__id
                        obj['headImg'] = 'http://120.25.12.205%s' %(item.account__headImg.url)
                        obj['startDate'] = item.startDate.strftime('%Y-%m-%d')
                        obj['summary'] = item.summary
                        obj['stage'] = item.stage
                        obj['direction1'] = item.direction1
                        obj['direction2'] = item.direction2
                        obj_list.append(obj)
		response['message'] = 'ok'
		response['data'] = obj_list
		response['status'] = 0

	return HttpResponse(json.dumps(response, ensure_ascii = False))

#创业圈内页
def projectInfo(request):
	response={}
	if 'sid' in request.GET and 'index' in request.GET:
		sid = int(request.GET['sid'])
		index = int(request.GET['index'])
		visibility = visualbility.objects.get(account_id=sid)
		obj = []
		if index == 1:
			if visibility.executiveSum == True:
                        	obj = executiveSum.objects.get(account=sid)
                        	first = obj.idea
                        	second = obj.targetCustomer
                        	third = obj.incomeChannel
                        	fourth = obj.competitor
                        	fifth = obj.investmentCost
                        	content=[first,second,third,fourth,fifth]
                        	response['data'] = content
                        	response['status'] = 0
                        	response['message'] = 'ok'
			else:
				response['message'] = 'ok'
                                response['status'] = 0
                                response['data'] = 'private'

                        return HttpResponse(json.dumps(response, ensure_ascii = False))
                if index == 2:
			if visibility.product == True:
                        	obj = product.objects.get(account=sid)
                        	first = obj.consumer
                        	second = obj.profitSupply
                        	third = obj.advantage
                        	fourth = obj.developmentStatus
                        	fifth = obj.patent
                        	content=[first,second,third,fourth,fifth]
                        	response['data'] = content
                        	response['status'] = 0
                        	response['message'] = 'ok'
			else:
				response['message'] = 'ok'
                                response['status'] = 0
                                response['data'] = 'private'

                        return HttpResponse(json.dumps(response, ensure_ascii = False))
                if index == 3:
			if visibility.competition == True:
                        	obj = competition.objects.get(account=sid)
                       		first = obj.tradeCondition
                        	second = obj.marketSclae
                        	third = obj.attracttion
                        	fourth = obj.competitionProduct
                        	fifth = obj.competitveFactor
                        	content=[first,second,third,fourth,fifth]
                        	response['data'] = content
                        	response['status'] = 0
                        	response['message'] = 'ok'
			else:
                                response['message'] = 'ok'
                                response['status'] = 0
                                response['data'] = 'private'

                        return HttpResponse(json.dumps(response, ensure_ascii = False))
                if index == 4:
                        if visibility.sales == True:
				obj = sales.objects.get(account=sid)
                       		first = obj.attractiveWay
                        	second = obj.pricingFactor
                        	third = obj.marketingProgram
                        	fourth = obj.salesWay
                        	content=[first,second,third,fourth]
                        	response['data'] = content
                        	response['status'] = 0
				response['message'] = 'ok'

			else:
                                response['message'] = 'ok'
                                response['status'] = 0
                                response['data'] = 'private'
                        
                        return HttpResponse(json.dumps(response, ensure_ascii = False)) 
		if index == 5:
			if visibility.sales == True:	
	                        obj = businessModel.objects.get(account=sid)
                        	first = obj.coreWork
                        	second = obj.resource
                        	third = obj.profitChannel
                        	content=[first,second,third]
                        	response['data'] = content
                        	response['status'] = 0
                        	response['message'] = 'ok'
			else:
				response['message'] = 'ok'
                                response['status'] = 0
                                response['data'] = 'private'
		
                        return HttpResponse(json.dumps(response, ensure_ascii = False))
		if index == 6:
			if visibility.teamManagement == True:
				obj_set = teamManagement.objects.filter(account=uid).all()
	                        obj_list = []
        	                for item in onj_set:
                	                obj = {}
                        	        obj['id'] = item.id
                                	obj['name'] = item.name
                                	obj_list.append(obj)
	                        response['data'] = obj_list
        	                response['status'] = 0
                	        response['message'] = 'ok'
			else:
                                response['message'] = 'ok'
                                response['status'] = 0
                                response['data'] = 'private'

                                return HttpResponse(json.dumps(response, ensure_ascii = False))
		if index == 7:
			if visibility.implementationPlan == True:
				obj = implementationPlan.objects.get(account=sid)
				first = obj.keyStage
                        	second = obj.workPlan
                        	third = obj.planRequest
                        	content=[first,second,third]
                        	response['data'] = content
                        	response['status'] = 0
                        	response['message'] = 'ok'
			else:
                                response['message'] = 'ok'
                                response['status'] = 0
                                response['data'] = 'private'

                        	return HttpResponse(json.dumps(response, ensure_ascii = False))
		if index == 8:
			if visibility.finacing == True:
				obj = finacing.objects.get(account=sid)
				if obj.cashFlow:
					first = "http://120.25.12.205%s"%(obj.cashFlow.url)
				else:
					first = 'not exist'
	                        if obj.profitAndLoss:
					second = "http://120.25.12.205%s"%(obj.profitAndLoss.url)
				else:
					second = 'not exist'
				if obj.assetAndLiabitilities:
        	                	third = "http://120.25.12.205%s"%(obj.assetAndLiabitilities.url)
				else:
					third = 'not exist'
                	        content = [first,second,third]
                        	response['data'] = content
                        	response['status'] = 0
                        	response['message'] = 'ok'
			else:
                                response['message'] = 'ok'
                                response['status'] = 0
                                response['data'] = 'private'

                        	return HttpResponse(json.dumps(response, ensure_ascii = False))
		if index == 9:
			if visibility.opportunitiesAndRisks == True:
				obj = opportunitiesAndRisks.objects.get(account=sid)
                        	first = obj.opportunities
                        	second = obj.risks
                        	content = [first,second]
                        	response['data'] = content
				response['status'] = 0
                                response['message'] = 'ok'
			else:
                                response['message'] = 'ok'
                                response['status'] = 0
                                response['data'] = 'private'

				return HttpResponse(json.dumps(response, ensure_ascii = False))
	else:
		response['message'] = 'miss some parameter'
		response['status'] = 404
		response['data'] = None
	return HttpResponse(json.dumps(response, ensure_ascii = False))

#投资圈内页
def investInfo(request):
	response={}
	if 'sid' in request.GET:
		invest = investmentInfo.objects.get(account_id=request.GET['sid'])
		obj = {}
                obj['summary'] = invest.summary
		obj['team'] = invest.team
		obj['phase'] = invest.phase
		obj['assembly'] = invest.assembly

		response['status'] = 0 
		response['message'] = 'ok'
		response['data'] = obj
	else:
		response['message'] = 'miss some parameter'
                response['status'] = 404
                response['data'] = None
        return HttpResponse(json.dumps(response, ensure_ascii = False))

#官网主页
def official_page(request):
        t = get_template('index.html')
        html = t.render(Context(None))
        return HttpResponse(html)
