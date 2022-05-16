from selenium import webdriver
from bs4 import BeautifulSoup
import time, os
import requests
from datetime import datetime
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import discord
import asyncio
import re
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
import logging
import time
import nest_asyncio
import glob
import numpy as np

# def item_croll(soup) :
#     regexp = re.compile('[+\d]+\s[가-힣+\s]+')
#     item = soup.select('span.d-block.text-grade5') # 유뮬
#     item_p = []
#     for idx, i in enumerate(item) :
#         if regexp.findall(str(item[idx])) :
#             item_p.append(",".join(regexp.findall(str(item[idx]))))
            
#     item2 = soup.select('span.d-block.text-grade6') # 고대
#     item2_p = []
#     for idx, i in enumerate(item2) :
#         if regexp.findall(str(item2[idx])) :
#             item2_p.append(",".join(regexp.findall(str(item2[idx]))))
            
#     return item_p + item2_p # 장착 유물 방어구


def item_croll(soup) :
    투구 = soup.select_one('#tab-equips > div > a.char-equip.equip-1 > div > div > h4 > span').get_text()
    견장 = soup.select_one('#tab-equips > div > a.char-equip.equip-5 > div > div > h4 > span').get_text()
    상의 = soup.select_one('#tab-equips > div > a.char-equip.equip-2 > div > div > h4 > span').get_text()
    하의 = soup.select_one('#tab-equips > div > a.char-equip.equip-3 > div > div > h4 > span').get_text()
    장갑 = soup.select_one('#tab-equips > div > a.char-equip.equip-4 > div > div > h4 > span').get_text()
    무기 = soup.select_one('#tab-equips > div > a.char-equip.equip-0 > div > div > h4 > span').get_text()
    return 투구, 견장, 상의, 하의, 장갑, 무기

def stat_croll(soup) :

    공격력 = soup.select_one('#qul-box-1 > div.qul-box-1-wrap.pt-2.pb-2.ps-1.pe-1.rounded.shadow-sm.bg-theme-4.text-left > div > div.row.pt-1.pb-0.ps-0.pe-0.m-0.mb-2 > div:nth-child(1) > span > span.text-grade5').get_text()
    최대생명력 = soup.select_one('#qul-box-1 > div.qul-box-1-wrap.pt-2.pb-2.ps-1.pe-1.rounded.shadow-sm.bg-theme-4.text-left > div > div.row.pt-1.pb-0.ps-0.pe-0.m-0.mb-2 > div:nth-child(2) > span.text-grade5').get_text()

    치명 = soup.select_one('#qul-box-1 > div.qul-box-1-wrap.pt-2.pb-2.ps-1.pe-1.rounded.shadow-sm.bg-theme-4.text-left > div > div:nth-child(4) > div:nth-child(1) > span > span.text-grade5').get_text()
    특화 = soup.select_one('#qul-box-1 > div.qul-box-1-wrap.pt-2.pb-2.ps-1.pe-1.rounded.shadow-sm.bg-theme-4.text-left > div > div:nth-child(4) > div:nth-child(2) > span > span.text-grade5').get_text()
    제압 = soup.select_one('#qul-box-1 > div.qul-box-1-wrap.pt-2.pb-2.ps-1.pe-1.rounded.shadow-sm.bg-theme-4.text-left > div > div:nth-child(5) > div:nth-child(1) > span > span.text-grade5').get_text()
    신속 = soup.select_one('#qul-box-1 > div.qul-box-1-wrap.pt-2.pb-2.ps-1.pe-1.rounded.shadow-sm.bg-theme-4.text-left > div > div:nth-child(5) > div:nth-child(2) > span > span.text-grade5').get_text()
    인내 = soup.select_one('#qul-box-1 > div.qul-box-1-wrap.pt-2.pb-2.ps-1.pe-1.rounded.shadow-sm.bg-theme-4.text-left > div > div:nth-child(6) > div:nth-child(1) > span > span.text-grade5').get_text()
    숙련 = soup.select_one('#qul-box-1 > div.qul-box-1-wrap.pt-2.pb-2.ps-1.pe-1.rounded.shadow-sm.bg-theme-4.text-left > div > div:nth-child(6) > div:nth-child(2) > span > span.text-grade5').get_text()

    return 공격력, 최대생명력, 제압, 신속, 인내, 숙련, 치명, 특화

def engraving(soup) :
    item = soup.select('#qul-box-3 > div > div > div')[0].get_text().split('\n\xa0')
#     engrav_text = item.split('\n')
    engrav_text = ''.join(i for i in item)

    return engrav_text

def kill_thread(thread):
    """
    thread: a threading.Thread object
    """
    thread_id = thread.ident
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
    if res > 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
        print('Exception raise failure')
        


def URL_croll(keyword, driver) :    


    link = 'https://www.youtube.com/results?search_query=' + keyword
    driver.get(link)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    my_titles = soup.select(
        'h3 > a'
        )

    title = []
    url = []

    for idx in my_titles:
        if idx.get('href')[:7] != '/watch?':
            pass
        else:
            title.append(idx.text)
            url.append(idx.get('href'))

    title_list = pd.DataFrame(url, columns = ['url'])
    title_list['title'] = title
    # print(my_titles)
    # display(title_list)
    return title_list._get_value(0, 'url'), title_list._get_value(0, 'title')


    
    


def queue(id): #음악 재생용 큐
    if que[id] != []:
        player = que[id].pop(0)
        playerlist[id] = player
        del playlist[0]
        player.start()



nest_asyncio.apply()

now = time.localtime()
datetime = "%04d%02d%02d" % (now.tm_year, now.tm_mon, now.tm_mday)

#####for logging 
file = "./log/" + datetime + ".log" #로깅 
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
# logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename= file, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
#####

##### for emo
listdir = os.listdir("C:/Users/kyeongmin/Desktop/labs/private/discord/images/로스트아크_환영해요_로아콘!/image")
image_df = pd.DataFrame(listdir, columns = ['path'])
for idx, i in enumerate(image_df.index) :
    
    text = image_df._get_value(idx, col = 'path').split('.')[0].split('_')[-1]
    text = ''.join(filter(str.isalnum, text)) 
    image_df._set_value(idx, 'key', text)
#####


##### for tip
tip_listdir = os.listdir("C:/Users/kyeongmin/Desktop/labs/private/discord/images/팁")
tip_df = pd.DataFrame(tip_listdir, columns = ['path'])
for idx, i in enumerate(tip_df.index) :

    text = tip_df._get_value(idx, col = 'path').split('.')[0].split('_')[-1]
    text = ''.join(filter(str.isalnum, text)) 
    tip_df._set_value(idx, 'key', text)
#####

app = commands.Bot(command_prefix = "!")

@app.event
async def on_ready():
    print("다음으로 로그인합니다 : ") # 봇 디스코드 세션 로그인
    print(app.user.name)
    print(app.user.id)
    print("==========")
    game = discord.Game("!명령어") # 봇 현재 상태
    await app.change_presence(status=discord.Status.online, activity=game) # 활동 상태 표시
    
@app.event
async def on_message(message) :
#     print(message.content)
    await app.process_commands(message)

        
@app.command(pass_context = True)
async def 검색(ctx, char_id) :
    try :
        loawa_url = 'https://loawa.com/char/'
        html = requests.get(loawa_url + char_id)
        soup = BeautifulSoup(html.text, 'html.parser')
    except discord.ext.commands.errors.MissingRequiredArgument :
        await ctx.send("검색할 모험가명을 입력해 주세요.")
    
    stat = []
    p = re.compile('[\d+]')
    try :
        temp = list(stat_croll(soup))
        for idx, i in enumerate(temp) :
            stat.append(''.join(p.findall(temp[idx])))

        item_text = '\n'.join(item_croll(soup))
    #     item_text = '\t\n'.join(i for i in item_p )

        embed=discord.Embed(title = char_id, url="https://loawa.com", description= item_text, color=0x369140)
        embed.set_author(name="로아와 검색", url= loawa_url + char_id)

        embed.add_field(name = '\n==========================\n', value = '\u200b', inline = False)
        embed.add_field(name="신속", value=stat[3], inline=True)
        embed.add_field(name="치명", value=stat[6], inline=True)
        embed.add_field(name="숙련", value=stat[4], inline=True)
        embed.add_field(name="특화", value=stat[7], inline=True)
        embed.add_field(name="제압", value=stat[2], inline=True)
        embed.add_field(name="인내", value=stat[4], inline=True)
        embed.add_field(name="공격력", value=stat[0], inline=True)
        embed.add_field(name="최대생명력", value=stat[1], inline=True)

        embed.add_field(name = '\n==========================\n', value = '\u200b', inline = False)     
        embed.add_field(name="각인 효과", value = engraving(soup), inline = False)
        embed.set_footer(text="")
        await ctx.send(embed=embed)
        
    except :
        await ctx.send('존재하지 않는 모험가입니다.')
    


    
    
@app.command(pass_context = True)
async def 재생(ctx, *, char) :
    print(char)
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        url, title = URL_croll(char, driver)
        print(url, title)
        url = 'https://www.youtube.com' + url
        url1 = re.match('(https?://)?(www\.)?((youtube\.(com))/watch\?v=([-\w]+)|youtu\.be/([-\w]+))', url) #정규 표현식을 사용해 url 검사
        if url1 == None:
            await ctx.send(embed=discord.Embed(title=":no_entry_sign: url을 제대로 입력해주세요.",colour = 0x2EFEF7, description = url1))
        else :
            if ctx.author.voice and ctx.author.voice.channel:
                channel = ctx.author.voice.channel
                await ctx.send(embed=discord.Embed(title = title, colour = 0x2EFEF7, description = url))
                await channel.connect()
            else:
                await ctx.send("초대할 음성채널에 먼저 입장해 주세요!")            
    except IndexError:
        await ctx.send(embed=discord.Embed(title=":no_entry_sign: url을 입력해주세요.",colour = 0x2EFEF7))



        
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(app.voice_clients, guild=ctx.guild) #discord.utils.get

    if not voice.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
    else:
        await ctx.send("노래 종료 후 사용해 주세요. !노래끄기")
        
    if char == "끄기" :
        await app.voice_clients[0].disconnect()


@app.command(pass_context = True)
async def 노래끄기(ctx) :
    await app.voice_clients[0].disconnect()
    
@app.command(pass_context = True)
async def 삭제(ctx, char) :
    
#     user = discord.utils.get(message.guild.members, name = name) NOT WORKING (TODO : get user information)
    try :
        await ctx.message.channel.purge(limit = int(char))
#         await ctx.send(user.mension + " " + char + "개의 메시지를 삭제했습니다.")
        await ctx.send(char + "개의 메시지를 삭제했습니다.")
    except ValueError:
        await ctx.send("해당 명령어는 !삭제 {줄}로 사용 가능합니다.")
    except discord.errors.Forbidden :
        await ctx.send("권한이 부족합니다. 관리자에게 문의하세요.")

    
        
        
@app.command(pass_context = True)
async def 이모티콘(ctx, char) :
    dir_path = "C:/Users/kyeongmin/Desktop/labs/private/discord/images/로스트아크_환영해요_로아콘!/image/"
    if len(image_df[image_df['key'] == char]) > 0 :
        file_name = image_df[image_df['key'] == char]['path'].tolist()[0]
#         print(file_name)
        file = discord.File(dir_path + file_name, filename = char + ".png")
        await ctx.message.channel.purge(limit = int(1))
        await ctx.send(file = file)
    else :
        await ctx.send("현재는 사용할 수 없는 이모티콘입니다.")

@app.command(pass_context = True)
async def 팁(ctx, char) :

    dir_path = "C:/Users/kyeongmin/Desktop/labs/private/discord/images/팁/"
    if len(tip_df[tip_df['key'] == char]) > 0 :
        file_name = tip_df[tip_df['key'] == char]['path'].tolist()[0]

        file = discord.File(dir_path + file_name, filename = char + ".png")

        await ctx.send(file = file)
    else :
        await ctx.send("존재하지 않는 이미지입니다.")
        
        
@app.command(pass_context = True)
async def 각인계산기(ctx) :
    url = 'https://loa.icepeng.com/imprinting'
    await ctx.send(embed=discord.Embed(title = "icepeng 각인계산기", colour = 0x2EFEF7, description = url))
        
    
        
        
@app.command(pass_context = True)
async def 명령어(ctx, char) :   
    url = 'https://korea3500.notion.site/Coffee-5bb06765136f49e39f645b1f61e37651'
    if "이모티콘" in char :
        
        await ctx.send("작업 중")
    

@app.command(pass_context= True)
async def 총쏘는진첩이(ctx) :
    await ctx.send("건슬링어 짱짱쌔요!")
    
@app.command(pass_context= True)
async def 디에스공(ctx) :
    await ctx.send("고백살인마")
    
@app.command(pass_context = True)
async def 계산기(ctx, char) :
    quadro_optimal_value = 0
    octa_optimal_value = 0
    discount_factor = 0.95
    
    
    char = int(char)
    quadro_optimal_value = np.round(char * discount_factor * 3/4, 2)
    octa_optimal_value = np.round(char * discount_factor * 7/8, 2)

    ### generating https://cog-creators.github.io/discord-embed-sandbox/  ###
    embed=discord.Embed(title="로아 경매 이득금 계산기", url="http://github.com/korea3500", description="입력한 금액 : " + str(char))
    embed.add_field(name="4인 파티 기준", value = quadro_optimal_value, inline=True)
    embed.add_field(name="8인 공격대 기준", value = octa_optimal_value, inline=True)
    await ctx.send(embed=embed)

@app.command(pass_context = True)
async def 사사게(ctx, *, char) :
#     print(char)
    search_id = char.replace(' ', '+')
    
    inven_url = 'https://www.inven.co.kr/board/lostark/5355?query=list&p=1&sterm=&name=subject&keyword='
    html = requests.get(inven_url + search_id)
    soup = BeautifulSoup(html.text, 'html.parser')
    result = soup.find_all("a", class_="subject-link")

    title_list = []
    url_list = []
    for idx, i in enumerate(result) :
        title = i.get_text()
        title_list.append(''.join(title.replace('    ', '').split('\n')))
        url_list.append(result[idx]['href'])
#     print(title_list, url_list)
    if len(title_list) == 1 :
        embed=discord.Embed(title="인벤 사사게 검색", url= inven_url + search_id, description="검색한 키워드 : " + char)
        embed.add_field(name = "검색 결과가 없습니다!", value = url_list[0], inline=False)
        await ctx.send(embed=embed)
    
    else :
        embed=discord.Embed(title="인벤 사사게 검색", url= inven_url + search_id, description="검색한 키워드 : " + char)
        for idx in range(1, len(title_list)) : # 인벤 사사게 검색 중 기본 게시물인 사사게 정책 게시글을 표시하지 않기 위함
#             print(title_list[idx])
            embed.add_field(name = title_list[idx], value = url_list[idx], inline=False)

    #     embed.set_footer(text = "add footer")
        await ctx.send(embed=embed)

    


    
@명령어.error
async def 명령어_error(ctx, error) :
    url = 'https://korea3500.notion.site/Coffee-5bb06765136f49e39f645b1f61e37651'
    await ctx.send(embed=discord.Embed(title="Coffee guide",colour = 0x2EFEF7, description = url))    

@삭제.error
async def 삭제_error(ctx, error) :
    if isinstance(error, commands.MissingRequiredArgument) :
        await ctx.send("해당 명령어는 !삭제 {줄}로 사용 가능합니다.")

@이모티콘.error
async def 이모티콘_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
#         await ctx.send("사용할 이모티콘의 이름을 입력 해주세요!")
        await ctx.send(', '.join(image_df['key']))
        
        
@팁.error
async def 팁_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        tip_listdir = os.listdir("C:/Users/kyeongmin/Desktop/labs/private/discord/images/팁")
        await ctx.send("사용할 팁의 이름을 입력 해주세요! !팁 {팁}\n\n사용가능한 팁 : \n" + ', '.join(tip_df['key']))
        
@계산기.error
async def 계산기_error(ctx, error) :
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("경매 금액을 입력해 주세요!")
    if isinstance(error, commands.CommandInvokeError) :
        await ctx.send("경매 금액은 반드시 숫자여야 합니다.\nex) !계산기 6000")
        
@사사게.error
async def 사사게_error(ctx, error) :
    if isinstance(error, commands.MissingRequiredArgument) :
        await ctx.send("검색 키워드를 입력해 주세요!\nex) !사사게 커피왜캐맛있음")
        
        
# @app.error
# async def app_error(ctx, error) :
#     url = 'https://korea3500.notion.site/Coffee-5bb06765136f49e39f645b1f61e37651'
#     await ctx.send("등록되지 않은 명령어입니다. !help 를 확인해주세요!")
#     await ctx.send(embed=discord.Embed(title="Coffee guide",colour = 0x2EFEF7, description = url))    

token = '__TOKEN__'
app.run(token)