#-*- coding: utf-8 -*-
from django.contrib import admin
from up.models import *

# Register your models here.
class BasedInfoAdmin(admin.ModelAdmin):
        list_display = ('id','name','mail','phone','headImg')
        search_fields = ('name','mail','phone')

class DetailInfoAdmin(admin.ModelAdmin):
        list_display = ('id','name','sex','year','province','city','address','school','major','workingCompany','position')
        search_fields = ('name','nickname','province','city','address')

class ConnectInfoAdmin(admin.ModelAdmin):
	list_display = ('id','QQ','phone','mail')
	
class poineeringTagAdmin(admin.ModelAdmin):
	list_display = ('id','stage','fund','name','startDate')

class investmentInfoAdmin(admin.ModelAdmin):
	list_display = ('id','stage','direction1','direction2','company','mail','phase','team','assembly')

class visualbilityAdmin(admin.ModelAdmin):
	list_display = ('id','executiveSum','product','competition','sales','businessModel')

class verify_codeAdmin(admin.ModelAdmin):
        list_display = ('id','mail','verified_code')

class provinceAdmin(admin.ModelAdmin):
	list_display = ('id','name')

class cityAdmin(admin.ModelAdmin):
	list_display = ('id','province','name')
	search_fields = ('province','name')

class schoolAdmin(admin.ModelAdmin):
	list_display = ('id','province','name')
	search_fields = ('province','name')

class executiveSumAdmin(admin.ModelAdmin):
        list_display = ('id','account','idea','targetCustomer','incomeChannel','competitor','investmentCost')

class productAdmin(admin.ModelAdmin):
        list_display = ('id','consumer','profitSupply','advantage','developmentStatus','patent')

class competitionAdmin(admin.ModelAdmin):
        list_display = ('id','tradeCondition','marketSclae','attracttion','competitionProduct','competitveFactor')

class salesAdmin(admin.ModelAdmin):
        list_display = ('id','attractiveWay','pricingFactor','marketingProgram','salesWay')

class businessModelAdmin(admin.ModelAdmin):
        list_display = ('id','coreWork','resource','profitChannel')

class teamManagementAdmin(admin.ModelAdmin):
	list_display = ('id','name')

class memberInfoAdmin(admin.ModelAdmin):
	list_display = ('id','place','position','organiztion','introuduction','startYear','startMonth','endYear','endMonth')

class implementationPlanAdmin(admin.ModelAdmin):
	list_display = ('id','keyStage','workPlan','planRequest')

class finacingAdmin(admin.ModelAdmin):
	list_display = ('id','cashFlow','profitAndLoss','assetAndLiabitilities')

class opportunitiesAndRisksAdmin(admin.ModelAdmin):
	list_display = ('id','opportunities','risks')

class IndustryAdmin(admin.ModelAdmin):
	list_display = ('id','name',)

admin.site.register(BasedInfo, BasedInfoAdmin)
admin.site.register(DetailInfo, DetailInfoAdmin)
admin.site.register(ConnectInfo, ConnectInfoAdmin)
admin.site.register(visualbility, visualbilityAdmin)
admin.site.register(poineeringTag,poineeringTagAdmin)
admin.site.register(investmentInfo,investmentInfoAdmin)
admin.site.register(verify_code, verify_codeAdmin)
admin.site.register(executiveSum, executiveSumAdmin)
admin.site.register(product, productAdmin)
admin.site.register(competition, competitionAdmin)
admin.site.register(sales, salesAdmin)
admin.site.register(businessModel, businessModelAdmin)
admin.site.register(teamManagement, teamManagementAdmin)
admin.site.register(memberInfo, memberInfoAdmin)
admin.site.register(implementationPlan, implementationPlanAdmin)
admin.site.register(finacing, finacingAdmin)
admin.site.register(opportunitiesAndRisks, opportunitiesAndRisksAdmin)
admin.site.register(industry,IndustryAdmin)
admin.site.register(ProvinceList,provinceAdmin)
admin.site.register(CityList,cityAdmin)
admin.site.register(SchoolList,schoolAdmin)
