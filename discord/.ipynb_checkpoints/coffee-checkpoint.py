import selenium
import bs4
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import discord
from discord.ext import commands
import nest_asyncio
import asyncio
import discord
nest_asyncio.apply()
import requests
from bs4 import BeautifulSoup
import random
import re
import discord
import logging
import time



def item_croll(soup) :
    regexp = re.compile('[+\d]+\s[가-힣+\s]+')
    item = soup.select('span.d-block.text-grade5') # 유뮬 방어구
    item_p = []
    for idx, i in enumerate(item) :
        if regexp.findall(str(item[idx])) :
            item_p.append(",".join(regexp.findall(str(item[idx]))))
            
    item2 = soup.select('span.d-block.text-grade6') # 고대 방어구
    item2_p = []
    for idx, i in enumerate(item2) :
        if regexp.findall(str(item2[idx])) :
            item2_p.append(",".join(regexp.findall(str(item2[idx]))))
            
    return item_p + item2_p # 장착 방어구

def stat_croll(soup) :

    공격력 = soup.select('#qulbox1 > div > div.p-0.mp > div:nth-child(3) > div:nth-child(1) > span > span')
    최대생명력 = soup.select('#qulbox1 > div > div.p-0.mp > div:nth-child(3) > div:nth-child(2) > span.text-grade5')

    공격력 = str(공격력).split('>')[1].split('<')[0]
    최대생명력 = str(최대생명력).split('>')[1].split('<')[0]
    
    치명 = soup.select_one('#qulbox1 > div > div.p-0.mp > div:nth-child(7)').get_text()[:7].split(' ')[1]
    특화 = soup.select_one('#qulbox1 > div > div.p-0.mp > div:nth-child(7)').get_text()[7:].split(' ')[1]
    제압 = soup.select_one('#qulbox1 > div > div.p-0.mp > div:nth-child(8)').get_text()[:7].split(' ')[1]
    신속 = soup.select_one('#qulbox1 > div > div.p-0.mp > div:nth-child(8)').get_text()[7:].split(' ')[1]
    인내 = soup.select_one('#qulbox1 > div > div.p-0.mp > div:nth-child(9)').get_text()[:7].split(' ')[1]
    숙련 = soup.select_one('#qulbox1 > div > div.p-0.mp > div:nth-child(9)').get_text()[7:].split(' ')[1]


    return 공격력, 최대생명력, 제압, 신속, 인내, 숙련, 치명, 특화

def engraving(soup) :
    item = soup.select('#qulbox3 > div > div')[0].get_text().split('\xa0')
    engrav = list(filter(None, item))[1:]
    engrav_text = '\t\n'.join(i for i in engrav)
    
    return engrav_text






now = time.localtime()
datetime = "%04d%02d%02d" % (now.tm_year, now.tm_mon, now.tm_mday)
file = "./log/" + datetime + ".log" #로깅 

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename= file, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

app = commands.Bot(command_prefix = "!")
token = ''

@app.event
async def on_ready():
    print("다음으로 로그인합니다 : ") # 봇 디스코드 세션 로그인
    print(app.user.name)
    print(app.user.id)
    print("==========")
    game = discord.Game("아메리카노 주문") # 봇 현재 상태
    await app.change_presence(status=discord.Status.online, activity=game) # 활동 상태 표시
    
@app.event
async def on_message(message) :
    await app.process_commands(message)

        
@app.command(pass_context = True)
async def 검색(ctx, char_id) :
#     char_id = message.content[4:]
    loawa_url = 'https://loawa.com/char/'
    html = requests.get(loawa_url + char_id)
    soup = BeautifulSoup(html.text, 'html.parser')
    공격력, 최대생명력, 제압, 신속, 인내, 숙련, 치명, 특화 = stat_croll(soup)
    item_p = item_croll(soup)
    item_text = '\t\n'.join(i for i in item_p )

    embed=discord.Embed(title = char_id, url="http://github.com/korea3500", description= item_text, color=0x369140)
    embed.set_author(name="로아와 검색", url= loawa_url + char_id)

    embed.add_field(name = '\n==========================\n', value = '\u200b', inline = False)
    embed.add_field(name="신속", value=신속, inline=True)
    embed.add_field(name="치명", value=치명, inline=True)
    embed.add_field(name="숙련", value=숙련, inline=True)
    embed.add_field(name="특화", value=특화, inline=True)
    embed.add_field(name="제압", value=제압, inline=True)
    embed.add_field(name="인내", value=인내, inline=True)
    embed.add_field(name="공격력", value=공격력, inline=True)
    embed.add_field(name="최대생명력", value=최대생명력, inline=True)
    
    embed.add_field(name = '\n==========================\n', value = '\u200b', inline = False)
    embed.add_field(name="각인 효과", value = engraving(soup), inline = False)
    embed.set_footer(text="")
    await ctx.send(embed=embed)
        
        
        
#for test
@app.command(pass_context = True)
async def random(ctx, num1, num2) :
    picked = random.randint(int(num1), int(num2))
    await ctx.send('뽑힌 숫자는 : '+str(picked))

    
    
app.run(token)