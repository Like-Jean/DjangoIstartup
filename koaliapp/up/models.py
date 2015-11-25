#-*- coding: utf-8 -*-
from django.db import models

# Create your models here.

#省份列表
class ProvinceList(models.Model):
	name = models.CharField('名称',max_length=30)

	def __unicode__(self):
                return str(self.id) + self.name
        class Meta:
            verbose_name = "省份列表"
            verbose_name_plural = "省份列表"

#城市列表
class CityList(models.Model):
	province = models.ForeignKey(ProvinceList,verbose_name='省份')
	name = models.CharField('名称',max_length=20)

	def __unicode__(self):
                return str(self.id) + self.name
        class Meta:
            verbose_name = "城市列表"
            verbose_name_plural = "城市列表"

#学校列表
class SchoolList(models.Model):
	province = models.ForeignKey(ProvinceList,verbose_name='省份')
	name = models.CharField('名称',max_length=60)

        def __unicode__(self):
                return str(self.id) + self.name

        class Meta:
            verbose_name = "学校列表"
            verbose_name_plural = "学校列表"

#专业分类
class majorClassfied(models.Model):
	name = models.CharField('专业分类',max_length = 20)
	
	def __unicode__(self):
                return str(self.id) + self.name

        class Meta:
            verbose_name = "专业分类"
            verbose_name_plural = "专业分类"

#专业列表
class majorList(models.Model):
	models.ForeignKey(majorClassfied,verbose_name='省份')
	name = models.CharField('专业名称',max_length = 30)

	def __unicode__(self):
                return str(self.id) + self.name

        class Meta:
            verbose_name = "专业列表"
            verbose_name_plural = "专业列表"

#用户注册的基本信息
class BasedInfo(models.Model):
        mail = models.CharField('邮箱',max_length = 30,blank = True,null = True)
        name = models.CharField('名称',max_length = 10)
        phone = models.CharField('手机',max_length = 30,blank = True,null = True)
        password = models.CharField('密码',max_length = 16)
	headImg = models.FileField(verbose_name='头像',upload_to = './upload/',null = True)
	is_verified = models.BooleanField(verbose_name='是否通过验证',default = False)
        is_logined = models.BooleanField(verbose_name='是否登录',default = False)
	form = models.CharField('类型',max_length = 10)

        def __unicode__(self):
		return str(self.id)
        class Meta:
            verbose_name = "用户基本信息"
            verbose_name_plural = "用户基本信息"

#用户的详细信息
class DetailInfo(models.Model):
        account = models.ForeignKey(BasedInfo,verbose_name='帐号')
        name = models.CharField('名称',max_length = 10)
        sex = models.CharField('性别',max_length=4,blank = True,null = True)
        year = models.CharField(verbose_name='年份',max_length=5,blank = True,null = True)
        nationality = models.CharField('国家',max_length = 20,blank = True,null = True)
        province =  models.CharField('省份',max_length = 20,blank = True,null = True)
        city = models.CharField('城市',max_length = 10,blank = True,null = True)
        address = models.CharField('具体地址',max_length = 50,blank = True,null = True)
        school = models.CharField('本科就读学校1',max_length = 30,blank = True,null = True)
        major = models.CharField('专业1',max_length = 30,blank = True,null = True)
	workingCompany = models.CharField('曾就业公司',max_length = 30,blank = True,null = True)
	position = models.CharField('曾就业职位',max_length = 30,blank = True,null = True)
	form = models.CharField('类型',max_length = 10)
	
        def __unicode__(self):
		return str(self.id) + self.name
        class Meta:
            verbose_name = "用户详细信息"
            verbose_name_plural = "用户详细信息"

#用户联系方式
class ConnectInfo(models.Model):
	account = models.ForeignKey(BasedInfo,verbose_name='帐号')
	QQ = models.CharField('qq',max_length = 12)
	phone = models.CharField('手机',max_length = 11)
	mail = models.EmailField('邮箱')

	def __unicode__(self):
                return str(self.id)
        class Meta:
            verbose_name = "用户联系方式"
            verbose_name_plural = "用户联系方式"

#储存注册用的验证码
class verify_code(models.Model):
        mail = models.CharField('邮箱',max_length = 30,blank = True,null = True)
        verified_code = models.IntegerField(blank = True,null = True)

        def __unicode__(self):
		return str(self.id) + self.mail
#投资信息
class investmentInfo(models.Model):
	account = models.ForeignKey(BasedInfo,verbose_name='账号')
	company = models.TextField(verbose_name='公司名称',blank = True,null = True)
	summary = models.TextField(verbose_name='公司简介',blank = True,null = True)
	stage = models.CharField(verbose_name='投资类型',max_length = 20,blank = True,null = True)
	mail =  models.EmailField('邮箱')
	direction1 = models.CharField(verbose_name='投资领域1',max_length = 10,blank = True,null = True)
	direction2 = models.CharField(verbose_name='投资领域2',max_length = 10,blank = True,null = True)
	assembly = models.TextField(verbose_name='投资组合',blank = True,null = True)
	team = models.TextField(verbose_name='投资团队',blank = True,null = True)
	phase = models.CharField(verbose_name='投资阶段',max_length = 10,blank = True,null = True)

        def __unicode__(self):
                return str(self.id)
        class Meta:
            verbose_name = "投资信息"
            verbose_name_plural = "投资信息"
	
#创业标签
class poineeringTag(models.Model):
       account = models.ForeignKey(BasedInfo,verbose_name='帐号')
       name = models.CharField('项目名称',max_length = 30)
       stage = models.CharField('项目阶段',max_length = 12)
       fund = models.CharField('所需资金',max_length = 13)
       summary = models.CharField('一句话简介',max_length = 200,blank = True,null = True)
       direction1 = models.CharField('方向一',max_length = 20,blank = True,null = True)
       direction2 = models.CharField('方向二',max_length = 20,blank = True,null = True)
       startDate = models.DateField(auto_now_add=True,verbose_name='日期')
       last_modified = models.DateField(auto_now=True,verbose_name='最后修改')
       integrity = models.CharField('完整度',max_length = 4,blank = True,null = True)

       def __unicode__(self):
               return str(self.id) + self.name
       class Meta:
           verbose_name = "创业标签"
           verbose_name_plural = "创业标签"
       
#简略概要
class executiveSum(models.Model):
       account = models.ForeignKey(BasedInfo,verbose_name='帐号')
       tag = models.ForeignKey(poineeringTag,verbose_name='项目标签')
       idea = models.CharField('思路创意',max_length = 400,blank = True,null = True)
       targetCustomer = models.CharField('目标客户',max_length = 400,blank = True,null = True)
       incomeChannel = models.CharField('收入渠道',max_length = 400,blank = True,null = True)
       competitor = models.CharField('竞争对手',max_length = 400,blank = True,null = True)
       investmentCost = models.CharField('投资成本',max_length = 400,blank = True,null = True)
       
       def __unicode__(self):
	       return str(self.id)
       class Meta:
           verbose_name = "简略概要"
           verbose_name_plural = "简略概要"  

#产品/服务
class product(models.Model):
       account = models.ForeignKey(BasedInfo,verbose_name='帐号')
       tag = models.ForeignKey(poineeringTag,verbose_name='项目标签')
       consumer = models.CharField('消费人群',max_length = 400,blank = True,null = True)
       profitSupply = models.CharField('提供价值',max_length = 400,blank = True,null = True)
       advantage = models.CharField('产品优势',max_length = 400,blank = True,null = True)
       developmentStatus = models.CharField('开发阶段',max_length = 400,blank = True,null = True)
       patent = models.CharField('专利情况',max_length = 400,blank = True,null = True)
       
       def __unicode__(self):
	       return str(self.id)
       class Meta:
           verbose_name = "产品/服务"
           verbose_name_plural = "产品/服务"

#市场竞争
class competition(models.Model):
       account = models.ForeignKey(BasedInfo,verbose_name='帐号')
       tag = models.ForeignKey(poineeringTag,verbose_name='项目标签')
       tradeCondition = models.CharField('行业情况',max_length = 400,blank = True,null = True)
       marketSclae = models.CharField('市场规模',max_length = 400,blank = True,null = True)
       attracttion = models.CharField('产品吸引力',max_length = 400,blank = True,null = True)
       competitionProduct = models.CharField('竞争产品',max_length = 400,blank = True,null = True)
       competitveFactor = models.CharField('竞争优势',max_length = 400,blank = True,null = True)
       
       def __unicode__(self):
	       return str(self.id)
       class Meta:
           verbose_name = "市场竞争"
           verbose_name_plural = "市场竞争"

#销售
class sales(models.Model):
       account = models.ForeignKey(BasedInfo,verbose_name='帐号')
       tag = models.ForeignKey(poineeringTag,verbose_name='项目标签')
       attractiveWay = models.CharField('吸引用户',max_length = 400,blank = True,null = True)
       pricingFactor = models.CharField('定价因素',max_length = 400,blank = True,null = True)
       marketingProgram = models.CharField('营销方案',max_length = 400,blank = True,null = True)
       salesWay = models.CharField('营销渠道',max_length = 400,blank = True,null = True)
       
       def __unicode__(self):
	       return str(self.id)
       class Meta:
           verbose_name = "销售"
           verbose_name_plural = "销售"

#商业模式
class businessModel(models.Model):
       account = models.ForeignKey(BasedInfo,verbose_name='帐号')
       tag = models.ForeignKey(poineeringTag,verbose_name='项目标签')
       coreWork = models.CharField('核心工作',max_length = 400,blank = True,null = True)
       resource = models.CharField('需要资源',max_length = 400,blank = True,null = True)
       profitChannel = models.CharField('盈利渠道',max_length = 500,blank = True,null = True)
       
       def __unicode__(self):
	       return str(self.id)
       class Meta:
           verbose_name = "商业模式"
           verbose_name_plural = "商业模式"

#团队管理
class teamManagement(models.Model):
	account = models.ForeignKey(BasedInfo,verbose_name='账号')
	tag = models.ForeignKey(poineeringTag,verbose_name='项目标签')
	name = models.CharField('姓名',max_length=50)
	
	def __unicode__(self):
               return str(self.id)+self.name
        class Meta:
           verbose_name = "管理团队"
           verbose_name_plural = "管理团队"

#团队成员资料
class memberInfo(models.Model):
	member = models.ForeignKey(teamManagement,verbose_name='所属成员')
	place = models.CharField('地点',max_length = 14,blank = True,null = True)
	organiztion = models.CharField('单位',max_length = 30,blank = True,null = True)
	position = models.CharField('职位',max_length = 20,blank = True,null = True)
	introuduction = models.TextField(verbose_name='简介')
	startYear = models.CharField('开始年份',max_length=4)
	startMonth = models.CharField('开始月份',max_length=2)
	endYear = models.CharField('结束年份',max_length=4)
	endMonth = models.CharField('结束月份',max_length=2)

	def __unicode__(self):
               return str(self.id)
        class Meta:
           verbose_name = "团队成员资料"
           verbose_name_plural = "团队成员资料"

#执行方案
class implementationPlan(models.Model):
	account = models.ForeignKey(BasedInfo,verbose_name='账号')
        tag = models.ForeignKey(poineeringTag,verbose_name='项目标签')
	keyStage = models.TextField('重要阶段')
	workPlan = models.TextField('工作计划')
	planRequest = models.TextField('计划需求')

	def __unicode__(self):
               return str(self.id)
        class Meta:
           verbose_name = "执行方案"
           verbose_name_plural = "执行方案"

#财务融资
class finacing(models.Model):
	account = models.ForeignKey(BasedInfo,verbose_name='帐号')
	tag = models.ForeignKey(poineeringTag,verbose_name='项目标签')
	cashFlow = models.FileField(verbose_name='现金流量表',upload_to = './table/',null = True,blank=True)
	profitAndLoss = models.FileField(verbose_name='损益表',upload_to = './table/',null = True,blank=True)
	assetAndLiabitilities = models.FileField(verbose_name='资产负债表',upload_to = './table/',null = True,blank=True)
	
	def __unicode__(self):
               return str(self.id)
        class Meta:

           verbose_name = "财务融资"
           verbose_name_plural = "财务融资"

#机会风险
class opportunitiesAndRisks(models.Model):
	account = models.ForeignKey(BasedInfo,verbose_name='帐号')
        tag = models.ForeignKey(poineeringTag,verbose_name='项目标签')
        opportunities = models.TextField(verbose_name='发展机会',blank = True,null = True)
        risks = models.TextField(verbose_name='风险',blank = True,null = True)

        def __unicode__(self):
               return str(self.id)
        class Meta:
           verbose_name = "机会风险"
           verbose_name_plural = "机会风险"

#可见性设置
class visualbility(models.Model):
	account = models.ForeignKey(BasedInfo,verbose_name='帐号')
	executiveSum = models.BooleanField(default=True)
	product = models.BooleanField(default=True)
	competition = models.BooleanField(default=True)
	sales = models.BooleanField(default=True)
	businessModel = models.BooleanField(default=True)
	teamManagement = models.BooleanField(default=True)
	implementationPlan = models.BooleanField(default=True)
	finacing = models.BooleanField(default=True)
	opportunitiesAndRisks = models.BooleanField(default=True)

	def __unicode__(self):
               return str(self.id)
        class Meta:
           verbose_name = "可见性"
           verbose_name_plural = "可见性"
	
#行业分类
class industry(models.Model):
	name = models.CharField('行业名称',max_length=20)
        item = models.ManyToManyField(poineeringTag,verbose_name='行业项目',blank = True,null = True)
	
	def __unicode__(self):
	       return str(self.id)
        class Meta:
           verbose_name = "行业分类"
           verbose_name_plural = "行业分类"


