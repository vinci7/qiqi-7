from wxpy import *
from PIL import Image
import os

bot = Bot(console_qr=True)

@bot.register(chats=Friend, msg_types=PICTURE, except_self=True)
@bot.register(chats=Group, msg_types=PICTURE, except_self=True)
def automeme(msg):

    file_name = msg.file_name
    #回复自定义表情信息
    if (file_name.endswith('.gif')):
        print(type(msg.chat))
        return 
        return '盗图狗在此，发一张盗一张[害羞]'

    #保存图片
    save_path = './image/'+file_name
    msg.get_file(save_path)
    #转换图片格式 png2gif
    im = Image.open(save_path)
    w, h = im.size
    #打印图片信息
    print(msg, file_name, 'size: {}*{}'.format(w, h))
    #压缩图片
    num = 0
    while ((w > 1024) or (h > 1024)):
        w = w//1.2
        h = h//1.2
        im.thumbnail((w, h))
        num += 1
        print('正在尝试第{}次预压缩，w={} h={}...'.format(num, w, h))
    #保存自定义表情
    gif_path = './image/'+file_name+'.gif'
    im.save(gif_path, 'gif')
    print(os.path.getsize(gif_path))
    #回复自定义表情
    try:
        msg.reply_image(gif_path, None)
    except Exception as e:
        print('正在尝试第1次压缩...')
        im.thumbnail((w//2, h//2))
        im.save(gif_path, 'gif')
        try:
            msg.reply_image(gif_path, None)
            print('处理成功...')
        except Exception as e:
            print('正在尝试第2次压缩...')
            im.thumbnail((w//2, h//2))
            im.save(gif_path, 'gif')
            try:
                msg.reply_image(gif_path, None)
                print('处理成功...')
            except Exception as e:
                print(e)
                return '机器人失联中...'
    except ConnectionError:
        return '机器人失联中...'
    #关闭图片
    im.close()

#自动处理文字消息

@bot.register(chats=Friend, msg_types=TEXT, except_self=True)
def auto_reply_text_message(msg):
    return '发图吧〜'

# 自动接受好友请求
@bot.register(msg_types=FRIENDS)
def auto_accept_friends(msg):
    new_friend = bot.accept_friend(msg.card)
    new_friend.send('你好，我自动接收了您的好友请求。发我图片，我可以帮你转换成自定义表情。[玫瑰]')
    print(msg.card)


# 堵塞线程，并进入 Python 命令行
bot.join()