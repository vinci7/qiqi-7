from wxpy import *
from PIL import Image, ImageSequence, ImageFont, ImageDraw
import time
import random
import os

#求图功能
from bs4 import BeautifulSoup
import requests
import urllib.request

#频率限制
from functools import wraps
import datetime

# 图灵API_KEY
TULING_API_KEY = ''

#初始化机器人
bot = Bot(cache_path=True, console_qr=True)
#保存联系人列表
bot.chats(True)

#管理员昵称
admin_nick_name = 'Cookie🍪'

# 工作群
work_group_name = ''

# 一次性返回图片数限制
numberLimit = 2
numberFriendLimit = 3
numberGroupLimit = 1

#[DEBUG] 调试
if bot.self.name == admin_nick_name:
	test = []
	test.append(bot.friends().search('奇奇七号')[0])
	test.append(bot.friends().search('Cookie🍪')[0])


tuling = Tuling(api_key=TULING_API_KEY)

# 大字功能支持颜色
colorDict = {'大字': 'black', '彩虹字': 'black', '黑字': 'black', '白字': 'white', '绿字': 'green', 
			 '红字': 'red', '紫字': 'purple', '蓝字': 'blue', '粉字': 'pink', '黄字': 'yellow', 
			 '橙字': 'orange', '灰字': 'grey', '黑色': 'black', '白色': 'white', '绿色': 'green', 
			 '红色': 'red', '紫色': 'purple', '蓝色': 'blue', '粉色': 'pink', '黄色': 'yellow', 
			 '橙色': 'orange', '灰色': 'grey'}
# 彩虹色
colorSeq = ['红色', '橙色', '黄色', '蓝色', '紫色', '粉色']
# 根据字数调整字号
fontSize = [0, 300, 200, 150, 120, 80, 50, 50, 50, 50, 50, 40, 40, 40, 40, 40, 30, 30, 30] 

# 求图，斗图
tuDict = ['求图', '斗图', 'doutu', 'qiutu']

# 帮助关键字
helpDict = ['做什么', '干什么', '帮助', '说明', '用', 'help', '-h', '--help', '怎么用']

# 帮助信息
helpHint = '发我图片，我可以帮你转换成自定义表情。其他功能的具体使用方法请看我的朋友圈哦！点击如下链接获取更多帮助：https://vinci7.github.io/qiqi-7[玫瑰]'

# 欢迎词
welcomeHint = '你好，奇奇七号自动接收了您的好友请求。发我图片，我可以帮你转换成自定义表情。回复「帮助」获取更多帮助，或者也可以看我的朋友圈查看使用说明哦！[玫瑰]'

# 限制频率: 指定周期内超过消息条数，直接回复 "🙊"
def freq_limit(period_secs=10, limit_msgs=4):
    def decorator(func):
        @wraps(func)
        def wrapped(msg):
            now = datetime.datetime.now()
            period = datetime.timedelta(seconds=period_secs)
            recent_received = 0
            for m in msg.bot.messages[::-1]:
                if m.sender == msg.sender:
                    if now - m.create_time > period:
                        break
                    recent_received += 1

            if recent_received > limit_msgs:
                if not isinstance(msg.chat, Group) or msg.is_at:
                    return '🙊'
            return func(msg)

        return wrapped

    return decorator

#压缩im
def compressIm(im):

	w,h = im.size

	num = 0
	while ((w > 1024) or (h > 1024)):
		w = w//1.2
		h = h//1.2
		try:
			im.thumbnail((w, h))
		except Exception as e:
			raise e
		else:
			num += 1
			print('正在尝试第{}次预压缩，w={} h={}...'.format(num, w, h))
	return im

#转换图片格式 png to gif
def png2gif(file_name, save_path):
	
	im = Image.open(save_path)
	w, h = im.size

	#处理图片过大
	if ((w > 10000) or (h > 10000)):
		return 0, w, h, 0

	#压缩im
	im = compressIm(im)

	#保存自定义表情
	try:
		gif_path = './image/'+file_name+'.gif'
		im.save(gif_path, 'gif')
	except Exception as e:
		raise e
		im.close()
		return gif_path, w, h, 0
	else:
		im.close()
		#返回
		return gif_path, w, h, os.path.getsize(gif_path)
	

#转换图片格式 img to gif
def img2gif(file_name, from_path):
	
	im = Image.open(from_path)
	w, h = im.size

	#处理图片过大
	if ((w > 10000) or (h > 10000)):
		return 0, w, h, 0

	#压缩im
	im = compressIm(im)

	#保存自定义表情
	try:
		gif_path = './memes/'+file_name+'.gif'
		im.save(gif_path, 'gif')
	except Exception as e:
		raise e
		im.close()
		return gif_path, w, h, 0
	else:
		im.close()
		#返回
		return gif_path, w, h, os.path.getsize(gif_path)


# 转换自定义表情函数
def automeme(msg):

	if ((isinstance(msg.chat, Group)) and (msg.chat.name != work_group_name)):
		print('{}群中发了一张图片'.format(msg.chat))
		return

	file_name = msg.file_name

	#不处理gif表情
	if (file_name.endswith('.gif')):
		if (isinstance(msg.chat, Group)):
			return
		else:
			return '发相册中保存的图片才能转换哦~[玫瑰]' 
	
	#保存图片
	save_path = './image/'+file_name
	msg.get_file(save_path)
	
	#压缩图片
	try:
		#[LOG]开始压缩
		print('start compression: {}, {}'.format(msg, file_name))
		gif_path, w, h, size = png2gif(file_name, save_path)
		
	except Exception as e:
		raise e
		return '压缩图片失败，请稍后再试...'
	else:
		#处理图片过大
		if (gif_path == 0):
			return '图片太大啦！'
			#[LOG] 图片过大
			print('too big pic!:{}, {}; w*h: {}*{};'.format(msg, file_name, w, h))
		else:
			#[LOG] 图片信息，压缩成功
			print('compression successful:{}, {}; w*h: {}*{}; size: {}'.format(msg, file_name, w, h, size))

	#回复自定义表情
	try:
		msg.reply_image(gif_path, None)
	except Exception as e:
		print(e)
		return '机器人失联中，请稍后再试...'
	else:
		if (os.path.exists(gif_path)):
			os.remove(gif_path)


#[DEBUG] 转换自定义表情事件
if bot.self.name == admin_nick_name:
	@bot.register(chats=test, msg_types=PICTURE, except_self=False)
	@freq_limit()
	def automeme_test(msg):
		return automeme(msg)
else:
	@bot.register(chats=Friend, msg_types=PICTURE, except_self=True)
	@bot.register(chats=Group, msg_types=PICTURE, except_self=True)
	@freq_limit()
	def automeme_online(msg):
		return automeme(msg)


def dazi(text, length, color='black'):

	# 字号
	if (length > 10):
		font = ImageFont.truetype("msyh.ttf", fontSize[length])
	else:
		font = ImageFont.truetype("msyhbd.ttf", fontSize[length])
	
	# 生成空白图 画上大字
	w,h = font.getsize(text)
	im = Image.new("RGBA", (w, h), (0,0,0,0))
	draw = ImageDraw.Draw(im)
	draw.text((0,0), text, font = font, fill = color)

	#[LOG] 创建大字gif
	print("create dazi gif size: {}*{}, text: {}, color: {}".format(w, h, text, color))

	#压缩图片
	im = compressIm(im)

	# 生成透明背景gif图
	# Get the alpha band
	alpha = im.split()[3]
	# Convert the image into P mode but only use 255 colors in the palette out of 256
	im = im.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
	# Set all pixel values below 128 to 255, and the rest to 0
	mask = Image.eval(alpha, lambda a: 255 if a <=128 else 0)
	# Paste the color of index 255 and use alpha as a mask
	im.paste(255, mask)
	# The transparency index is 255
	gif_path = "./dazi/text_{}.gif".format(random.randint(0,100000))
	im.save(gif_path, transparency=255)

	return gif_path

def saveImgbyURL(imageURL,fileName):
	u = urllib.request.urlopen(imageURL)
	data = u.read()
	f = open(fileName, 'wb')
	f.write(data)
	f.close()

def qiutu(query, numberLimit):

	# 爬虫，求图网站
	html = requests.get("https://www.doutula.com/search?keyword={}".format(query)).content
	soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')

	memeDivs = soup.find_all('a', attrs={"data-picid": True})

	memes = []
	for memeDiv in memeDivs:
		memeImg = memeDiv.find('img', class_="img-responsive lazy image_dtb")
		
		meme = []
		meme.append(memeDiv['data-picid'])
		meme.append(memeDiv.find('p').text)
		meme.append('http:{}'.format(memeImg['data-original']))

		memes.append(meme)

	getNumber = min(len(memes), numberLimit)
	# 从爬取的结果中随机选取 getNumber 个表情返回
	results = random.sample(memes, getNumber)
	print('find {} memes'.format(len(memes)))


	pic_paths = []

	# 保存表情
	for result in results:
		url = result[2]
		postfix = url[url.rfind('.'):]
		fileName = "memes/{}{}".format(result[0], postfix)
		saveImgbyURL(url, fileName)

		# 如果表情不是gif格式就转换成gif格式
		if postfix == '.gif':
			pic_paths.append(fileName)
		else:
			try:
				gif_path, w, h, size = img2gif(result[0], fileName)
			except Exception as e:
				print(e)
				print('img2gif failure!')
			else:
				print(url, gif_path)
				pic_paths.append(gif_path)

	# 返回表情路径
	return pic_paths

# 处理文字消息函数
def autotext(msg):
	
	raw_text = msg.text.strip()
	keyword = msg.text.split()[0]

	if (len(keyword) <= 1):
		return

	if ((keyword in tuDict) or (keyword in colorDict)):
		text = ''
		try:
			text = raw_text[raw_text.index(' ')+1:].strip()
		except Exception as e:
			print(e)
			#[LOG] no space
			print('{}, 没有空格符...'.format(raw_text))
			return
		length = len(text)
	elif ((not isinstance(msg.chat, Group)) or (msg.is_at)):
		for helpword in helpDict:
			if helpword in raw_text:
				return helpHint
		return
	else:
		#tuling.do_reply(msg)
		return

	#斗图功能
	if (keyword in tuDict):

		# 回复图片数限制
		if (isinstance(msg.chat, Friend)):
			pic_paths = qiutu(text, numberFriendLimit)
		else:
			pic_paths = qiutu(text, numberGroupLimit)
		
		# 没找到表情
		if (len(pic_paths) == 0):
			return '十分抱歉！没找到相关表情，请换关键词后重试...'

		# 处理找到的表情
		for pic_path in pic_paths:
			try:
				msg.reply_image(pic_path, None)
			except Exception as e:
				print(e)
				return '机器人失联中，请稍后再试...'

	#大字，多颜色支持
	elif (keyword in colorDict):
		
		#确认颜色
		color = colorDict[keyword]

		#当然是选择原谅TA！
		if ('原谅' in text):
			color = 'green'
		
		if (length <= 17):
			try:
				gif_path = dazi(text, length, color)
				msg.reply_image(gif_path, None)
			except Exception as e:
				print(e)
				return '机器人连不上网了，请稍后再试...'
			else:
				if (os.path.exists(gif_path)):
					os.remove(gif_path)
		else:
			return '字数太多啦!'


#[DEBUG] 文字消息事件
if bot.self.name == admin_nick_name:
	@bot.register(chats=test, msg_types=TEXT, except_self=False)
	@freq_limit()
	def automeme_test(msg):
		return autotext(msg)
else:
	@bot.register(chats=Friend, msg_types=TEXT, except_self=True)
	@bot.register(chats=Group, msg_types=TEXT, except_self=True)
	@freq_limit()
	def automeme_online(msg):
		return autotext(msg)


# 自动接受好友请求
if bot.self.name != admin_nick_name:
	@bot.register(msg_types=FRIENDS)
	def auto_accept_friends(msg):
		new_friend = bot.accept_friend(msg.card)
		new_friend.send(welcomeHint)
		print(msg.card)


# 堵塞线程，并进入 Python 命令行
bot.join()


