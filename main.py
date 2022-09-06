from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
import pytz

# # 生成一个时区对象
tzone = pytz.timezone("Asia/Shanghai")
# # 如果不传时区对象，就默认当前用户当前所在时区的当前时间
today = datetime.now(tzone) # 加拿大系统当前的时间
print(today)
# today = datetime.now()

start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
xiaoji = os.environ["XIAOJI"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d").astimezone(tzone)
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d").astimezone(tzone)
  if next < today:
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_shici():
  words=requests.get('https://v1.hitokoto.cn/?c=j')
#   print(words.json()['hitokoto'])
  return words.json()['hitokoto']
client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"shici":{"value":get_shici()}}
res = wm.send_template(user_id, template_id, data)
res = wm.send_template(xiaoji, template_id, data)
print(res)
# print(dayss)
