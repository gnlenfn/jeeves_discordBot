import discord
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
from dotenv import load_dotenv
import os

load_dotenv(verbose=True,
            dotenv_path='../.env')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

app = commands.Bot(command_prefix='!')
   
@app.event
async def on_ready():
    print('다음으로 로그인합니다: ')
    print(app.user.name)
    print('connection was succesful')
    await app.change_presence(status=discord.Status.online, activity=None)

@app.command(name='문제추가')
async def add_list(ctx, *args):
    site, url = args[0], args[1]
    username = ctx.author.nick
    if not username:
        username = ctx.author.name

    wirte_ps_list(username, site, url)
    await ctx.send("문제 등록 완료")
    return username, site, url

@app.command(name="문제목록")
async def print_url(ctx):
    await ctx.send("구글스프레드시트:\nhttp://t2m.kr/JeXvW")


def wirte_ps_list(username, site, url):
    scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
    ]

    json_file_name = './rapid-bricolage-304806-3e0bcf6ba899.json'
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
