from twocaptcha import TwoCaptcha
from bestcaptchasolverapi3.bestcaptchasolverapi import BestCaptchaSolverAPI
from anticaptchaofficial.recaptchav3proxyless import *
import deathbycaptcha
import capsolver

from time import sleep
import time

import asyncio
import requests
from pyppeteer import launch
import openpyxl
import json
import websockets

from concurrent.futures import ThreadPoolExecutor
import contextvars
import functools
import nest_asyncio
nest_asyncio.apply()

async def to_thread(func, /, *args, **kwargs):
    loop = asyncio.get_running_loop()
    ctx = contextvars.copy_context()
    func_call = functools.partial(ctx.run, func, *args, **kwargs)
    return await loop.run_in_executor(None, func_call)


width, height = 1920, 1024
excelPath="D:/SocialRobot/captchaTest.xlsx"

api_key = '812bade32688c9eab547f08071bf1810'
username = "popokun"
password = ",X6:bDB}+d*W8s*"
capsolver_key = "CAI-6417405DED7382F181DDC7AD3E35DB67"
ACCESS_TOKEN = 'A4F0406B89C946ECAED764AD6DA96AA3'#bestsolver
anti_key = "aa4b259f16af6857ac897235dcc5245a"

PAGE_URL = 'https://2captcha.com/demo/recaptcha-v3'
SITE_KEY = '6LfB5_IbAAAAAMCtsjEHEHKqcB9iQocwwxTiihJu'

def twocap():
	token = ''

	solver = TwoCaptcha(api_key)
	try:
		result = solver.recaptcha(sitekey=SITE_KEY,url=PAGE_URL,version='v3')
		token = str(result['code'])

	except Exception as e:
		token = str(e)

	return token

def bestsol():
	token = ''

	bcs = BestCaptchaSolverAPI(ACCESS_TOKEN)
	try:
		solution = None
		captcha_id = bcs.submit_recaptcha(
			{'page_url': PAGE_URL, 'site_key': SITE_KEY,'type': 3}
		)
		timer = 0
		while solution == None and timer < 60:  # while it's still in progress
			resp = bcs.retrieve(captcha_id)
			solution = resp['gresponse']
			sleep(5)  # sleep for 10 seconds and recheck
			timer += 1
		token = str(solution)

	except Exception as ex:
		token = str(ex)

	return token

def anticap():
	token = ''
	antisolver = recaptchaV3Proxyless()
	antisolver.set_verbose(1)
	antisolver.set_key(anti_key)
	antisolver.set_website_url(PAGE_URL)
	antisolver.set_website_key(SITE_KEY)
	antisolver.set_page_action("home_page")
	antisolver.set_min_score(0.9)
	antisolver.set_soft_id(0)
	token = antisolver.solve_and_return_solution()
	if token != 0:
		pass
	else:
		token = str(antisolver.error_code)
	return str(token)

def deathcap():
	token = ''

	client = deathbycaptcha.HttpClient(username, password)
	client.is_verbose = False
	Captcha_dict = {
		# 'proxy': 'http://user:password@127.0.0.1:1234',
		# 'proxytype': 'HTTP',
	    'googlekey': SITE_KEY,
	    'pageurl': PAGE_URL,
	    'action': "examples/v3scores",
	    'min_score': 0.3
	}
	json_Captcha = json.dumps(Captcha_dict)
	try:

		# Put your CAPTCHA type and Json payload here:
		captcha = client.decode(type=5, token_params=json_Captcha)
		if captcha:
			token = captcha["text"]

			if '':  # check if the CAPTCHA was incorrectly solved
				client.report(captcha["captcha"])
	except deathbycaptcha.AccessDeniedException:
		# Access to DBC API denied, check your credentials and/or balance
		token = "error: Access to DBC API denied, check your credentials and/or balance"
	return str(token)

def capsol():
	token = ''
	res = ''
	capsolver.api_key = capsolver_key
	try:
		solution = capsolver.solve({
			"type": "ReCaptchaV3TaskProxyLess",
			"websiteURL": PAGE_URL,
			"websiteKey": SITE_KEY,
		})
		token = str(solution["gRecaptchaResponse"])

	except Exception as e:
		token = str(e)

	return token

def save(record,captcha):
	record.append(captcha)
	record.append(time.ctime())
	record.append(PAGE_URL)
	record.append("recaptchaV3")
	wb = openpyxl.load_workbook(excelPath)
	userExcel = wb['recaptchaV3']
	userExcel.append(record)
	wb.save(excelPath)


async def twocaptchaV3(browser,starttime):
	print("测试2captcha")
	page = await browser.newPage()
	await page.setViewport({'width': width, 'height': height})
	await page.goto(PAGE_URL, {'waitUntil' : 'domcontentloaded'})

	record = list()
	record.append(starttime)
	record.append(time.ctime())
	begin = time.time()
	token = await to_thread(twocap)
	t = time.time()-begin
	record.append(time.ctime())
	record.append(t)
	print("2captcha解决结束")
	record.append(str(token))

	print("2captcha判断是否验证成功")
	try:
		record.append("Success")
		js = "verifyRecaptcha(\'" + token + "\')"
		await page.evaluate(js)
		await asyncio.sleep(3)
		
		element = await page.querySelector('#root > div > main > div > section > form > div > pre > code')
		text = await page.evaluate('(element) => element.textContent',element)
		record.append(str(text))

		element = await page.querySelector('#root > div > main > div > section > form > div > pre > code')
		text = await page.evaluate('(element) => element.textContent',element)
		record.append(str(text))
	except:
		record.append("Fail")
		element = await page.querySelector('#root > div > main > div > section > form > aside')
		text = await page.evaluate('(element) => element.textContent',element)
		record.append(str(text))
		record.append("")

	save(record,"2captcha")
	print("2captcha保存结果")
	await page.close()

async def bestsolverV3(browser,starttime):
	print("测试bestsolver")
	page = await browser.newPage()
	await page.setViewport({'width': width, 'height': height})
	await page.goto(PAGE_URL, {'waitUntil' : 'domcontentloaded'})

	record = list()
	record.append(starttime)
	record.append(time.ctime())
	begin = time.time()
	token = await to_thread(bestsol)
	t = time.time()-begin
	record.append(time.ctime())
	record.append(t)
	print("bestsolver解决结束")
	record.append(str(token))

	print("bestsolver判断是否验证成功")
	try:
		js = "verifyRecaptcha(\'" + token + "\')"
		await page.evaluate(js)
		await asyncio.sleep(3)
		
		element = await page.querySelector('#root > div > main > div > section > form > div > pre > code')
		text = await page.evaluate('(element) => element.textContent',element)
		record.append("Success")
		record.append(str(text))

		element = await page.querySelector('#root > div > main > div > section > form > div > pre > code')
		text = await page.evaluate('(element) => element.textContent',element)
		record.append(str(text))
	except:
		record.append("Fail")
		element = await page.querySelector('#root > div > main > div > section > form > aside')
		text = await page.evaluate('(element) => element.textContent',element)
		record.append(str(text))
		record.append("")

	save(record,"bestcaptchasolver")
	print("bestsolver保存结果")
	await page.close()

async def anticapV3(browser,starttime):
	print("测试anticaptcha")
	page = await browser.newPage()
	await page.setViewport({'width': width, 'height': height})
	await page.goto(PAGE_URL, {'waitUntil' : 'domcontentloaded'})

	record = list()
	record.append(starttime)
	record.append(time.ctime())
	begin = time.time()
	token = await to_thread(anticap)
	t = time.time()-begin
	record.append(time.ctime())
	record.append(t)
	print("anticaptcha解决结束")
	record.append(str(token))

	print("anticaptcha判断是否验证成功")
	try:
		js = "verifyRecaptcha(\'" + token + "\')"
		await page.evaluate(js)
		await asyncio.sleep(3)
		
		element = await page.querySelector('#root > div > main > div > section > form > div > pre > code')
		text = await page.evaluate('(element) => element.textContent',element)
		record.append("Success")
		record.append(str(text))

		element = await page.querySelector('#root > div > main > div > section > form > div > pre > code')
		text = await page.evaluate('(element) => element.textContent',element)
		record.append(str(text))
	except:
		record.append("Fail")
		element = await page.querySelector('#root > div > main > div > section > form > aside')
		text = await page.evaluate('(element) => element.textContent',element)
		record.append(str(text))
		record.append("")

	save(record,"anti-captcha")
	print("anticaptcha保存结果")
	await page.close()

async def deathcapV3(browser,starttime):
	print("测试deathcap")
	page = await browser.newPage()
	await page.setViewport({'width': width, 'height': height})
	await page.goto(PAGE_URL, {'waitUntil' : 'domcontentloaded'})

	record = list()
	record.append(starttime)
	record.append(time.ctime())
	begin = time.time()
	token = await to_thread(deathcap)
	t = time.time()-begin
	record.append(time.ctime())
	record.append(t)
	print("deathcap解决结束")
	record.append(str(token))

	print("deathcap判断是否验证成功")
	try:
		js = "verifyRecaptcha(\'" + token + "\')"
		await page.evaluate(js)
		await asyncio.sleep(3)
		
		element = await page.querySelector('#root > div > main > div > section > form > div > pre > code')
		text = await page.evaluate('(element) => element.textContent',element)
		record.append("Success")
		record.append(str(text))

		element = await page.querySelector('#root > div > main > div > section > form > div > pre > code')
		text = await page.evaluate('(element) => element.textContent',element)
		record.append(str(text))
	except:
		record.append("Fail")
		element = await page.querySelector('#root > div > main > div > section > form > aside')
		text = await page.evaluate('(element) => element.textContent',element)
		record.append(str(text))
		record.append("")

	save(record,"deathbycaptcha")
	print("deathcap保存结果")
	await page.close()

async def capsolV3(browser,starttime):
	print("测试capsoler")
	page = await browser.newPage()
	await page.setViewport({'width': width, 'height': height})
	await page.goto(PAGE_URL, {'waitUntil' : 'domcontentloaded'})

	record = list()
	record.append(starttime)
	record.append(time.ctime())
	begin = time.time()
	token = await to_thread(capsol)
	t = time.time()-begin
	record.append(time.ctime())
	record.append(t)
	print("capsolver解决结束")
	record.append(str(token))

	print("capsolver判断是否验证成功")
	try:
		js = "verifyRecaptcha(\'" + token + "\')"
		await page.evaluate(js)
		await asyncio.sleep(3)
		
		element = await page.querySelector('#root > div > main > div > section > form > div > pre > code')
		text = await page.evaluate('(element) => element.textContent',element)
		record.append("Success")
		record.append(str(text))

		element = await page.querySelector('#root > div > main > div > section > form > div > pre > code')
		text = await page.evaluate('(element) => element.textContent',element)
		record.append(str(text))
	except:
		record.append("Fail")
		element = await page.querySelector('#root > div > main > div > section > form > aside')
		text = await page.evaluate('(element) => element.textContent',element)
		record.append(str(text))
		record.append("")

	save(record,"capsolver")
	print("capsolver保存结果")
	await page.close()

async def main():
    # headless = False 为False：有头，True为无头
    # userDataDir 设置当前网站的保存路径，下次登陆时可不用登陆    --disable-infobars禁止策略化

	for i in range(288):
		browser = await launch(headless=False, args=['--disable-web-security','--disable-site-isolation-trials','--allow-running-insecure-content'], userDataDir='C:/Chrome dev session',executablePath='C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')
		starttime =  time.ctime()
		task1 = asyncio.create_task(twocaptchaV3(browser,starttime),name='twocaptchafun_{}'.format(i))
		task2 = asyncio.create_task(bestsolverV3(browser,starttime),name='bestsolverfun_{}'.format(i))
		task3 = asyncio.create_task(anticapV3(browser,starttime),name='anticapfun_{}'.format(i))
		task4 = asyncio.create_task(deathcapV3(browser,starttime),name='deathcapfun_{}'.format(i))
		task5 = asyncio.create_task(capsolV3(browser,starttime),name='capsolfun_{}'.format(i))
		await asyncio.sleep(300)
		await browser.close()


if __name__ == "__main__":
	test = main()
	asyncio.run(test)