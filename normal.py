import os
import sys
sys.path.append(os.path.abspath(os.path.join(__file__, os.pardir, os.pardir)))
from time import sleep
import asyncio
import requests
from pyppeteer import launch
import openpyxl
import base64

from twocaptcha import TwoCaptcha#2captcha
from bestcaptchasolverapi3.bestcaptchasolverapi import BestCaptchaSolverAPI#bestsolver
from time import sleep
from anticaptchaofficial.imagecaptcha import *#anti-captcha
import deathbycaptcha#deathbycaptcha
import capsolver#capsolver

TWO_API_KEY = '812bade32688c9eab547f08071bf1810'#2captcha
ACCESS_TOKEN = 'A4F0406B89C946ECAED764AD6DA96AA3'#bestsolver
ANTI_KEY = 'aa4b259f16af6857ac897235dcc5245a'#anti-captcha
username = "popokun"#deathbycaptcha
password = ",X6:bDB}+d*W8s*"
CAPSOLVER_KEY = 'CAI-6417405DED7382F181DDC7AD3E35DB67'#capsolver

width, height = 1920, 1024
excelPath="D:/SocialRobot/captchaTest.xlsx"
PAGE_URL = "https://www.mtcaptcha.com/"

imgFolderpath = 'D:/SocialRobot/Twitter/2captcha/code/img/imgtotext/'  #保存图片文件夹
# imgFolderpath = r"D:\SocialRobot\Twitter\2captcha\code\img\imgtotext"

#######2captcha######
async def twocap(imgpath):
	print("2captcha")
	api_key = os.getenv('APIKEY_2CAPTCHA', TWO_API_KEY)
	solver = TwoCaptcha(api_key)
	token = ''
	res = ''
	try:
		result = solver.normal(imgpath)
	except Exception as e:
		print(e)
		token = str(e)
		res = "shibai"
	else:
		print('result: ' + str(result))
		token = str(result['code'])
		res = "chenggong"
	return token,res

######bestdolver######
async def bestsol(imgpath):
	token = ''
	res = ''
	try:
		bcs = BestCaptchaSolverAPI(ACCESS_TOKEN)        # get access token from: https://bestcaptchasolver.com/account
		# check account balance
		# ---------------------------
		balance = bcs.account_balance()                       # get account balance
		print ('Balance: {}'.format(balance))                 # print balance
		print ('Solving image captcha ...')
		data = {}
		data['image'] = imgpath
	    # optional parameters
	    # -------------------
	    # data['is_case'] = True, default: False
	    # data['is_phrase'] = True, default: False
	    # data['is_math'] = True, default: False
	    # data['alphanumeric'] = 1 (digits only) or 2 (letters only), default: all characters
	    # data['minlength'] = minimum length of captcha text, default: any
	    # data['maxlength'] = maximum length of captcha text, default: any
	    # data['affiliate_id'] = 'affiliate_id from /account'

		id = bcs.submit_image_captcha(data)  # submit image captcha (case_sensitive param optional)
		image_text = None
		# None is returned if completion is still in pending
		while image_text == None:
			image_text = bcs.retrieve(id)['text']  # get the image text using the ID
			sleep(5)
		print ('Captcha text: {}'.format(image_text))
		token = str(image_text)
		res = "chenggong"
	except Exception as ex:
		print ('[!] Error occured: {}'.format(ex))
		token = str(ex)
		res = "shibai"
	return token,res

######anti-captcha######
async def anticap(imgpath):
	token = ''
	res = ''
	solver = imagecaptcha()
	solver.set_verbose(1)
	solver.set_key(ANTI_KEY)

	# Specify softId to earn 10% commission with your app.
	# Get your softId here: https://anti-captcha.com/clients/tools/devcenter
	solver.set_soft_id(0)

	captcha_text = solver.solve_and_return_solution(imgpath)
	if captcha_text != 0:
	    print ("captcha text "+captcha_text)
	    token = str(captcha_text)
	    res = "chenggong"
	else:
	    print ("task finished with error "+solver.error_code)
	    token = str(solver.error_code)
	    res = "shibai"
	return token,res

######deathcaptcha######
async def deathcap(imgpath):
	token = ''
	res = ''
	client = deathbycaptcha.HttpClient(username, password)
	captcha_file = imgpath  # image
	try:
	    balance = client.get_balance()
	    print(balance)

	    # Put your CAPTCHA file name or file-like object, and optional
	    # solving timeout (in seconds) here:
	    captcha = client.decode(captcha_file)
	    if captcha:
	        # The CAPTCHA was solved; captcha["captcha"] item holds its
	        # numeric ID, and captcha["text"] item its the response.
	        print("CAPTCHA %s solved: %s" % (captcha["captcha"], captcha["text"]))
	        if '':  # check if the CAPTCHA was incorrectly solved
	            client.report(captcha["captcha"])
	        token = str(captcha["text"])
	        res = "chenggong"
	except deathbycaptcha.AccessDeniedException:
	    # Access to DBC API denied, check your credentials and/or balance
	    print("error: Access to DBC API denied, check your credentials and/or balance")
	    token = "error: Access to DBC API denied, check your credentials and/or balance"
	    res = "shibai"
	return token,res

######capsolver######
async def capsol(imgpath):
	token = ''
	res = ''
	capsolver.api_key = CAPSOLVER_KEY
	# img_path = os.path.join(Path(__file__).resolve().parent,imgpath)
	try:
		with open(imgpath,'rb') as f:
		    solution = capsolver.solve({
		        "type":"ImageToTextTask",
		        "module":"mtcaptcha", 
		        "body": base64.b64encode(f.read())
		    })
		print(solution)
		token = str(solution['text'])
		res = "chenggong"
	except Exception as e:
		print(e)
		token = str(e)
		res = "shibai"
	return token,res

def save(jilu,t,captcha,excelPath):
	# t = int(t*1000)
	jilu.append(t)
	jilu.append(captcha)
	jilu.append(time.ctime())
	jilu.append(PAGE_URL)
	jilu.append("normal")
	wb = openpyxl.load_workbook(excelPath)
	userExcel = wb['normal']
	userExcel.append(jilu)
	wb.save(excelPath)
	print("完成")

async def twocaptchaimg():
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


async def main():
    # headless = False 为False：有头，True为无头
    # userDataDir 设置当前网站的保存路径，下次登陆时可不用登陆    --disable-infobars禁止策略化
	browser = await launch(headless=False, devtools=True, args=['--disable-web-security','--disable-site-isolation-trials','--allow-running-insecure-content'], userDataDir='C:/Chrome dev session',executablePath='C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')
    # 申明一个page对象
	page = await browser.newPage()
    # 浏览器设置宽高
	await page.setViewport({'width': width, 'height': height})

	for i in range(0,2000):
		###打开页面
		await page.goto(PAGE_URL,{'waitUntil' : 'domcontentloaded'})
		await asyncio.sleep(3)
		jilu = list()

		###获取图片
		print("保存图片")
		# imgpath = os.path.join(imgFolderpath,str(time.ctime()) + ".png")
		imgpath = imgFolderpath + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".png"
		frame = page.frames# for iframe in frame:	(iframe.name)(iframe.url)(iframe.content)
		iframe = frame[2]
		await page.evaluate('window.scrollTo(0,3000);')
		sleep(5)
		img = await iframe.waitForSelector('#mtcap-image-1')
		await img.screenshot({'path':imgpath})  #保存路径

		###获取答案
		NORMAL = ''
		if i%5 == 0:
			begin = time.time()#破解时间
			token,res = twocap(imgpath)#2captcha
			t = time.time()-begin
			NORMAL = "2captcha"
		if i%5 == 1:
			begin = time.time()#破解时间
			token,res = bestsol(imgpath)#bestsolver
			t = time.time()-begin
			NORMAL = "bestsolver"
		if i%5 == 2:
			begin = time.time()#破解时间
			token,res = anticap(imgpath)#anti-captcha
			t = time.time()-begin
			NORMAL = "anti-captcha"
		if i%5 == 3:
			begin = time.time()#破解时间
			token,res = deathcap(imgpath)#deathcaptcha
			t = time.time()-begin
			NORMAL = "deathcaptcha"
		if i%5 == 4:
			begin = time.time()#破解时间
			token,res = capsol(imgpath)#capsolver
			t = time.time()-begin
			NORMAL = "capsolver"

		print(NORMAL)
		jilu.append(str(token))
		if res == "chenggong":
			await iframe.type('#mtcap-inputtext-1', token)
			print("chenggong")
		else:
			print("shibai")
		
		###判断
		await asyncio.sleep(6)
		element = await iframe.waitForSelector('#mtcap-msg-1')
		text = await iframe.evaluate('(element) => element.textContent',element)
		print(text)
		if text == "Verified Successfully":
			print("识别成功")
			jilu.append("tongguo")
		else:
			print("识别失败")
			jilu.append("shibai")
		
		###记录
		jilu.append(imgpath)
		save(jilu,t,NORMAL,excelPath)
		await asyncio.sleep(3)
		if i%5 == 4:
			# await page.close()
			await asyncio.sleep(60)

	# await asyncio.sleep(100)

data_list = asyncio.get_event_loop().run_until_complete(main())
s = requests.Session()
# s.cookies.set(data_list[0]['name'], data_list[0]['value'])