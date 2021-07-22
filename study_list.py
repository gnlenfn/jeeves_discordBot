import discord
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
from dotenv import load_dotenv
import os
import logging


def __get_logger():
    """로거 인스턴스 반환
    """

    __logger = logging.getLogger('logger')

    # 로그 포멧 정의
    formatter = logging.Formatter(
        '%(levelname)s##%(asctime)s %(message)s >> @@file::%(filename)s @@line::%(lineno)s')
    # 스트림 핸들러 정의
    stream_handler = logging.StreamHandler()
    # 각 핸들러에 포멧 지정
    stream_handler.setFormatter(formatter)
    # 로거 인스턴스에 핸들러 삽입
    __logger.addHandler(stream_handler)
    # 로그 레벨 정의
    __logger.setLevel(logging.INFO)

    return __logger

logger = __get_logger()
load_dotenv(verbose=True,
            dotenv_path='../.env')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

app = commands.Bot(command_prefix='!')


########################################################################################

@app.event
async def on_ready():
    print('다음으로 로그인합니다: ')
    print(app.user.name)
    print('connection was succesful')
    await app.change_presence(status=discord.Status.online, activity=None)

@app.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        logger.info(f"##### {ctx.author.name} used wrong command #####")
        await ctx.send("올바른 명령어를 사용하세요")
    else:
        raise

@app.command(name='명령어')
async def call_commands(ctx):
    logger.info(f"{ctx.author.name} called a command list")
    await ctx.send(
"""
```md
# !명령어
쓸 수 있는 명령어들을 보여줍니다.

# !문제추가 문제이름 URL
위 명령어 대로 내가 선정한 문제를 공유합니다. 문제풀이 사이트와 URL 적어주시면 됩니다.
ex) !문제추가 백준-문제이름 www.test.com

# !문제목록
지금까지 푼 문제를 구글스프레드시트에 저장하기 때문에 해당 주소를 알려줍니다
```
""")

@app.command(name='문제추가')
async def add_list(ctx, *args):
    site, url = args[0], args[1]
    username = ctx.author.nick
    if not username:
        username = ctx.author.name

    wirte_ps_list(username, site, url)
    await ctx.send("문제 등록 완료")
    logger.info(f"##### {ctx.author.name} added one #####")
    return username, site, url

@app.command(name="문제목록")
async def print_url(ctx):
    await ctx.send("구글스프레드시트:\nhttp://t2m.kr/JeXvW")
    logger.info(f"##### {ctx.author.name} called list #####")

########################################################################################

def wirte_ps_list(username, site, url):
    scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
    ]

    json_file_name = '../rapid-bricolage-304806-3e0bcf6ba899.json'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
    gc = gspread.authorize(credentials)

    spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1WIpKIdRy5y2OSoPtaGZXZKXyb2x3gs63LIWZWDQPjFE/edit?usp=sharing'

    doc = gc.open_by_url(spreadsheet_url)

    worksheet = doc.worksheet('문제목록')

    date = get_next_meeting_date()
    worksheet.append_row([date, username, site, url])  
       
def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead < 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

def get_next_meeting_date():
    weekday_dict = {0: '월', 1: "화", 2: "수", 3: "목", 4: "금", 5: "토", 6: "일"}
    today_date = datetime.datetime.today()
    today_weekday = datetime.datetime.today().weekday()
    register_hour = datetime.datetime.now().hour

    if 0 < today_weekday < 4:
        next_meeting = next_weekday(today_date, 4)
    
    elif 4 < today_weekday < 7:
        next_meeting = next_weekday(today_date, 0)
    
    elif today_weekday == 0 or today_weekday == 4:
        if register_hour < 21:
            next_meeting = datetime.datetime.today()
        else:
            if today_weekday == 0:
                next_meeting = next_weekday(today_date, 4)
            else:
                next_meeting = next_weekday(today_date, 0)
    
    return next_meeting.strftime("%Y-%m-%d" + "-" + weekday_dict[next_meeting.weekday()])



app.run(DISCORD_TOKEN)
