import json
import os

import discord
import requests
from discord.ext import commands, tasks

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print("--- 연결 성공 ---")
    print("bot name: 리브스")
    print("ID: {bot.user.id}")

@bot.command(name="명령어", description="명령어 안내")
async def info(ctx):
    await ctx.send("""
```ini
[!민용]
그는...

[!레이더 (이름) (서버)]
쐐기 레이더 검색
아즈샤라는 서버 안써도 무관

[!토큰]
오늘의 토큰 가격

[!어픽스]
이번주 쐐기 어픽스

[!로그 (이름) (서버)]
WCL 로그 검색
아즈샤라는 서버 안써도 무관

[!쐐기루트]
주간 쐐기 루트 MDT 확인
```
    """)

# 입창!!
@bot.command(name="민용", description="그는 입창이다.")
async def 민용(ctx):
    await ctx.send("입창!")

# 레이더 검색
@bot.command(name="레이더", description="레이더 검색")
async def raider(ctx, *args):
    try:
        if len(args) > 1:
            nick, sev = args[0], args[1]
        else:
            nick, sev = args[0], "아즈샤라"
        response = requests.get(f'https://raider.io/api/v1/characters/profile?region=kr&realm={sev}&name={nick}')#, headers=headers, params=params)
        data = response.json()
        await ctx.send(data["profile_url"])
    except:
        await ctx.send("*** 검색 실패 ***")

# 토큰 가격
@bot.command(name="토큰", description="오늘의 토큰 가격")
async def token(ctx):
    url = "https://kr.api.blizzard.com/data/wow/token/index?namespace=dynamic-kr&locale=ko_KR&access_token=USCXiOLLG2QPYOBq2XMkFFSAE28I7H08IR"
    res = requests.get(url)
    data = res.json()
    price = format(int(data["price"]) // 10000, ",")
    await ctx.send(f"오늘의 토큰 가격: {price} 골드")

# 이번주 쐐기 어픽스 
@bot.command(name='어픽스', description="이번 주 어픽스")
async def affix(ctx):
    headers = {
    'accept': 'application/json',
    }

    params = (
        ('region', 'kr'),
        ('locale', 'ko'),
    )

    response = requests.get('https://raider.io/api/v1/mythic-plus/affixes', headers=headers, params=params)
    data = response.json()
    await ctx.send(data["title"] + "\n" + "\n")
    await ctx.send(f"""
```md
# {data["affix_details"][0]["name"]}
{data["affix_details"][0]["description"]}
# {data["affix_details"][1]["name"]}
{data["affix_details"][1]["description"]}
# {data["affix_details"][2]["name"]}
{data["affix_details"][2]["description"]}
# {data["affix_details"][3]["name"]}
{data["affix_details"][3]["description"]}
        ```

        """)

# WCL 로그 검색
@bot.command(name="로그", decsription="로그 검색")
async def search_wcl(ctx, *args):
    if len(args) > 1:
        nick, server = args[0], args[1]
    else:
        nick, server = args[0], "아즈샤라"
    await ctx.send(f"https://www.warcraftlogs.com/character/kr/{server}/{nick}")


# 주간 쐐기 루트 MDT
@bot.command(name="쐐기루트", description="MDT 루트 확인")
async def mythic_plus(ctx):
    url = "https://raider.io/news/151-the-weekly-route-tyrannical-prideful-basics"
    await ctx.send(f"{url} <- 주간 쐐기 루트, 던전 별 MDT 문자열 import")


access_token = os.environ["BOT_TOKEN"]
bot.run(access_token)
