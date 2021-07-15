import discord
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials

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

    json_file_name = 'rapid-bricolage-304806-3e0bcf6ba899.json'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
    gc = gspread.authorize(credentials)

    spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1WIpKIdRy5y2OSoPtaGZXZKXyb2x3gs63LIWZWDQPjFE/edit?usp=sharing'

    doc = gc.open_by_url(spreadsheet_url)

    worksheet = doc.worksheet('문제목록')

    worksheet.append_row([username, site, url])  
       
app.run('Nzg3MzQwNDk1NDExODcxNzU0.X9Th-g.mKeM2pvOF2MPgjY7Htrn6sxS4FU')