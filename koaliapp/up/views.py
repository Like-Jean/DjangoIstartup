#-*- coding: utf-8 -*-
#ip:192.168.31.163
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django import forms
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.cache import SessionStore
from django.template import Context

from up.models import *
from random import randint
import httplib
import urllib
import json
import re
import smtplib  
import sys

reload(sys)

sys.setdefaultencoding('utf8')

mail_host="smtp.koalitech.com"  #设置服务器
mail_user="verify@koalitech.com"    #用户名
mail_pass="QQwwee11"   #口令 
mail_postfix="koalitech.com"  #发件箱的后缀



def send_mail(sub,toList,content):
        me="系统验证<"+mail_user+"@"+mail_postfix+">"  
        msg = MIMEMultipart('related')  
        msg['Subject'] = sub  
        msg['From'] = me  
        msg['To'] = toList
	msg.attach(content)
        try:  
            server = smtplib.SMTP()  
            server.connect(mail_host)  
            server.login(mail_user,mail_pass)
            server.sendmail(me, toList, msg.as_string())  
            server.close()  
            return True  
        except Exception, e:  
            print str(e)  
            return False  

mail_feedback="feedback@koalitech.com"    #用户名
mail_feedbackPass="Qqwwee11"   #口令 
object_mail = "postmaster@koalitech.com"  #反馈由反馈邮箱发到管理员邮箱

def feedback_mail(sub,toList,content):
        me="用户反馈<"+mail_feedback+"@"+mail_postfix+">"
        msg = MIMEMultipart('related')
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = toList
        msg.attach(content)
        try:
            server = smtplib.SMTP()
            server.connect(mail_host)
            server.login(mail_feedback,mail_feedbackPass)
            server.sendmail(me, toList, msg.as_string())
            server.close()
            return True
        except Exception, e:
            print str(e)
            return False

host = "yunpian.com"#服务地址
port = 80#端口号
version = "v1"#版本号
sms_send_uri = "/" + version + "/sms/send.json"#通用短信接口的URI

def send_message(text, mobile):
	apikey='ed30d52c7e2adddd40bc42359551f05b'
	params = urllib.urlencode({'apikey': apikey, 'text': text, 'mobile':mobile})

	headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn = httplib.HTTPConnection(host, port=port, timeout=30)
        conn.request("POST", sms_send_uri, params, headers)
	
	response = conn.getresponse()
	response_str = response.read()
        conn.close()

	return response_str
	
# Create your views here.

#检测邮箱或手机是否已存在
def check(request):
        response={}
        if 'phone' in request.GET:
                check_phone = request.GET['phone']
                try:
                    user = BasedInfo.objects.get(phone=check_phone)
                    if user:
                            response['message'] = 'existed'
                            response['status'] = 0
                            response['data'] = None
                except ObjectDoesNotExist:
                    response['message'] = 'available'
                    response['status'] = 0
                    response['data'] = None
        elif 'mail' in request.GET:
                check_mail = request.GET['mail']
                try:
                    user = BasedInfo.objects.get(mail=check_mail)
                    if user:
                            response['message'] = 'existed'
                            response['status'] = 0
                            response['data'] = None
                except ObjectDoesNotExist:
                    response['message'] = 'available'
                    response['status'] = 0
                    response['data'] = None
        else:
		response['message'] = 'miss some parameter'
                response['status'] = 404
                response['data'] = None
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

			return HttpResponse(json.dumps(response, ensure_ascii = False))
	else:
		response['message'] = 'failed'
                response['status'] = 404

	return HttpResponse(json.dumps(response, ensure_ascii = False)) 
		
 
#注册
@csrf_exempt
def register(request):
        response = {}
        if 'phone' in request.POST and 'name' in request.POST and 'password' in request.POST and 'form' in request.POST:
		try:
		    user = BasedInfo.objects.get(phone=request.POST['phone'])
                    if user:
		   	    response['message'] = 'existed'
                            response['status'] = 0
                            response['data'] = None

			    return HttpResponse(json.dumps(response, ensure_ascii = False))
		except ObjectDoesNotExist:
                    user = BasedInfo(name=request.POST['name'],phone=request.POST['phone'],password=request.POST['password'],form=request.POST['form'],is_verified=True)
		    user.save()
		    if request.POST['form'] == '创业者':
		    	    user.headImg = '/site_media/upload/chuangyezhe_02.jpg'
			    project = poineeringTag(account_id=user.id)
                    	    project.save()

			    visibility = visualbility(account_id=user.id)
                            visibility.save()
 
 	                    pid = project.id
 	
        	            user_executive = executiveSum(account_id=user.id,tag_id=pid)
	                    user_executive.save()
 
                            user_product = product(account_id=user.id,tag_id=pid)
                            user_product.save()
 
                            user_competition = competition(account_id=user.id,tag_id=pid)
                            user_competition.save()
 
                            user_sales = sales(account_id=user.id,tag_id=pid)
                            user_sales.save()
 
                            user_business = businessModel(account_id=user.id,tag_id=pid)
                            user_business.save()
 
                            user_team = teamManagement(account_id=user.id,tag_id=pid)
                            user_team.save()
 
                            user_implementation = implementationPlan(account_id=user.id,tag_id=pid)
                            user_implementation.save()
 
                            user_finacing = finacing(account_id=user.id,tag_id=pid)
                            user_finacing.save()
 
                            user_opportunities = opportunitiesAndRisks(account_id=user.id,tag_id=pid)
                            user_opportunities.save()

		    else:
			    user.headImg = '/site_media/upload/touzizhe_02.jpg'
			    project = investmentInfo(account_id=user.id)
                            project.save()
                    user.save()
                
		    user_info = DetailInfo(account_id=user.id,name=user.name)
		    user_info.form = request.POST['form']
                    if 'sex' in request.POST:
                            user_info.sex = request.POST['sex']
                    if 'birthday' in request.POST:
                            user_info.birthday = request.POST['birthday']
                    if 'nationality' in request.POST:
                            user_info.nationality = request.POST['nationality']
                    if 'province' in request.POST:
                            user_info.province = request.POST['province']
                    if 'city' in request.POST:
                            user_info.city = request.POST['city']                
                    if 'school' in request.POST:
                            user_info.school = request.POST['school']
                    if 'major' in request.POST:
                            user_info.major = request.POST['major']
                
                    if 'company' in request.POST:
                            user_info.workingCompany = request.POST['company']
                    if 'position' in request.POST:
                            user_info.position = request.POST['position']
		    user_info.save()
                #初始化用户个人资料

		#初始化联系方式
		    connect = ConnectInfo(account_id=user.id,phone=request.POST['phone'])
		    connect.save()

                    response['message'] = 'success'
                    response['status'] = 0
                    response['data'] = user.id

        elif 'mail' in request.POST and 'name' in request.POST and 'password' in request.POST and 'form' in request.POST:
		try:
                    user = BasedInfo.objects.get(mail=request.POST['mail'])
                    if user:
                            response['message'] = 'existed'
                            response['status'] = 0
                            response['data'] = None

                            return HttpResponse(json.dumps(response, ensure_ascii = False))
		except ObjectDoesNotExist:
                    user = BasedInfo(name=request.POST['name'],mail=request.POST['mail'],password=request.POST['password'],form=request.POST['form'])
		    user.save()
		    if request.POST['form'] == '创业者':
                            user.headImg = '/site_media/upload/chuangyezhe_02.jpg'
			    project = poineeringTag(account_id=user.id)
                            project.save()

                            visibility = visualbility(account_id=user.id)
                            visibility.save()

                            pid = project.id

                            user_executive = executiveSum(account_id=user.id,tag_id=pid)
                            user_executive.save()

                            user_product = product(account_id=user.id,tag_id=pid)
                            user_product.save()

                            user_competition = competition(account_id=user.id,tag_id=pid)
                            user_competition.save()

                            user_sales = sales(account_id=user.id,tag_id=pid)
                            user_sales.save()

                            user_business = businessModel(account_id=user.id,tag_id=pid)
                            user_business.save()

                            user_team = teamManagement(account_id=user.id,tag_id=pid)
                            user_team.save()

                            user_implementation = implementationPlan(account_id=user.id,tag_id=pid)
                            user_implementation.save()

                            user_finacing = finacing(account_id=user.id,tag_id=pid)
                            user_finacing.save()

                            user_opportunities = opportunitiesAndRisks(account_id=user.id,tag_id=pid)
                            user_opportunities.save()
                    else:
			    user.headImg = '/site_media/upload/touzizhe_02.jpg'
			    project = investmentInfo(account_id=user.id)
			    project.mail = request.POST['mail']
                            project.save()
		    user.is_verified = True
                    user.save()
                
                    user_info = DetailInfo(account_id=user.id,name=user.name)
		    user_info.form = request.POST['form']
                    #if 'sex' in request.POST:
                     #       user_info.sex = request.POST['sex']
                    if 'year' in request.POST:
                            user_info.year = request.POST['year']
                    if 'nationality' in request.POST:
                            user_info.nationality = request.POST['nationality']
                    if 'province' in request.POST:
                            user_info.province = request.POST['province']
                    if 'city' in request.POST:
                            user_info.city = request.POST['city']
		    if 'school' in request.POST:
                            user_info.school = request.POST['school']
                    if 'major' in request.POST:
                            user_info.major = request.POST['major']

                    if 'company' in request.POST:
                            user_info.workingCompany = request.POST['company']
                    if 'position' in request.POST:
                            user_info.position = request.POST['position']
                    user_info.save()
                #初始化用户个人资料

		    user_connect = ConnectInfo(account_id=user.id)
                    user_connect.mail = request.POST['mail']
                    user_connect.save()

		    Content = MIMEText('<html><body><h2>感谢您的注册，<a href="http://120.25.206.58/activate/?mail=%s" target="_blank">请点击该链接</a>完成激活。</h2></body></html>' %(user_connect),'html','utf-8')
                    Sub = "【夸励科技】请激活您的istartup账号"
                    if send_mail(Sub,request.POST['mail'],Content):
	   	    	    pass
                    else:
                            response['message'] = 'send failed'
                            response['status'] = 401
			    return HttpResponse(json.dumps(response, ensure_ascii = False))


                    response['message'] = 'success'
                    response['status'] = 0
                    response['data'] = user.id

        else:
                response['message'] = 'failed'
                response['status'] = 404
                response['data'] = None
        
        return HttpResponse(json.dumps(response, ensure_ascii = False))

@csrf_exempt
#邮箱发送验证码
def verify_mail(request):
        response={}
        if 'mail' in request.GET:
		Content = MIMEText('<html><body><h2>感谢您的注册，<a href="http://120.25.206.58/activate/?mail=%s" target="_blank">请点击该链接</a>完成激活。</h2></body></html>'%(request.GET['mail']),'html','utf-8')
		Sub = "【夸励科技】请激活您的istartup账号"
                if send_mail(Sub,request.GET['mail'],Content):
                      response['message'] = 'send successfully'
                      response['status'] = 0

                else:
                      response['message'] = 'send failed'
                      response['status'] = 401 

        else:
                response['message'] = 'miss some parameter'
                response['status'] = 404

        return HttpResponse(json.dumps(response, ensure_ascii = False))

#邮件激活
def activate(request):
	response={}
	if 'mail' in request.GET:
		user = BasedInfo.objects.get(mail=request.GET['mail'])
		user.is_verified = True
		user.save()
		
		response['message'] = 'ok'
		response['status'] = 0
	else:
		response['message'] = 'failed'
                response['status'] = 404

        return HttpResponse(json.dumps(response, ensure_ascii = False))

@csrf_exempt
#短信发送验证码
def verify_phone(request):
        response={}
        if 'phone' in request.POST:
		phone = request.POST['phone']
		try:
                    ver = verify_code.objects.get(mail=request.POST['phone'])
                except ObjectDoesNotExist:
                    ver = verify_code(mail=request.POST['phone'])
                Rannum = randint(1000,9999)
                ver.verified_code = Rannum
                ver.save()
                Content = "【夸励科技】感谢您注册istartup，您的验证码是%s"%(Rannum)
		result= json.loads(send_message(Content,phone))
		if result["code"]==0 and result["msg"]=="OK":
			response['message'] = 'send successfully'
                	response['status'] = 0
                else:
			response['message'] = 'failed'
                	response['status'] = 401
        else:
                response['message'] = 'miss some parameter'
                response['status'] = 404

        return HttpResponse(json.dumps(response, ensure_ascii = False))

@csrf_exempt
#提交验证码
def summit_verifying_code(request):
        response={}
        if 'phone' in request.POST and 'vcode' in request.POST:
                ver = verify_code.objects.get(mail=request.POST['phone'])
                ver_code = int(request.POST['vcode'])
                if ver_code == ver.verified_code:
			ver.delete()
                        response['message'] = 'verify successfully'
                        response['status'] = 0
                else:
                        response['message'] = 'verify failed'
                        response['status'] = 401
        else:
             response['message'] = 'miss some parameter'
             response['status'] = 404

        return HttpResponse(json.dumps(response, ensure_ascii = False))
	
@csrf_exempt
#短信发送找回密码验证码
def find_phone(request):
        response={}
        if 'phone' in request.POST:
                phone = request.POST['phone']
                try:
                    ver = verify_code.objects.get(mail=request.POST['phone'])
                except ObjectDoesNotExist:
                    ver = verify_code(mail=request.POST['phone'])
                Rannum = randint(1000,9999)
                ver.verified_code = Rannum
                ver.save()
                Content = "【夸励科技】正在找回密码，您的验证码是%s"%(Rannum)
                result= json.loads(send_message(Content,phone))
                if result["code"]==0 and result["msg"]=="OK":
                        response['message'] = 'send successfully'
                        response['status'] = 0
                else:
                        response['message'] = 'failed'
                        response['status'] = 401
        else:
                response['message'] = 'miss some parameter'
                response['status'] = 404

        return HttpResponse(json.dumps(response, ensure_ascii = False))
@csrf_exempt
#找回密码
def find_password(request):
	response={}
        if 'phone' in request.POST and 'password' in request.POST:
		user = BasedInfo.objects.get(phone=request.POST['phone'])
                user.password = request.POST['password']
		user.save()
                response['message'] = 'find successfully'
                response['status'] = 0
        elif 'mail' in request.POST and 'password' in request.POST:
		user = BasedInfo.objects.get(mail=request.POST['mail'])
                user.password = request.POST['password']
                user.save()
                response['message'] = 'find successfully'
                response['status'] = 0
	else:
             response['message'] = 'miss some parameter'
             response['status'] = 404

        return HttpResponse(json.dumps(response, ensure_ascii = False))

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

				    result = {}
				    result['id'] = user.id
				    result['form'] = user.form
                                    response['message'] = 'login successfully'
                                    response['status'] = 0
                                    response['data'] = result
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

				    result ={}
				    result['id'] = user.id
                                    result['form'] = user.form
                                   
                                    response['status'] = 0
                                    response['data'] = result
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

#发送反馈
def feedback(request):
	response={}
	if 'content' in request.GET and 'uid' in request.GET:
		user_name = BasedInfo.objects.get(id=request.GET['uid']).name
		connect_info = ConnectInfo.objects.get(account_id=request.GET['uid'])
		Sub = "istartup意见反馈:"+user_name
		Content = MIMEText(request.GET['content']+"e-mail:"+connect_info.mail+"phone:"+connect_info.phone+"QQ:"+connect_info.QQ,_subtype='plain',_charset='utf-8')
                if feedback_mail(Sub,object_mail,Content):
                      response['message'] = 'send successfully'
                      response['status'] = 0

                else:
                      response['message'] = 'send failed'
                      response['status'] = 401

        else:
                response['message'] = 'miss some parameter'
                response['status'] = 404

        return HttpResponse(json.dumps(response, ensure_ascii = False))

