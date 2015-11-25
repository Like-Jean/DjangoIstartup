#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django import forms
from up.models import *
import json
import re
import sys

reload(sys)

sys.setdefaultencoding('utf8')
#获取创业标签
def getTag(request):
	response={}
	if 'uid' in request.GET and request.GET['form']=='创业者' or request.GET['form']=='poineer':
		uid = int(request.GET['uid'])
		tag = poineeringTag.objects.get(account=uid)
		obj={}
		obj['name'] = tag.name
		obj['summary'] = tag.summary
		obj['stage'] = tag.stage
		obj['direction1'] = tag.direction1
		obj['direction2'] = tag.direction2
		obj['fund'] = tag.fund
		obj['time'] = tag.startDate.strftime('%Y-%m-%d')
		
		response['data'] = obj
		response['message'] = 'ok'
		response['status'] = 0
	elif 'uid' in request.GET and request.GET['form']=='投资者' or request.GET['form']=='investor':
                uid = int(request.GET['uid'])
                tag = investmentInfo.objects.get(account=uid)
                obj={}
                obj['company'] = tag.company
                obj['summary'] = tag.summary
                obj['stage'] = tag.stage
		obj['address'] = tag.mail
		obj['direction1'] = tag.direction1
		obj['direction2'] = tag.direction2
		obj['phase'] = tag.phase
		obj['assembly'] = tag.assembly
		obj['team'] = tag.team
                
                response['data'] = obj
                response['message'] = 'ok'
                response['status'] = 0

	else:
		response['message'] = 'miss some parameter'
                response['status'] = 404
		response['data'] = None

	return HttpResponse(json.dumps(response, ensure_ascii = False))

@csrf_exempt
#修改商业标签
def changeTag(request):
	response={}
	if 'uid' in request.POST and request.POST['form'] == '创业者' or request.POST['form']=='poineer':
		uid = int(request.POST['uid'])
		tag = poineeringTag.objects.get(account=uid)
		if 'name' in request.POST:
			tag.name = request.POST['name']
			tag.save()
			response['message'] = 'ok'
			response['status'] = 0

		if 'summary' in request.POST:
			tag.summary = request.POST['summary']
			tag.save()
                        response['message'] = 'ok'
                        response['status'] = 0

		if 'stage' in request.POST:
			tag.stage = request.POST['stage']
			tag.save()
                        response['message'] = 'ok'
                        response['status'] = 0

		if 'direction1' in request.POST:
			direction = industry.objects.get(id=request.POST['direction1'])
			direction.item.add(tag)
			direction.save()
			tag.direction1 = direction.name
			tag.save()
                        response['message'] = 'ok'
                        response['status'] = 0

		if 'direction2' in request.POST:
			direction = industry.objects.get(id=request.POST['direction2'])
                        direction.item.add(tag)
                        direction.save()
                        tag.direction2 = direction.name

			tag.save()
                        response['message'] = 'ok'
                        response['status'] = 0

		if 'fund' in request.POST:
			tag.fund = request.POST['fund']
                        tag.save()
                        response['message'] = 'ok'
                        response['status'] = 0
		if 'time' in request.POST:
			tag.startDate = request.POST['time']
			tag.save()
			response['message'] = 'ok'
                        response['status'] = 0		
			return HttpResponse(json.dumps(response, ensure_ascii = False))

	elif 'uid' in request.POST and request.POST['form'] == '投资者' or request.POST['form']=='investor':
		uid = int(request.POST['uid'])
                tag = investmentInfo.objects.get(account_id=uid)

		if 'company' in request.POST:
			tag.company = request.POST['company']
			tag.save()
		if 'stage' in request.POST:
			tag.stage = request.POST['stage']
			tag.save()
		if 'summary' in request.POST:
			tag.summary = request.POST['summary']
			tag.save()
		if 'mail' in request.POST:
			tag.mail = request.POST['mail']
			tag.save()
		if 'address' in request.POST:
			tag.mail = request.POST['address']
			tag.save()
		if 'direction1' in request.POST:
			tag.direction1 = request.POST['direction1']
			tag.save()
		if 'direction2' in request.POST:
			tag.direction2 = request.POST['direction2']
                        tag.save()
		if 'phase' in request.POST:
			tag.phase = request.POST['phase']
			tag.save()
		if 'assembly' in request.POST:
			tag.assembly = request.POST['assembly']
			tag.save()
		if 'team' in request.POST:
			tag.team = request.POST['team']
			tag.save()
		response['message'] = 'ok'
                response['status'] = 0
                return HttpResponse(json.dumps(response, ensure_ascii = False))
	else:
		response['message'] = 'miss some parameter'
                response['status'] = 404
	return HttpResponse(json.dumps(response, ensure_ascii = False))

#获取商业计划
def getPlan(request):
        response={}
        if 'uid' in request.GET and 'index' in request.GET:
                index = int(request.GET['index'])
                uid = int(request.GET['uid'])
                if index == 1:
                        obj = executiveSum.objects.get(account=uid)
                        first = obj.idea
                        second = obj.targetCustomer
                        third = obj.incomeChannel
                        fourth = obj.competitor
                        fifth = obj.investmentCost
                        content=[first,second,third,fourth,fifth]        
                        response['message'] = 'ok'
                        response['status'] = 0
                        response['data'] = content
                        
                        return HttpResponse(json.dumps(response, ensure_ascii = False))
                if index == 2:
                        obj = product.objects.get(account=uid)
                        first = obj.consumer
                        second = obj.profitSupply
                        third = obj.advantage
                        fourth = obj.developmentStatus
                        fifth = obj.patent
                        content=[first,second,third,fourth,fifth]        
                        response['message'] = 'ok'
                        response['status'] = 0
                        response['data'] = content
                         
                        return HttpResponse(json.dumps(response, ensure_ascii = False))
                if index == 3:
                        obj = competition.objects.get(account=uid)
                        first = obj.tradeCondition
                        second = obj.marketSclae
                        third = obj.attracttion
                        fourth = obj.competitionProduct
                        fifth = obj.competitveFactor
                        content=[first,second,third,fourth,fifth]        
                        response['message'] = 'ok'
                        response['status'] = 0
                        response['data'] = content

                        return HttpResponse(json.dumps(response, ensure_ascii = False))
                if index == 4:
                        obj = sales.objects.get(account=uid)
                        first = obj.attractiveWay
                        second = obj.pricingFactor
                        third = obj.marketingProgram
                        fourth = obj.salesWay
                        content=[first,second,third,fourth]        
                        response['data'] = content
                        response['status'] = 0
                        response['message'] = 'ok'
                       
                        return HttpResponse(json.dumps(response, ensure_ascii = False))
                if index == 5:
                        obj = businessModel.objects.get(account=uid)
                        first = obj.coreWork
                        second = obj.resource
                        third = obj.profitChannel
                        content=[first,second,third]        
                        response['message'] = 'ok'
                        response['status'] = 0
                        response['data'] = content
                        
                        return HttpResponse(json.dumps(response, ensure_ascii = False))
		if index == 6:
			obj_set = teamManagement.objects.filter(account=uid).all()
			obj_list = []
			for item in obj_set:
				obj = {}
				obj['id'] = item.id
				obj['name'] = item.name
				obj_list.append(obj)
			response['data'] = obj_list
			response['status'] = 0
			response['message'] = 'ok'

			return HttpResponse(json.dumps(response, ensure_ascii = False))
		if index == 7:
			obj = implementationPlan.objects.get(account=uid)
			first = obj.keyStage
			second = obj.workPlan
			third = obj.planRequest
			content=[first,second,third]
                        response['data'] = content
                        response['status'] = 0
                        response['message'] = 'ok'
			
			return HttpResponse(json.dumps(response, ensure_ascii = False))

		if index == 8:
			obj = finacing.objects.get(account=uid)
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

			return HttpResponse(json.dumps(response, ensure_ascii = False))
		if index == 9:
			obj = opportunitiesAndRisks.objects.get(account=uid)
			first = obj.opportunities
			second = obj.risks
			content = [first,second]
			response['data'] = content
                        response['status'] = 0
                        response['message'] = 'ok'

			return HttpResponse(json.dumps(response, ensure_ascii = False))
			
        else:
                response['message'] = 'miss some parameter'
                response['status'] = 404

        return HttpResponse(json.dumps(response, ensure_ascii = False))

@csrf_exempt
#创建团队成员
def addMember(request):
	response={}
	if 'uid' in request.POST and 'name' in request.POST:
		uid = int(request.POST['uid'])
		member = teamManagement(account=BasedInfo.objects.get(id=uid),tag=poineeringTag.objects.get(account=uid),name=request.POST['name'])
		member.save()
		response['message'] = 'ok'
		response['status'] = 0
		response['data'] = member.id
	else:
		response['message'] = 'miss some parameter'
                response['status'] = 404
		response['data'] = None

        return HttpResponse(json.dumps(response, ensure_ascii = False))

@csrf_exempt
#增加成员简历
def addResume(request):
	response={}
	if 'mid' in request.POST:
		mid = int(request.POST['mid'])
		Member = teamManagement.objects.get(id=mid)
		memberResume = memberInfo(member=Member)
		if 'place' in request.POST:
			memberResume.place = request.POST['place']
		if 'organization' in request.POST:
                        memberResume.organiztion = request.POST['organization']
		if 'position' in request.POST:
                        memberResume.position = request.POST['position']
		if 'introduction' in request.POST:
                        memberResume.introuduction = request.POST['introduction']
		if 'startYear' in request.POST:
                        memberResume.startYear = request.POST['startYear']
		if 'startMonth' in request.POST:
			memberResume.startMonth = request.POST['startMonth']
		if 'endMonth' in request.POST:
			memberResume.endMonth = request.POST['endMonth']
		if 'endYear' in request.POST:
			memberResume.endYear = request.POST['endYear']
		memberResume.save()

		response['message'] = 'ok'
		response['status'] = 0
		response['data'] = memberResume.id
	else:
		response['message'] = 'miss some parameter'
                response['status'] = 404
		response['data'] = None

	return HttpResponse(json.dumps(response, ensure_ascii = False))

@csrf_exempt
#删除团队成员
def deleteMember(request):
	response={}
	if 'mid' in request.POST:
		mid = int(request.POST['mid'])
		try:
		    memberInfo.objects.filter(member=mid).delete()
		except ObjectDoesNotExist:
		    pass
		teamManagement.objects.get(id=mid).delete()

		response['message'] = 'ok'
                response['status'] = 0

        else:
                response['message'] = 'miss some parameter'
                response['status'] = 404

        return HttpResponse(json.dumps(response, ensure_ascii = False))

#查看团队成员
def checkResume(request):
        response={}
        if 'mid' in request.GET:
		mid = int(request.GET['mid'])
                try:
                    memberinfo = memberInfo.objects.filter(member=mid).all()
		    if memberinfo:
			member_list = []
			for item in memberinfo:
				member={}
				member['id'] = item.id
				member['place'] = item.place
				member['organization'] = item.organiztion
				member['position'] = item.position
				member['introduction'] = item.introuduction
				member['startYear'] = item.startYear
				member['startMonth'] = item.startMonth
				member['endYear'] = item.endYear
				member['endMonth'] = item.endMonth
				member_list.append(member)
			response['status'] = 0
			response['message'] = 'ok'
			response['data'] = member_list

			return HttpResponse(json.dumps(response, ensure_ascii = False)) 
                except ObjectDoesNotExist:
			response['status'] = 0
                        response['message'] = 'ok'
                        response['data'] = ''
		
			return HttpResponse(json.dumps(response, ensure_ascii = False))
	else:
		response['message'] = 'miss some parameter'
                response['status'] = 404

        return HttpResponse(json.dumps(response, ensure_ascii = False))

@csrf_exempt
#修改团队成员简历
def updateResume(request):
	response={}
	if 'rid' in request.POST:
		response={}
		mid = int(request.POST['rid'])
		memberinfo = memberInfo.objects.get(id=mid)
		if 'place' in request.POST:
			memberinfo.place = request.POST['place']
			response['message'] = 'ok'
			response['status'] = 0
		if 'organization' in request.POST:
                        memberinfo.organiztion = request.POST['organization']
                        response['message'] = 'ok'
                        response['status'] = 0
		if 'position' in request.POST:
                        memberinfo.position = request.POST['position']
                        response['message'] = 'ok'
                        response['status'] = 0
                if 'introduction' in request.POST:
                        memberinfo.introuduction = request.POST['introduction']
                        response['message'] = 'ok'
                        response['status'] = 0
                if 'startYear' in request.POST:
                        memberinfo.startYear = request.POST['startYear']
                        response['message'] = 'ok'
                        response['status'] = 0
                if 'startMonth' in request.POST:
                        memberinfo.startMonth = request.POST['startMonth']
                        response['message'] = 'ok'
                        response['status'] = 0
                if 'endYear' in request.POST:
                        memberinfo.endYear = request.POST['endYear']
                        response['message'] = 'ok'
                        response['status'] = 0
                if 'endMonth' in request.POST:
                        memberinfo.endMonth = request.POST['endMonth']
                        response['message'] = 'ok'
                        response['status'] = 0
		memberinfo.save()
	else:
		response['message'] = 'miss some parameter'
                response['status'] = 404

        return HttpResponse(json.dumps(response, ensure_ascii = False))

@csrf_exempt
#删除成员简历
def deleteResume(request):
	response={}
	if 'rid' in request.POST:
		rid = request.POST['rid']
		memberInfo.objects.get(id=rid).delete()
		response['status'] = 0
		response['message'] = 'ok'
	else:
		response['message'] = 'miss some parameter'
                response['status'] = 404

	return HttpResponse(json.dumps(response, ensure_ascii = False))

#用以生成上传现金流表的表单
class cashflowForm(forms.Form):
	userid = forms.CharField()
	cashflow = forms.FileField()

#上传现金流表格
@csrf_exempt
def uploadCashflow(request):
	response={}
	if request.method == 'POST':
		cf = cashflowForm(request.POST,request.FILES)
		if cf.is_valid():
			uid = cf.cleaned_data['userid']
			cashflow = cf.cleaned_data['cashflow']
			finace = finacing.objects.get(account=uid)
			finace.cashFlow = cashflow
			finace.save()

			return  HttpResponseRedirect('/mainpage/')

        else:
                response['message'] = 'failed'
                response['status'] = 404

        return HttpResponse(json.dumps(response, ensure_ascii = False))

#用以生成上传收益资金表的表单
class profitAndLossForm(forms.Form):
	userid = forms.CharField()
        profitAndLoss = forms.FileField()

@csrf_exempt
#上传收益资金表
def uploadProfitAndLoss(request):
        response={}
        if request.method == 'POST':
                cf = profitAndLossForm(request.POST,request.FILES)
                if cf.is_valid():
                        uid = cf.cleaned_data['userid']
                        profitAndLoss = cf.cleaned_data['profitAndLoss']
                        finace = finacing.objects.get(account=uid)
                        finace.profitAndLoss = profitAndLoss
                        finace.save()

                        response['status'] = 0
                        response['message'] = 'ok'

			return  HttpResponseRedirect('/mainpage/')
        else:
                response['message'] = 'failed'
                response['status'] = 404

        return HttpResponse(json.dumps(response, ensure_ascii = False))

#用以生成上传机会风险表的表单
class opportunitiesAndRisksForm(forms.Form):
        userid = forms.CharField()
        opportunitiesAndRisks = forms.FileField()

@csrf_exempt
#上传机会与风险表
def uploadOpportunitiesAndRisks(request):
        response={}
        if request.method == 'POST':
                cf = opportunitiesAndRisksForm(request.POST,request.FILES)
                if cf.is_valid():
                        uid = cf.cleaned_data['userid']
                        opportunitiesAndRisks = cf.cleaned_data['opportunitiesAndRisks']
                        finace = finacing.objects.get(account=uid)
                        finace.opportunitiesAndRisks = opportunitiesAndRisks
                        finace.save()

                        response['status'] = 0
                        response['message'] = 'ok'

			return  HttpResponseRedirect('/mainpage/')
        else:
                response['message'] = 'failed'
                response['status'] = 404

        return HttpResponse(json.dumps(response, ensure_ascii = False))

@csrf_exempt
#修改商业计划
def changePlan(request):
        response={}
        if 'uid' in request.POST and 'ex_index' in request.POST and 'in_index' in request.POST and 'content' in request.POST:
                uid = int(request.POST['uid'])
                ex_index = int(request.POST['ex_index'])
                in_index = int(request.POST['in_index'])

                if ex_index == 1:
                        obj = executiveSum.objects.get(account=uid)
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
                        obj = product.objects.get(account=uid)
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
                        obj = competition.objects.get(account=uid)
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
                        obj = sales.objects.get(account=uid)
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
                        obj = businessModel.objects.get(account=uid)
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
			obj = teamManagement.objects.get(account=uid,id=mid)
			obj.name = request.POST['content']
			obj.save()
			response['message'] = 'ok'
                        response['status'] = 0
                        response['data'] = None

                        return HttpResponse(json.dumps(response, ensure_ascii = False))

		if ex_index == 7:
			obj = implementationPlan.objects.get(account=uid)
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
			obj = opportunitiesAndRisks.objects.get(account=uid)
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
                response['message'] = 'miss some parameter'
                response['status'] = 404

        return HttpResponse(json.dumps(response, ensure_ascii = False))

@csrf_exempt
#设置商业计划可见
def shift_visuality(request):
        response = {}				
        if 'uid' in request.POST and 'index' in request.POST and 'choice' in request.POST:
		visibility = visualbility.objects.get(account=int(request.POST['uid']))
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

	else:
		response['status'] = 404
                response['message'] = 'miss some parameter'

        return HttpResponse(json.dumps(response, ensure_ascii = False))
