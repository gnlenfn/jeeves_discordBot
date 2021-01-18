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
    print(f"ID: {bot.user.id}")

@bot.command(name="명령어", description="명령어 안내")
async def info(ctx):
    await ctx.send("""
```ini
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

[!나락]
나락런 관련 자료 
```
    """)

# 인사
@bot.command(name="하이")
async def hello(ctx):
    await ctx.send(ctx.message.author.mention + " 어서오고")

# 입창!!
@bot.command(name="민용")
async def 민용(ctx):
    await ctx.send("이거이거 3시에 돈 바짝벌지")
@bot.command(name="정민")
async def 정민(ctx):
    await ctx.send("청주 거부 신흥 재력가")
@bot.command(name="연성")
async def 연성(ctx):
    await ctx.send("사무관 (진)")
@bot.command(name="노경")
async def 노경(ctx):
    await ctx.send("배.노.경")

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

def create_access_token(client_id, client_secret, region = 'kr'):
    data = { 'grant_type': 'client_credentials' }
    response = requests.post('https://%s.battle.net/oauth/token' % region, data=data, auth=(client_id, client_secret))
    return response.json()

response = create_access_token(os.environ["CLIENT_ID"], os.environ["CLIENT_SECRET"])
access = response['access_token']
# 토큰 가격
@bot.command(name="토큰", description="오늘의 토큰 가격")
async def token(ctx):
    print("request token price!")
    url = "https://kr.api.blizzard.com/data/wow/token/index?namespace=dynamic-kr&locale=ko_KR&access_token="+access
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
    await ctx.send(data["title"])
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

# 쐐기 보상
@bot.command(name="쐐기보상")
async def item_drop(ctx):
    await ctx.send(file=discord.File("./images/mythic_plus_drop.png"))

# 영혼재
@bot.command(name="영혼재")
async def soul_ash(ctx):
    print("request soul ash!")
    await ctx.send("""
    ```md
    - 1등급(190): 1250
    - 2등급(210): 2000
    - 3등급(225): 3200
    - 4등급(235): 5150
    ```
    """)

# 나락런
@bot.command(name="나락")
async def soul_ash(ctx):
    print("request The mow!")
    await ctx.send(file=discord.File("./images/venari.png"))
    url = "https://goo-gle.tistory.com/194"
    await ctx.send(f"{url} <- 나락런 (어둠땅 초기 참고)")

############################# 노래 재생 ##############################################
@bot.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()


access_token = os.environ["BOT_TOKEN"]
bot.run(access_token)
