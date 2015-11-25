#-*- coding: utf-8 -*-
#用于处理模板和网页的访问
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
from django import forms

from up.models import *
import json
from django.template.loader import get_template
from django.template import Context
import re
import sys

reload(sys)

sys.setdefaultencoding('utf8')

#官网主页
def official_page(request):
        t = get_template('index.html')
        html = t.render(Context(None))
        return HttpResponse(html)

#手机注册页面
def register_phone(request):
	t = get_template('register.html')
	html = t.render(Context(None))
        return HttpResponse(html)

#邮箱注册页面
def register_mail(request):
        t = get_template('register3.html')
        html = t.render(Context(None))
        return HttpResponse(html)

#注册成功页
def success(request):
	t = get_template('success.html')
	if 'mail' in request.GET:
		html = t.render(Context({'mail':request.GET['mail']}))
	else:
		html = t.render(Context({'phone':request.GET['phone']}))
	return HttpResponse(html)
#用户协议
def protocol(request):
        t = get_template('protocol.html')
        html = t.render(Context(None))
        return HttpResponse(html)

#登录页
def web_login(request):
	t = get_template('login.html')
        html = t.render(Context(None))
        return HttpResponse(html)

#登录主页
def mainpage(request):
	userid = int(request.session.get('userid',0))
	#如果session中的userid不存在，则回到登录页面
	if userid == 0:
		
		return HttpResponseRedirect('/web_login/')
	else:
		user = BasedInfo.objects.get(id=userid)
		user_info = DetailInfo.objects.get(account_id=user.id)
		
		person = {}	    
		person['id'] = userid
		person['name'] = user.name
		person['form'] = user.form
		person['img'] = 'http://120.25.12.205%s' %(user.headImg.url)
		person['province'] = user_info.province
		person['city'] = user_info.city
		person['school'] = user_info.school
		person['company'] = user_info.workingCompany
		if user.phone:
			person['phone'] = user.phone
		else:
			person['mail'] = user.mail
		if user_info.sex == '男':
			person['is_male'] = True
		else:
			person['is_male'] = False

		if user.form == '创业者':
			person['is_poineer'] = True
			projectInfo = poineeringTag.objects.get(account_id=user.id)
			project = {}
			project['name'] = projectInfo.name
			project['fund'] = projectInfo.fund
			project['summary'] = projectInfo.summary
			project['stage'] = projectInfo.stage
			project['direction1'] = projectInfo.direction1
			project['direction2'] = projectInfo.direction2
		
			ExecutiveSum = executiveSum.objects.get(tag_id=projectInfo.id)
			execut = {}
			execut['idea'] = ExecutiveSum.idea
			execut['targetCustomer'] = ExecutiveSum.targetCustomer
			execut['incomeChannel'] = ExecutiveSum.incomeChannel
			execut['competitor'] = ExecutiveSum.competitor
			execut['investmentCost'] = ExecutiveSum.investmentCost

			Product = product.objects.get(tag_id=projectInfo.id)
			prod = {}
			prod['consumer'] = Product.consumer
			prod['profitSupply'] = Product.profitSupply
			prod['advantage'] = Product.advantage
			prod['developmentStatus'] = Product.developmentStatus
			prod['patent'] = Product.patent

			Competition = competition.objects.get(tag_id=projectInfo.id)
			comp = {}
			comp['tradeCondition'] = Competition.tradeCondition
			comp['marketSclae'] = Competition.marketSclae
			comp['attracttion'] = Competition.attracttion
			comp['competitionProduct'] = Competition.competitionProduct
			comp['competitveFactor'] = Competition.competitveFactor

			Sales = sales.objects.get(tag_id=projectInfo.id)
			sale = {}
			sale['attractiveWay'] = Sales.attractiveWay
			sale['pricingFactor'] = Sales.pricingFactor
			sale['marketingProgram'] = Sales.marketingProgram
			sale['salesWay'] = Sales.salesWay

			BusinessModel = businessModel.objects.get(tag_id=projectInfo.id)
			business = {}
			business['coreWork'] = BusinessModel.coreWork
			business['resource'] = BusinessModel.resource
			business['profitChannel'] = BusinessModel.profitChannel

			ImplementationPlan = implementationPlan.objects.get(tag_id=projectInfo.id)
			implement = {}
			implement['keyStage'] = ImplementationPlan.keyStage
			implement['workPlan'] = ImplementationPlan.workPlan
			implement['planRequest'] = ImplementationPlan.planRequest

			Finacing = finacing.objects.get(tag_id=projectInfo.id)
			finace ={}
			if Finacing.cashFlow:
				finace['cashFlow'] = Finacing.cashFlow
			if Finacing.profitAndLoss:
                                finace['profitAndLoss'] = Finacing.profitAndLoss
			if Finacing.assetAndLiabitilities:
                                finace['assetAndLiabitilities'] = Finacing.assetAndLiabitilities

			OpportunitiesAndRisks = opportunitiesAndRisks.objects.get(tag_id=projectInfo.id)
			opport = {}
			opport['opportunities'] = OpportunitiesAndRisks.opportunities
			opport['risks'] = OpportunitiesAndRisks.risks

			visibility = visualbility.objects.get(account_id=userid)
			visible = {}
			visible['executiveSum'] = visibility.executiveSum
			visible['product'] = visibility.product
			visible['sales'] = visibility.sales
			visible['competition'] = visibility.competition
			visible['businessModel'] = visibility.businessModel
			visible['teamManagement'] = visibility.teamManagement
			visible['implementationPlan'] = visibility.implementationPlan
			visible['opportunitiesAndRisks'] = visibility.opportunitiesAndRisks
			visible['finacing'] = visibility.finacing

			t = get_template('mainpage.html')
			html = t.render(Context({'user':person,'project':project,'executiveSum':execut,'product':prod,'competition':comp,'sales':sale,'businessModel':business,'implementationPlan':implementationPlan,'finacing':finace,'opportunitiesAndRisks':opport,'visible':visible}))
		
			return HttpResponse(html)
		else:
			person['is_poineer'] = False
			projectInfo = investmentInfo.objects.get(account_id=user.id)
			project = {}
			project['company'] = projectInfo.company
			project['summary'] = projectInfo.summary
			project['stage'] = projectInfo.stage
			project['phase'] = projectInfo.phase
			project['direction1'] = projectInfo.direction1
			project['direction2'] = projectInfo.direction2
			project['mail'] = projectInfo.mail
			project['team'] = projectInfo.team
			project['assembly'] = projectInfo.assembly
			
			t = get_template('mainpage.html')
                        html = t.render(Context({'user':person,'project':project}))

			return HttpResponse(html)

@csrf_exempt
#登录
def login(request):
        response={}
        if 'mail' in request.POST and 'password' in request.POST:
                try:
                    user = BasedInfo.objects.get(mail=request.POST['mail'])
                    if user:
                            psd = request.POST['password']
                            if psd == user.password:

			  	    user.is_logined = True
				    user.save()

				    request.session.flush()
                                    request.session['userid'] = user.id
				    request.session['mail'] = user.mail
					
				    response['status'] = 0
                                    response['message'] = 'ok'
                            else:
                                    response['message'] = 'wrong password'
                                    response['status'] = 404
                                    response['data'] = None
                except ObjectDoesNotExist:
                    response['message'] = 'account do not exist'
                    response['status'] = 404
                    response['data'] = None
        elif 'phone' in request.POST and 'password' in request.POST:
                try:
                    user = BasedInfo.objects.get(phone=request.POST['phone'])
                    if user:
                            psd = request.POST['password']
                            if psd == user.password:

                                    user.is_logined = True
				    user.save()

				    request.session.flush()
                                    request.session['userid'] = user.id
				    request.session['phone'] = user.phone

				    response['status'] = 0
                                    response['message'] = 'ok'
                            else:
                                    response['message'] = 'wrong password'
                                    response['status'] = 404
                                    response['data'] = None
                except ObjectDoesNotExist:
                    response['message'] = 'account do not exist'
		    response['status'] = 404
                    response['data'] = None
	else:
                response['message'] = 'miss some parameter'
                response['status'] = 404
                response['data'] = None

        return HttpResponse(json.dumps(response, ensure_ascii = False))

@csrf_exempt
#修改商业计划
def changePlanview(request):
	userid = int(request.session.get('userid',0))
        #如果session中的userid不存在，则回到登录页面
        if userid == 0:

                return HttpResponseRedirect('/web_login/')
        else:
		response={}
		if 'ex_index' in request.POST and 'in_index' in request.POST and 'content' in request.POST:
			ex_index = int(request.POST['ex_index'])
	                in_index = int(request.POST['in_index'])

        	        if ex_index == 1:
                	        obj = executiveSum.objects.get(account=userid)
                        	if in_index == 1:
                                	obj.idea = request.POST['content']
                                	obj.save()
                                	response['message'] = 'ok'
                               		response['status'] = 0
                                	response['data'] = None
                                
                                	return HttpResponse(json.dumps(response, ensure_ascii = False))
                        	if in_index == 2:
                                	obj.targetCustomer = request.POST['content']
                                	obj.save()
                                	response['message'] = 'ok'
                                	response['status'] = 0
                                	response['data'] = None

                                	return HttpResponse(json.dumps(response, ensure_ascii = False))
                        	if in_index == 3:
                                	obj.incomeChannel = request.POST['content']
                                	obj.save()
                                	response['message'] = 'ok'
                                	response['status'] = 0
                                	response['data'] = None

                                	return HttpResponse(json.dumps(response, ensure_ascii = False))
                        	if in_index == 4:
                                	obj.competitor = request.POST['content']
                                	obj.save()
                                	response['message'] = 'ok'
                                	response['status'] = 0
                                	response['data'] = None

                                	return HttpResponse(json.dumps(response, ensure_ascii = False))
                        	if in_index == 5:
                                	obj.investmentCost = request.POST['content']
                                	obj.save()
                                	response['message'] = 'ok'
                                	response['status'] = 0
                                	response['data'] = None
                        
                                	return HttpResponse(json.dumps(response, ensure_ascii = False))
                	if ex_index == 2:
                        	obj = product.objects.get(account=userid)
                        	if in_index == 1:
                                	obj.consumer = request.POST['content']
                                	obj.save()
                                	response['message'] = 'ok'
                                	response['status'] = 0
                                	response['data'] = None
                                
                                	return HttpResponse(json.dumps(response, ensure_ascii = False))
                        	if in_index == 2:
                                	obj.profitSupply = request.POST['content']
                                	obj.save()
                                	response['message'] = 'ok'
                                	response['status'] = 0
                                	response['data'] = None

                                	return HttpResponse(json.dumps(response, ensure_ascii = False))
                        	if in_index == 3:
                                	obj.advantage = request.POST['content']
                                	obj.save()
                                	response['message'] = 'ok'
                                	response['status'] = 0
                                	response['data'] = None

                                	return HttpResponse(json.dumps(response, ensure_ascii = False))
                        	if in_index == 4:
                                	obj.developmentStatus = request.POST['content']
                                	obj.save()
                                	response['message'] = 'ok'
                                	response['status'] = 0
                                	response['data'] = None

                                	return HttpResponse(json.dumps(response, ensure_ascii = False))
                        	if in_index == 5:
                                	obj.patent = request.POST['content']
                                	obj.save()
                                	response['message'] = 'ok'
                                	response['status'] = 0
                                	response['data'] = None 
                        
                                	return HttpResponse(json.dumps(response, ensure_ascii = False))
                	if ex_index == 3:
                        	obj = competition.objects.get(account=userid)
                        	if in_index == 1:
                        	        obj.tradeCondition = request.POST['content']
                                	obj.save()
                                	response['message'] = 'ok'
                                	response['status'] = 0
                                	response['data'] = None
                                	
                                	return HttpResponse(json.dumps(response, ensure_ascii = False))
                        	if in_index == 2:
                        	        obj.marketSclae = request.POST['content']
                        	        obj.save()
                        	        response['message'] = 'ok'
                        	        response['status'] = 0
                        	        response['data'] = None
	
	                                return HttpResponse(json.dumps(response, ensure_ascii = False))
                        	if in_index == 3:
                                	obj.attracttion = request.POST['content']
                                	obj.save()
                                	response['message'] = 'ok'
					response['status'] = 0
                                        response['data'] = None

                                	return HttpResponse(json.dumps(response, ensure_ascii = False))
	                        if in_index == 4:
        	                        obj.competitionProduct = request.POST['content']
                	                obj.save()
                        	        response['message'] = 'ok'
                                	response['status'] = 0
                                	response['data'] = None

                                	return HttpResponse(json.dumps(response, ensure_ascii = False))
                        	if in_index == 5:
                        	        obj.competitveFactor = request.POST['content']
                        	        obj.save()
                        	        response['message'] = 'ok'
                        	        response['status'] = 0
                        	        response['data'] = None
                        	
                        	        return HttpResponse(json.dumps(response, ensure_ascii = False))
                	if ex_index == 4:
                        	obj = sales.objects.get(account=userid)
                        	if in_index == 1:
                                	obj.attractiveWay = request.POST['content']
                                	obj.save()
                                	response['message'] = 'ok'
                                	response['status'] = 0
                                	response['data'] = None
                                	
                                	return HttpResponse(json.dumps(response, ensure_ascii = False))
                        	if in_index == 2:
                        	        obj.pricingFactor = request.POST['content']
                        	        obj.save()
                        	        response['message'] = 'ok'
                        	        response['status'] = 0
                        	        response['data'] = None
	
	                                return HttpResponse(json.dumps(response, ensure_ascii = False))
                        	if in_index == 3:
                        	        obj.marketingProgram = request.POST['content']
                        	        obj.save()
                        	        response['message'] = 'ok'
                        	        response['status'] = 0
                        	        response['data'] = None

                        	        return HttpResponse(json.dumps(response, ensure_ascii = False))
                        	if in_index == 4:
                        	        obj.salesWay = request.POST['content']
                                	obj.save()
                                	response['message'] = 'ok'
                                	response['status'] = 0
                                	response['data'] = None
                                	return HttpResponse(json.dumps(response, ensure_ascii = False))
                	if ex_index == 5:
                        	obj = businessModel.objects.get(account=userid)
                        	if in_index == 1:
                        	        obj.coreWork = request.POST['content']
                                	obj.save()
                                	response['message'] = 'ok'
                                	response['status'] = 0
                                	response['data'] = None
                                
                                	return HttpResponse(json.dumps(response, ensure_ascii = False))
                        	if in_index == 2:
                                	obj.resource = request.POST['content']
                                	obj.save()
                                	response['message'] = 'ok'
                                	response['status'] = 0
                                	response['data'] = None

                                	return HttpResponse(json.dumps(response, ensure_ascii = False))
                        	if in_index == 3:
                                	obj.profitChannel = request.POST['content']
                                	obj.save()
                                	response['message'] = 'ok'
                                	response['status'] = 0
                                	response['data'] = None

                                	return HttpResponse(json.dumps(response, ensure_ascii = False))
			if ex_index == 6:
				mid = int(request.POST['in_index'])
				obj = teamManagement.objects.get(account=userid,id=mid)
				obj.name = request.POST['content']
				obj.save()
				response['message'] = 'ok'
                        	response['status'] = 0
                        	response['data'] = None

                        	return HttpResponse(json.dumps(response, ensure_ascii = False))

			if ex_index == 7:
				obj = implementationPlan.objects.get(account=userid)
				if in_index == 1:
					obj.keyStage = request.POST['content']
					obj.save()
                                	response['message'] = 'ok'
                                	response['status'] = 0
                                	response['data'] = None

					return HttpResponse(json.dumps(response, ensure_ascii = False))
				if in_index == 2:
					obj.workPlan = request.POST['content']
                                	obj.save()
                                	response['message'] = 'ok'
                                	response['status'] = 0
                                	response['data'] = None

					return HttpResponse(json.dumps(response, ensure_ascii = False))
				if in_index == 3:
					obj.planRequest = request.POST['content']
                                	obj.save()
                                	response['message'] = 'ok'
                                	response['status'] = 0
                                	response['data'] = None
                        
                                	return HttpResponse(json.dumps(response, ensure_ascii = False))
			if ex_index == 8:
				pass
			if ex_index == 9:
				obj = opportunitiesAndRisks.objects.get(account=userid)
				if in_index == 1:
					obj.opportunities = request.POST['content']
                                	obj.save()
                                	response['message'] = 'ok'
                                	response['status'] = 0
                                	response['data'] = None
			
					return HttpResponse(json.dumps(response, ensure_ascii = False))
				if in_index == 2:
					obj.risks = request.POST['content']
                                	obj.save()
                                	response['message'] = 'ok'
                                	response['status'] = 0
                                	response['data'] = None

                                	return HttpResponse(json.dumps(response, ensure_ascii = False))			
			else:
				response['message'] = 'miss some parameter 2'
	                	response['status'] = 404

			return HttpResponse(json.dumps(response, ensure_ascii = False))
		else:
			response['message'] = 'miss some parameter 1'
                        response['status'] = 404
	
			return HttpResponse(json.dumps(response, ensure_ascii = False))
			
@csrf_exempt
#修改个人信息
def changeTag(request):
        userid = int(request.session.get('userid',0))
        #如果session中的userid不存在，则回到登录页面
        if userid == 0:

                return HttpResponseRedirect('/web_login/')
        else:
                response={}
		project = poineeringTag.objects.get(account_id=userid)

		project.name = request.POST['name']
		project.fund = request.POST['fund']
		project.summary = request.POST['summary']
		project.direction1 = request.POST['direction1']
		project.direction2 = request.POST['direction2']
		project.stage = request.POST['stage']
		project.save()

		response['message'] = 'ok'
                response['status'] = 0
                response['data'] = None

		return HttpResponse(json.dumps(response, ensure_ascii = False))

@csrf_exempt
#改变可见性
def shift_visuality(request):
        userid = int(request.session.get('userid',0))
        #如果session中的userid不存在，则回到登录页面
        if userid == 0:

                return HttpResponseRedirect('/web_login/')
        else:
                response={}
		if 'index' in request.POST and 'choice' in request.POST:
                	visibility = visualbility.objects.get(account=userid)
                	index = int(request.POST['index'])
			
			
			if index == 1:
				if request.POST['choice'] == 'yes':
					visibility.executiveSum = True
				else:
					visibility.executiveSum = False
				visibility.save()
				response['status'] = 0
				response['message'] = 'ok'

				return HttpResponse(json.dumps(response, ensure_ascii = False))
                	if index == 2:
                        	if request.POST['choice'] == 'yes':
                                	visibility.product = True
                        	else:
                                	visibility.product = False
                        	visibility.save()
				response['status'] = 0
                        	response['message'] = 'ok'

                        	return HttpResponse(json.dumps(response, ensure_ascii = False))
                	if index == 3:
                        	if request.POST['choice'] == 'yes':
                        	        visibility.competition = True
                       		else:
                        	        visibility.competition = False
                        	visibility.save()
				response['status'] = 0
                        	response['message'] = 'ok'

                        	return HttpResponse(json.dumps(response, ensure_ascii = False))
                	if index == 4:
                        	if request.POST['choice'] == 'yes':
                        	        visibility.sales = True
                        	else:
                        	        visibility.sales = False
                        	visibility.save()
				response['status'] = 0
                        	response['message'] = 'ok'

                        	return HttpResponse(json.dumps(response, ensure_ascii = False))
                	if index == 5:
                        	if request.POST['choice'] == 'yes':
                        	        visibility.businessModel = True
                        	else:
                        	        visibility.businessModel = False
                        	visibility.save()
				response['status'] = 0
                        	response['message'] = 'ok'

                        	return HttpResponse(json.dumps(response, ensure_ascii = False))
			
			if index == 6:
				if request.POST['choice'] == 'yes':
                                	visibility.teamManagement = True
                        	else:
                        	        visibility.teamManagement = False
                        	visibility.save()
                        	response['status'] = 0
                        	response['message'] = 'ok'

				return HttpResponse(json.dumps(response, ensure_ascii = False))
			if index == 7:
				if request.POST['choice'] == 'yes':
                        	        visibility.implementationPlan = True
                        	else:
                        	        visibility.implementationPlan = False
                        	visibility.save()
                        	response['status'] = 0
                        	response['message'] = 'ok'

                        	return HttpResponse(json.dumps(response, ensure_ascii = False))
			if index == 8:
				if request.POST['choice'] == 'yes':
                        	        visibility.finacing = True
                        	else:
                        	        visibility.finacing = False
                        	visibility.save()
                        	response['status'] = 0
                        	response['message'] = 'ok'

                        	return HttpResponse(json.dumps(response, ensure_ascii = False))
			if index == 9:
				if request.POST['choice'] == 'yes':
                        	        visibility.opportunitiesAndRisks = True
                        	else:
                        	        visibility.opportunitiesAndRisks = False
                        	visibility.save()
                        	response['status'] = 0
                        	response['message'] = 'ok'

                		return HttpResponse(json.dumps(response, ensure_ascii = False))

#创建表单来处理图片
class pictureForm(forms.Form):
    userid = forms.CharField()
    headImg = forms.FileField()

#上传头像
@csrf_exempt
def uploadImg(request):
        response={}
        if request.method == "POST":
                pf = pictureForm(request.POST,request.FILES)
                if pf.is_valid():
                        uid = pf.cleaned_data['userid']
                        picture = pf.cleaned_data['headImg']
                        user = BasedInfo.objects.get(id=uid)
                        user.headImg = picture
                        user.save()

                        response['message'] = 'ok'
                        response['status'] = 0

		return HttpResponseRedirect('/mainpage/')

        else:
                response['message'] = 'failed'
                response['status'] = 404

        	return HttpResponse(json.dumps(response, ensure_ascii = False))

@csrf_exempt
#修改投资信息
def changeInvestTag(request):
        userid = int(request.session.get('userid',0))
        #如果session中的userid不存在，则回到登录页面
        if userid == 0:

                return HttpResponseRedirect('/web_login/')
        else:
                response={}
                project = investmentInfo.objects.get(account_id=userid)

                project.company = request.POST['company']
                project.phase = request.POST['phase']
                project.summary = request.POST['summary']
                project.direction1 = request.POST['direction1']
                project.direction2 = request.POST['direction2']
                project.stage = request.POST['stage']
		project.team = request.POST['team']
		project.assembly = request.POST['assembly']
		project.mail = request.POST['mail']
                project.save()

                response['message'] = 'ok'
                response['status'] = 0
                response['data'] = None

                return HttpResponse(json.dumps(response, ensure_ascii = False))

#获取创业板
def poineeringCircle(request):
	userid = int(request.session.get('userid',0))
        #如果session中的userid不存在，则回到登录页面
        if userid == 0:

                return HttpResponseRedirect('/web_login/')
        else:
		direction_list = list(industry.objects.values('id','name'))

		if request.GET['direction1'] == '0' and request.GET['direction2'] == '0':
			p = int(request.GET['p'])*10
			obj_set = poineeringTag.objects.exclude(name='').exclude(name=None).order_by('last_modified')[p-10:p]
			count = int(poineeringTag.objects.exclude(name='').exclude(name=None).count()/10)+1
                        obj_list = []
                        for item in obj_set:
                                obj = {}
                                obj['name'] = item.name
                                obj['founder'] = item.account.name
                                obj['id'] = item.account.id
                                obj['headImg'] = 'http://120.25.12.205%s' %(item.account.headImg.url)
                                obj['startDate'] = item.startDate.strftime('%Y-%m-%d')
                                obj['summary'] = item.summary

				#判断阶段
                                if item.stage == '精炼创意中':
					obj['idea'] = True
				elif item.stage == '组建团队中':
					obj['team'] = True
				elif item.stage == '产品开发中':
					obj['product'] = True
				elif item.stage == '正式运营中':
					obj['running'] = True

                                obj['fund'] = item.fund
                                obj['province'] = DetailInfo.objects.get(account_id=item.account_id).province
                                obj['city'] = DetailInfo.objects.get(account_id=item.account_id).city
                                obj['direction1'] = item.direction1
                                obj['direction2'] = item.direction2
                                obj_list.append(obj)
			t = get_template('poineeringCircle.html')
                        html = t.render(Context({'direction_list':direction_list,'obj_list':obj_list,'count':count,'p':p/10}))

                        return HttpResponse(html)
		else:
			p = int(request.GET['p'])*10
			
			if request.GET['direction1'] == '0':
				Industry = industry.objects.get(id = request.GET['direction2'])
                                obj_set = Industry.item.exclude(name='').exclude(name=None).order_by('last_modified')[p-10:p]
				count = Industry.item.exclude(name='').exclude(name=None).count()
				obj_list = []
                                for item in obj_set:
                                        obj = {}
                                        obj['name'] = item.name
                                        obj['founder'] = item.account.name
                                        obj['id'] = item.account.id
                                        obj['headImg'] = 'http://120.25.12.205%s' %(item.account.headImg.url)
                                        obj['startDate'] = item.startDate.strftime('%Y-%m-%d')
                                        obj['province'] = DetailInfo.objects.get(account_id=item.account_id).province
                                        obj['city'] = DetailInfo.objects.get(account_id=item.account_id).city
                                        obj['summary'] = item.summary
					
					#判断阶段
                                	if item.stage == '精炼创意中':
                                        	obj['idea'] = True
                                	elif item.stage == '组建团队中':
                                        	obj['team'] = True
                                	elif item.stage == '产品开发中':
                                        	obj['product'] = True
                                	elif item.stage == '正式运营中':
                                        	obj['running'] = True
                                        obj['fund'] = item.fund
                                        obj['direction1'] = item.direction1
                                        obj['direction2'] = item.direction2
                                        obj_list.append(obj)
			elif request.GET['direction2'] == '0':
                                Industry = industry.objects.get(id = request.GET['direction1'])
                                obj_set = Industry.item.exclude(name='').exclude(name=None).order_by('last_modified')[p-10:p]
				count = Industry.item.exclude(name='').exclude(name=None).count()
                                obj_list = []
                                for item in obj_set:
                                        obj = {}
                                        obj['name'] = item.name
                                        obj['founder'] = item.account.name
                                        obj['id'] = item.account.id
                                        obj['headImg'] = 'http://120.25.12.205%s' %(item.account.headImg.url)
                                        obj['startDate'] = item.startDate.strftime('%Y-%m-%d')
                                        obj['province'] = DetailInfo.objects.get(account_id=item.account_id).province
                                        obj['city'] = DetailInfo.objects.get(account_id=item.account_id).city
                                        obj['summary'] = item.summary

					if item.stage == '精炼创意中':
                                                obj['idea'] = True
                                        elif item.stage == '组建团队中':
                                                obj['team'] = True
                                        elif item.stage == '产品开发中':
                                                obj['product'] = True
                                        elif item.stage == '正式运营中':
                                                obj['running'] = True

                                        obj['fund'] = item.fund
                                        obj['direction1'] = item.direction1
                                        obj['direction2'] = item.direction2
                                        obj_list.append(obj)
			else:
				Industry = industry.objects.get(id = request.GET['direction1'])
                                obj_set = Industry.item.exclude(name='').exclude(name=None).order_by('last_modified')[p/2-5:p/2]
				count = Industry.item.exclude(name='').exclude(name=None).count()
                                obj_list = []
                                for item in obj_set:
                                        obj = {}
                                        obj['name'] = item.name
                                        obj['founder'] = item.account.name
                                        obj['id'] = item.account.id
                                        obj['headImg'] = 'http://120.25.12.205%s' %(item.account.headImg.url)
                                        obj['startDate'] = item.startDate.strftime('%Y-%m-%d')
                                        obj['province'] = DetailInfo.objects.get(account_id=item.account_id).province
                                        obj['city'] = DetailInfo.objects.get(account_id=item.account_id).city
                                        obj['summary'] = item.summary

					if item.stage == '精炼创意中':
                                                obj['idea'] = True
                                        elif item.stage == '组建团队中':
                                                obj['team'] = True
                                        elif item.stage == '产品开发中':
                                                obj['product'] = True
                                        elif item.stage == '正式运营中':
                                                obj['running'] = True
					
                                        obj['fund'] = item.fund
                                        obj['direction1'] = item.direction1
                                        obj['direction2'] = item.direction2
                                        obj_list.append(obj)
				Industry = industry.objects.get(id = request.GET['direction2'])
                                obj_set = Industry.item.exclude(name='').exclude(name=None).order_by('last_modified')[p/2-5:p/2]
				count = Industry.item.exclude(name='').exclude(name=None).count()+count
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
		
						if item.stage == '精炼创意中':
                                                	obj['idea'] = True
                                        	elif item.stage == '组建团队中':
                                                	obj['team'] = True
                                        	elif item.stage == '产品开发中':
                                                	obj['product'] = True
                                        	elif item.stage == '正式运营中':
                                                	obj['running'] = True
                                        	obj['fund'] = item.fund
                                        	obj['direction1'] = item.direction1
                                        	obj['direction2'] = item.direction2
				
                                        obj_list.append(obj)
			t = get_template('poineeringCircle.html')
                        html = t.render(Context({'direction_list':direction_list,'obj_list':obj_list,'count':count/10+1,'p':p/10}))

                        return HttpResponse(html)

#获取创业板内页
def poineeringInfo(request):
	userid = int(request.session.get('userid',0))
        #如果session中的userid不存在，则回到登录页面
        if userid == 0:

                return HttpResponseRedirect('/web_login/')
        else:
		sid = request.GET['sid']
		user = BasedInfo.objects.get(id=sid)
                user_info = DetailInfo.objects.get(account_id=user.id)

                person = {}
                person['id'] = userid
                person['name'] = user.name
                person['headImg'] = 'http://120.25.12.205%s' %(user.headImg.url)
                person['province'] = user_info.province
                person['city'] = user_info.city
                person['school'] = user_info.school
                person['company'] = user_info.workingCompany

		projectInfo = poineeringTag.objects.get(account_id=user.id)
                project = {}
                project['name'] = projectInfo.name
                project['fund'] = projectInfo.fund
                project['summary'] = projectInfo.summary
                project['stage'] = projectInfo.stage
                project['direction1'] = projectInfo.direction1
                project['direction2'] = projectInfo.direction2

                ExecutiveSum = executiveSum.objects.get(tag_id=projectInfo.id)
                execut = {}
                execut['idea'] = ExecutiveSum.idea
                execut['targetCustomer'] = ExecutiveSum.targetCustomer
                execut['incomeChannel'] = ExecutiveSum.incomeChannel
                execut['competitor'] = ExecutiveSum.competitor
                execut['investmentCost'] = ExecutiveSum.investmentCost

                Product = product.objects.get(tag_id=projectInfo.id)
                prod = {}
                prod['consumer'] = Product.consumer
                prod['profitSupply'] = Product.profitSupply
                prod['advantage'] = Product.advantage
                prod['developmentStatus'] = Product.developmentStatus
                prod['patent'] = Product.patent

                Competition = competition.objects.get(tag_id=projectInfo.id)
                comp = {}
                comp['tradeCondition'] = Competition.tradeCondition
		comp['attracttion'] = Competition.attracttion
                comp['competitionProduct'] = Competition.competitionProduct
                comp['competitveFactor'] = Competition.competitveFactor

                Sales = sales.objects.get(tag_id=projectInfo.id)
                sale = {}
                sale['attractiveWay'] = Sales.attractiveWay
                sale['pricingFactor'] = Sales.pricingFactor
                sale['marketingProgram'] = Sales.marketingProgram
                sale['salesWay'] = Sales.salesWay

                BusinessModel = businessModel.objects.get(tag_id=projectInfo.id)
                business = {}
                business['coreWork'] = BusinessModel.coreWork
                business['resource'] = BusinessModel.resource
                business['profitChannel'] = BusinessModel.profitChannel

                ImplementationPlan = implementationPlan.objects.get(tag_id=projectInfo.id)
                implement = {}
                implement['keyStage'] = ImplementationPlan.keyStage
                implement['workPlan'] = ImplementationPlan.workPlan
                implement['planRequest'] = ImplementationPlan.planRequest

                Finacing = finacing.objects.get(tag_id=projectInfo.id)
                finace ={}
                if Finacing.cashFlow:
                        finace['cashFlow'] = Finacing.cashFlow
                if Finacing.profitAndLoss:
                        finace['profitAndLoss'] = Finacing.profitAndLoss
                if Finacing.assetAndLiabitilities:
                        finace['assetAndLiabitilities'] = Finacing.assetAndLiabitilities

                OpportunitiesAndRisks = opportunitiesAndRisks.objects.get(tag_id=projectInfo.id)
                opport = {}
		opport['opportunities'] = OpportunitiesAndRisks.opportunities
                opport['risks'] = OpportunitiesAndRisks.risks

                visibility = visualbility.objects.get(account_id=user.id)
                visible = {}
                visible['executiveSum'] = visibility.executiveSum
                visible['product'] = visibility.product
                visible['sales'] = visibility.sales
                visible['competition'] = visibility.competition
                visible['businessModel'] = visibility.businessModel
                visible['teamManagement'] = visibility.teamManagement
                visible['implementationPlan'] = visibility.implementationPlan
                visible['opportunitiesAndRisks'] = visibility.opportunitiesAndRisks
                visible['finacing'] = visibility.finacing

                t = get_template('poineeringInfo.html')
                html = t.render(Context({'user':person,'project':project,'executiveSum':execut,'product':prod,'competition':comp,'sales':sale,'businessModel':business,'implementationPlan':implementationPlan,'finacing':finace,'opportunitiesAndRisks':opport,'visible':visible}))

		return HttpResponse(html)


#获取投资源
def investmentCircle(request):
	userid = int(request.session.get('userid',0))
        #如果session中的userid不存在，则回到登录页面
        if userid == 0:

                return HttpResponseRedirect('/web_login/')
        else:
		direction_list = list(industry.objects.values('id','name'))

		p = int(request.GET['p'])*10
		obj_set = investmentInfo.objects.exclude(company='').exclude(company=None)[p-10:p]
		count = int(investmentInfo.objects.exclude(company='').exclude(company=None).count()/10)+1
                obj_list = []
                for item in obj_set:
                	obj = {}
			obj['id'] = item.id
                        obj['name'] = item.account.name
                        obj['headImg'] = 'http://120.25.12.205%s' %(item.account.headImg.url)
                        obj['phase'] = item.phase
                        obj['stage'] = item.stage
                        obj['company'] = item.company
			obj['mail'] = item.mail
                        obj['province'] = DetailInfo.objects.get(account_id=item.account_id).province
                        obj['city'] = DetailInfo.objects.get(account_id=item.account_id).city
                        obj['direction1'] = item.direction1
                        obj['direction2'] = item.direction2
                        obj_list.append(obj)
		t = get_template('investmentCircle.html')
                html = t.render(Context({'direction_list':direction_list,'obj_list':obj_list,'count':count,'p':p/10}))

                return HttpResponse(html)

#获取投资源内页
def investInfo(request):
        userid = int(request.session.get('userid',0))
        #如果session中的userid不存在，则回到登录页面
        if userid == 0:

                return HttpResponseRedirect('/web_login/')
        else:
		sid = int(request.GET['sid'])    #获取选取的项目id
		item = investmentInfo.objects.get(id=sid)
		obj = {}
		obj['company'] = item.company
		obj['direction1'] = item.direction1
		obj['direction2'] = item.direction2
		obj['headImg'] = 'http://120.25.12.205%s' %(item.account.headImg.url)
		obj['summary'] = item.summary
		obj['stage'] = item.stage
		obj['phase'] = item.phase
		obj['team'] = item.team
		obj['assembly'] = item.assembly
		obj['mail'] = item.mail
		obj['province'] = DetailInfo.objects.get(account_id=item.account_id).province
                obj['city'] = DetailInfo.objects.get(account_id=item.account_id).city
		obj['name'] = item.account.name

		t = get_template('investmentInfo.html')
		html = t.render(Context({'obj':obj}))

		return HttpResponse(html)

