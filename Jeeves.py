import json
import os
import discord
import requests
from discord.ext import commands, tasks, channel

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

[!쐐기보상]
쐐기 드랍 및 주간보상 템렙
```
    """)

# 인사
@bot.command(name="하이")
async def hello(ctx):
    await ctx.send(ctx.author + " 어서오고")

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
# 교만
우두머리가 아닌 쫄 카운트의 20%마다 교만의 현신을 생성합니다.
- 스킬1/ 교만함 폭발: 2초 마다 60m 내의 플레이어 모두에게 피해를 주고 중첩 당 40%를 증가시키는 교만함 폭발 디버프를 겁니다.

- 스킬2/ 공격적인 과시: 탱커를 제외한 4명 중 1명에게 디버프를 겁니다. 대상은 4초 후에 발사되는 빨간색 미사일이 생성됩니다. 
미사일에 맞으면 2초 간 기절하고 높은 피해를 입습니다. 

- 교만의 현신을 처치한 경우 1분동안 크기가 커지고 이속 60%, 공격력 30%, 초당 마나 5% 증가의 버프를 얻습니다.
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

# 쐐기 보상
@bot.command(name="쐐기보상")
async def item_drop(ctx):
    await channel.send(file=discord.File("./images/mythic_plus_drop.png"))




access_token = os.environ["BOT_TOKEN"]
bot.run(access_token)
