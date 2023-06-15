import sys
import os
import requests
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import asyncio
import requests
import json
from pyppeteer import launch
from twocaptcha import TwoCaptcha

import openpyxl
import time

from bestcaptchasolverapi3.bestcaptchasolverapi import BestCaptchaSolverAPI
from time import sleep

from anticaptchaofficial.geetestproxyless import *
import deathbycaptcha
import json
import capsolver

import contextvars
import functools
from concurrent.futures import ThreadPoolExecutor
import nest_asyncio
nest_asyncio.apply()

async def to_thread(func, /, *args, **kwargs):
    loop = asyncio.get_running_loop()
    ctx = contextvars.copy_context()
    func_call = functools.partial(ctx.run, func, *args, **kwargs)
    return await loop.run_in_executor(None, func_call)

api_key = '812bade32688c9eab547f08071bf1810'
username = "popokun"
password = ",X6:bDB}+d*W8s*"
capsolver_key = "CAI-6417405DED7382F181DDC7AD3E35DB67"
ACCESS_TOKEN = 'A4F0406B89C946ECAED764AD6DA96AA3'#bestsolver

width, height = 1920, 1024
excelPath="D:\SocialRobot\captchaTest.xlsx"

PAGE_URL = 'https://2captcha.com/demo/geetest-v4'
CAPTCHA_ID='e392e1d7fd421dc63325744d5a2b9c73'

###保存记录###
def save(jilu,t,captcha,excelPath):
	print("保存记录")
	jilu.append(t)
	jilu.append(captcha)
	jilu.append(time.ctime())
	jilu.append(PAGE_URL)
	jilu.append("geetestV4")
	wb = openpyxl.load_workbook(excelPath)
	userExcel = wb['geetestV4']
	userExcel.append(jilu)
	wb.save(excelPath)
	print("完成")

def deathcap():
	token = ''
	res = ''
	client = deathbycaptcha.HttpClient(username, password)
	# Put the proxy and recaptcha_v2 data
	#https://www.google.com/recaptcha/api2/demo
	Captcha_dict = {
		'proxy': 'http://user:password@127.0.0.1:1234',
		'proxytype': 'HTTP',
		'captcha_id': CAPTCHA_ID,
		'pageurl': PAGE_URL}
	# Create a json string
	json_Captcha = json.dumps(Captcha_dict)
	try:
		balance = client.get_balance()
		print(balance)
		# Put your CAPTCHA type and Json payload here:
		captcha = client.decode(type=9, geetest_params=json_Captcha)
		if captcha:
		# The CAPTCHA was solved; captcha["captcha"] item holds its
		# numeric ID, and captcha["text"] item its response.
		# print ("CAPTCHA %s solved: %s" % (captcha["captcha"], captcha["text"]))
		# # To access the response by item
		# print ("captcha_id:", captcha["text"]["captcha_id"])
		# print ("lot_number:", captcha["text"]["lot_number"])
		# print ("pass_token:", captcha["text"]["pass_token"])
		# print ("gen_time:", captcha["text"]["gen_time"])
		# print ("captcha_output:", captcha["text"]["captcha_output"])
			token = captcha["text"]
			res = "chenggong"
		if '':  # check if the CAPTCHA was incorrectly solved
			client.report(captcha["captcha"])
	except deathbycaptcha.AccessDeniedException:
		# Access to DBC API denied, check your credentials and/or balance
		print("error: Access to DBC API denied, check your credentials and/or balance")
		token = "error: Access to DBC API denied, check your credentials and/or balance"
		res = "shibai"
	return token,res

def capsol():
	capsolver.api_key = capsolver_key
	token = ''
	res = ''
	try:
		solution = capsolver.solve({
			"type":"GeeTestTaskProxyLess",
			"websiteURL":PAGE_URL, 
			"captchaId": CAPTCHA_ID, 
			"gt":"",
			"challenge":"",
			"geetestApiServerSubdomain":"api-na.geetest.com",
			   })
		print(solution)
		token = solution
		res = "chenggong"
	except Exception as e:
		print(e)
		token = str(e)
		res = "shibai"
	return token,res

def bestsol():
	bcs = BestCaptchaSolverAPI(ACCESS_TOKEN)        # get access token from: https://bestcaptchasolver.com/account

	solution = None
	d = {'domain': PAGE_URL, 'captchaid': CAPTCHA_ID}
	captcha_id = bcs.submit_geetest_v4(d)

	timer = 0
	while solution == None and timer < 60:    # while it's still in progress
		resp = bcs.retrieve(captcha_id)
		solution = resp['solution']
		sleep(5)               # sleep for 10 seconds and recheck
		timer += 1
	return solution

async def twocaptchageetest(starttime):
	print("测试2captcha")
	jilu = list()
	jilu.append(starttime)
	
	solver = TwoCaptcha(api_key)
	begin = time.time()
	print("2cap:",time.ctime())
	jilu.append(time.ctime())
	try:
		print("测试2captcha")
		# result = solver.geetest_v4(captcha_id='e392e1d7fd421dc63325744d5a2b9c73',
		# 						url='https://2captcha.com/demo/geetest-v4')
		result = await to_thread(solver.geetest_v4,CAPTCHA_ID,PAGE_URL)
	except Exception as e:
		t = time.time()-begin
		jilu.append(time.ctime())
		print(e)
		jilu.append(str(e))
		jilu.append("Fail")
	else:
		t = time.time()-begin
		jilu.append(time.ctime())
		jilu.append(str(result))
		result = json.loads(result['code'])
		print(result)
		headers = {'Content-Type':'application/json; charset=utf-8'}
		data = requests.post('https://2captcha.com/api/v1/captcha-demo/gee-test-v4/verify',headers=headers,data=json.dumps(result))
		print(data)
		# print(json.loads(data.text))
		if str(data) == '''<Response [200]>''':
			print("chengg")
			jilu.append(str(data))
			jilu.append("Success")
		else:
			print("shibai")
			jilu.append(str(data))
			jilu.append("")
			jilu.append("Fail")

	###保存###
	print("保存记录")
	print(jilu)
	save(jilu,t,"2captcha",excelPath)
	await asyncio.sleep(3)

async def bestcaptchasolvergeetest(starttime):
	######bestsolver######
	print("测试bestcaptchasolver")
	jilu = list()
	jilu.append(starttime)
	begin = time.time()
	jilu.append(time.ctime())
	try:
		solution = await to_thread(bestsol)
		jilu.append(time.ctime())
	except Exception as ex:
		t = time.time()-begin
		print(ex)
		jilu.append(str(ex))
		jilu.append("Fail")
	else:
		if solution == None:
			t = time.time()-begin
			jilu.append('Timeout')
			jilu.append('Fail')
		else:
			t = time.time()-begin
			result = solution
			print("bestsolver解决结束")
			print("bestsolver判断是否验证成功")
			jilu.append(str(result))

			headers = {'Content-Type':'application/json; charset=utf-8'}
			data = requests.post('https://2captcha.com/api/v1/captcha-demo/gee-test-v4/verify',headers=headers,data=json.dumps(result))

			if str(data) == '''<Response [200]>''':
				print("chengg")
				jilu.append(str(data))
				jilu.append("Success")
			else:
				print("shibai")
				jilu.append(str(data))
				jilu.append("")
				jilu.append("Fail")
	###保存###
	print(jilu)
	save(jilu,t,"bestsolver",excelPath)
	await asyncio.sleep(3)

async def anticaptchageetest(starttime):
	######anti-captcha######
	print("测试anti-captcha")
	jilu = list()
	jilu.append(starttime)

	antisolver = geetestProxyless()
	antisolver.set_verbose(1)
	antisolver.set_key("aa4b259f16af6857ac897235dcc5245a")
	antisolver.set_website_url(PAGE_URL)
	antisolver.set_gt_key(CAPTCHA_ID)
	antisolver.set_version(4)

	antisolver.set_soft_id(0)
	
	jilu.append(time.ctime())
	begin = time.time()
	token = await to_thread(antisolver.solve_and_return_solution)
	jilu.append(time.ctime())
	if token != 0:
		t = time.time()-begin

		###判断是否验证成功###做记录
		print("anticaptcha判断是否验证成功")
		result = token
		jilu.append(str(result))
		headers = {'Content-Type':'application/json; charset=utf-8'}
		data = requests.post('https://2captcha.com/api/v1/captcha-demo/gee-test-v4/verify',headers=headers,data=json.dumps(result))
		if str(data) == '''<Response [200]>''':

			jilu.append(str(data))
			jilu.append("Success")
		else:

			jilu.append(str(data))
			jilu.append("")
			jilu.append("Fail")

	else:
		t = time.time()-begin

		print(antisolver.error_code)
		jilu.append(str(antisolver.error_code))
		jilu.append("Fail")

	###保存###
	print("anticaptcha判断完成")
	save(jilu,t,"anti-captcha",excelPath)

async def deathbycaptchageetest(starttime):
	######deathcap######
	print("测试deathcap")
	jilu = list()
	jilu.append(starttime)

	jilu.append(time.ctime())
	begin = time.time()
	token,res = await to_thread(deathcap)
	t = time.time()-begin
	jilu.append(time.ctime())

	jilu.append(str(token))
	print("deathbycaptcha解决结束")
	###判断是否验证成功###做记录
	print("deathbycaptcha判断是否验证成功")

	try:
		headers = {'Content-Type':'application/json; charset=utf-8'}
		data = requests.post('https://2captcha.com/api/v1/captcha-demo/gee-test-v4/verify',headers=headers,data=json.dumps(token))
		if str(data) == '''<Response [200]>''':
			jilu.append(str(data))
			jilu.append("Success")

		else:
			jilu.append(str(data))
			jilu.append("")
			jilu.append("Fail")
	except:
		jilu.append("Error")
		jilu.append("")
		jilu.append("Fail")


	###保存
	print("deathbycaptcha判断完成")
	save(jilu,t,"deathcap",excelPath)
	await asyncio.sleep(3)

async def capsolvergeetest(starttime):
	######capsol######
	print("测试capsol")
	jilu = list()
	jilu.append(starttime)

	jilu.append(time.ctime())
	begin = time.time()
	token,res = await to_thread(capsol)
	t = time.time()-begin
	jilu.append(time.ctime())

	jilu.append(str(token))
	print("capsolver解决结束")
	###判断是否验证成功###做记录
	print("capsolver判断是否验证成功")

	try:
		headers = {'Content-Type':'application/json; charset=utf-8'}
		data = requests.post('https://2captcha.com/api/v1/captcha-demo/gee-test-v4/verify',headers=headers,data=json.dumps(token))

		if str(data) == '''<Response [200]>''':
			jilu.append(str(data))
			jilu.append("Success")
		else:
			jilu.append(str(data))
			jilu.append
			jilu.append("Fail")

	except:
		jilu.append("Error")
		jilu.append("")
		jilu.append("Fail")


	###保存
	save(jilu,t,"capsol",excelPath)
	await asyncio.sleep(60)	

async def main():
	# # headless = False 为False：有头，True为无头
	# # userDataDir 设置当前网站的保存路径，下次登陆时可不用登陆    --disable-infobars禁止策略化
	# browser = await launch(headless=False, devtools=True, args=['--disable-web-security','--disable-site-isolation-trials','--allow-running-insecure-content'], userDataDir='C:/Chrome dev session',executablePath='C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')
	# # 申明一个page对象
	# page = await browser.newPage()
	# # 浏览器设置宽高
	# await page.setViewport({'width': width, 'height': height})
	# # 要访问的网址
	# await page.goto('https://2captcha.com/demo/geetest-v4',{'waitUntil' : 'domcontentloaded'})
	# await asyncio.sleep(5)
	# jilu = list()
	for i in range(288):
		starttime =  time.ctime()
		# task1 = asyncio.create_task(twocaptchageetest(starttime))
		# task2 = asyncio.create_task(bestcaptchasolvergeetest(starttime))
		# task3 = asyncio.create_task(anticaptchageetest(starttime))
		task4 = asyncio.create_task(deathbycaptchageetest(starttime))
		# task5 = asyncio.create_task(capsolvergeetest(starttime))
		await asyncio.sleep(300)



if __name__ == "__main__":
	test = main()
	asyncio.run(test)