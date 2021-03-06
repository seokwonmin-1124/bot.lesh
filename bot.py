#사용 시 출처를 남겨주세요
import asyncio
import discord
import sqlite3
import requests
import covid
from bs4 import BeautifulSoup
from discord.ext import commands
from keep_alive import keep_alive


intents = discord.Intents.default()
intents.members = True
game = discord.Activity(type=discord.ActivityType.watching, name=",도움말")
bot = commands.Bot(command_prefix=',', status=discord.Status.idle, activity=game, intents=intents)#봇이 하고있는 게임(~하는중), 상태 설정
bot.remove_command('help')

@bot.event 
async def on_ready():
    print("logged in as {0.user}".format(bot)) #봇이 로그인 하면 로그인 정보를 출력
"""    await bot.change_presence(status=discord.Status.online, activity=discord.Game("코로나 크롤링 기능 구현 완료"))"""

@bot.command(aliases=['시간표'])
async def siganpyo(ctx, period):

    if period == "1교시":
        await ctx.send("1교시는`9:10`에 시작합니다!")
    
    elif period == "2교시":
        await ctx.send("2교시는`10:05`에 시작합니다!")

    elif period == "3교시":
        await ctx.send("3교시는`11:00`에 시작합니다!")

    elif period == "4교시":
        await ctx.send("4교시는`11:55`에 시작합니다!")

    elif period == "점심시간":
        await ctx.send("점심시간은`01:50`까지입니다")
    
    elif period == "5교시":
        await ctx.send("5교시는`01:50`에 시작합니다!")

    elif period == "6교시":
        await ctx.send("6교시는`02:45`에 시작합니다!")

    elif period == "7교시":
        await ctx.send("7교시는`03:40`에 시작합니다!")

@siganpyo.error
async def period_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("1교시:`9:10`\n2교시:`10:05`\n3교시:`11:00`\n4교시:`11:55`\n점심시간:`01:50`\n5교시:`01:50`\n6교시:`02:45`\n7교시:`03:40`")


async def on_message(message):
    if message.author == bot.user: #봇이 보낸 메시지는 무시(유저만 받음)
        return

@bot.command(aliases=['메모'])
async def memo(ctx, *, sentence):

    option = sentence.split(" ")[0]
    memo = "".join(sentence[2:])
    user_id = str(ctx.author.id)

    if option == "생성":
        conn = sqlite3.connect('memo_main.db')
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS memo (user_id text PREMENT KEY, memo text)")
        cursor.execute(f"INSERT INTO memo VALUES('{user_id}', '{memo}')")
        conn.commit()
        conn.close()
        await ctx.send("메모가 저장되었습니다.")
    
    elif option == "불러오기":
        conn = sqlite3.connect('memo_main.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT memo FROM memo WHERE user_id = '{user_id}'")
        a = cursor.fetchone()
        await ctx.send(a[0])
        conn.close()
    
    elif option == "삭제":
        conn = sqlite3.connect('memo_main.db')
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM memo WHERE user_id = '{user_id}'")
        conn.commit()
        conn.close()
        await ctx.send("메모가 삭제되었습니다.")

    elif option == "수정":
        conn = sqlite3.connect('memo_main.db')
        cursor = conn.cursor()
        cursor.execute(f"UPDATE memo SET memo = '{memo}' WHERE user_id = '{user_id}'")
        conn.commit()
        conn.close()
        await ctx.send("메모가 수정되었습니다.")

@bot.command(aliases=['핑']) #ping
async def ping(ctx):
    await ctx.channel.send(f'`{bot.latency * 1000:.0f}ms`') #봇의 지연시간(핑)을 출력

@bot.command(aliases=['비웃어'])
async def scoff(ctx):
    await ctx.channel.send("`ㅋ`") #봇이 ㅋ을 출력

@bot.command(aliases=['비웃지마'])
async def dont_scoff(ctx):
    await ctx.channel.send("`넵`") #봇이 넵을 출력

@bot.command(aliases=['코로나']) #COVID file local import
async def covid19(ctx):
    embed=discord.Embed(title="코로나 확진자 정보", color=0x8ce137) #임베드 생성
    embed.set_thumbnail(url="https://yt3.ggpht.com/ytc/AKedOLRx1o4FfsK5isI9U-EHzAt7S57Knoyv7MoEIGKpGw=s900-c-k-c0x00ffffff-no-rj" ) #썸네일 설정
    embed.add_field(name="총 확진자", value=f'{covid.all}명{covid.today}', inline=True) #임베드에 필드 추가
    embed.add_field(name="총 사망자", value=f'{covid.die}명{covid.die_plus}', inline=True) #임베드에 필드 추가
    embed.set_footer(text=f'{covid.date}시 기준 확진자 정보입니다' ) #임베드에 푸터 추가
    await ctx.channel.send(embed=embed) #메시지 전송


@bot.command(aliases=['프로필']) #USER_PROFILE
async def userinfo(ctx, member: discord.Member=None):
    if member:
        #user_name = member.name
        user_server_name = member.display_name
        #user_tag = member.discriminator
        user_name_with_tag = member
        #user_id = member.id
        user_start_discord_date= member.created_at
        user_profile_img = member.avatar_url
        user_mention = member.mention

        await ctx.channel.send(f'bot.lesh가 알려주는 {user_mention} 님의 정보입니다!')
        embed=discord.Embed(title=f'{user_server_name}님의 정보', color=0x8ce137)
        embed.add_field(name='고유 이름', value=user_name_with_tag, inline=True)
        embed.add_field(name='서버 별명', value=user_server_name, inline=True)
        embed.add_field(name='디스코드를 시작한 날',  value=user_start_discord_date.strftime('%Y-%m-%d'), inline=True)
        embed.set_thumbnail(url=user_profile_img)
        embed.set_footer(text='.봇정보 으로 봇의 정보도 알아보세요' )
        await ctx.channel.send(embed=embed)

    else:
        #user_name = ctx.author.name
        user_server_name = ctx.author.display_name
        #user_tag = ctx.author.discriminator
        user_name_with_tag = ctx.author
        #user_id = ctx.author.id
        user_start_discord_date= ctx.author.created_at
        user_profile_img = ctx.author.avatar_url
        user_mention = ctx.author.mention

        await ctx.channel.send(f'bot.lesh가 알려주는 {user_mention} 님의 정보입니다!')
        embed=discord.Embed(title=f'{user_server_name}님의 정보', color=0x8ce137)
        embed.add_field(name='고유 이름', value=user_name_with_tag, inline=True)
        embed.add_field(name='서버 별명', value=user_server_name, inline=True)
        embed.add_field(name='디스코드를 시작한 날',  value=user_start_discord_date.strftime('%Y-%m-%d'), inline=True)
        embed.set_thumbnail(url=user_profile_img)
        embed.set_footer(text='.봇정보 으로 봇의 정보도 알아보세요' )
        await ctx.channel.send(embed=embed)

@userinfo.error
async def userinfo_error(ctx, error):
        embed = discord.Embed(title="잘못된 입력입니다.", description="역할의 정보는 가져올 수 없습니다.\n역할이 아닌 다른 에러라면 봇 개발자에게 캡쳐본과 함께 디엠을 남겨주세요", color=0xff0000)
        await ctx.send(embed=embed)

@bot.command(aliases=['봇정보']) #BOT_PROFILE
async def bot_info(ctx):
    embed=discord.Embed(title="봇 bot.lesh의 정보입니다!", color=0x8ce137)
    embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/lHib1cqwddASotFwfU3cxW6qDCQ2rKmX3GRjxwJj1zM/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/921288443869396992/f41655d1cbe05e9da2298bf3cead389f.webp" )
    embed.add_field(name="고유 이름", value="bot.lesh#1559", inline=True)
    embed.add_field(name="봇 제작자", value="LESH#3201", inline=True)
    embed.add_field(name="디스코드를 시작한 날", value="2021-12-18", inline=True)
    embed.set_footer(text=',프로필으로 자신의 정보도 알아보세요' )
    await ctx.channel.send(embed=embed)

@bot.command(aliases=['개발자정보']) #BOT_PROFILE
async def dev_info(ctx):
    embed=discord.Embed(title="개발자 LESH의 정보입니다!", color=0x8ce137)
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/758698615299506196/6b6f5041dbe78b2076a83e87ec9ea440.webp?size=1024" )
    embed.add_field(name="고유 이름", value="LESH#3201", inline=True)
    embed.add_field(name="개발한 봇", value="bot.lesh#1559", inline=True)
    embed.add_field(name="디스코드를 시작한 날", value="2020-09-24", inline=True)
    embed.set_footer(text=',프로필으로 자신의 정보도 알아보세요' )
    await ctx.channel.send(embed=embed)

@bot.command(aliases=['서버정보']) #BOT_PROFILE
async def server_info(ctx):
    await ctx.channel.send(f'{ctx.author.mention}님, {ctx.guild.name}서버의 정보입니다!')
    embed=discord.Embed(title=f"{ctx.guild.name}서버의 정보", color=0x8ce137)
    embed.set_thumbnail(url=f"{ctx.guild.icon_url}" )
    embed.add_field(name="서버 관리자", value=ctx.guild.owner, inline=True)
    embed.add_field(name="서버 인원", value=f"{ctx.guild.member_count}명", inline=True)
    embed.add_field(name="서버 개설 날짜", value=ctx.guild.created_at.strftime('%Y-%m-%d'), inline=True)
    embed.set_footer(text=',프로필으로 자신의 정보도 알아보세요' )
    await ctx.channel.send(embed=embed)


@bot.command(aliases=['hex'])
async def hex_code(ctx, hex_number_with_hashtag):
    hex_number = hex_number_with_hashtag[1:7]#hex_number_with_hashtag.replace('#', '')
    url = f"https://www.colorhexa.com/{hex_number}"
    hex_img = f"{url}.png"

    #만약 함수 {hex_code}의 길이가 6이라면 헥스 코드에 맞는 이미지를 출력하고 그렇지 않다면 에러를 출력한다
    if len(hex_number) == 6: #만약 함수 hex_number의 길이가 6이라면 아래 내용 실행/전송

        embed=discord.Embed(title=f'Hex code | {hex_number_with_hashtag}', color=0x8ce137)
        embed.add_field(name="설명", value=f'{hex_number_with_hashtag}에 해당하는 색상입니다', inline=False)
        embed.set_thumbnail(url=hex_img)
        embed.set_footer(text="image by colorhexa.com")
        await ctx.send(embed=embed)

    else: #아니라면 에러를 출력한다
        embed = discord.Embed(title="잘못된 입력입니다.", description="올바른 입력은 #으로 시작하는 6자리의 숫자 또는 문자 조합입니다.", color=0xff0000)
        await ctx.send(embed=embed)

@hex_code.error
async def hex_error(ctx, error):
    embed = discord.Embed(title="잘못된 입력입니다.", description="올바른 입력은 #으로 시작하는 6자리의 숫자 또는 문자 조합입니다.", color=0xff0000)
    await ctx.send(embed=embed)

@bot.command(aliases=['도움말']) #도움말
async def help(ctx, help_opt):

    if help_opt == "코로나":
        embed=discord.Embed(title="명령어 코로나의 도움말 입니다.", color=0x8ce137)
        embed.add_field(name="명령어 설명", value="`,코로나`를 입력하면 코로나 정보를 알려드립니다.", inline=False)
        embed.set_footer(text="bot.lesh 도움말 코로나")
        await ctx.channel.send(embed=embed)

    elif help_opt == "프로필":
        embed=discord.Embed(title="명령어 프로필의 도움말 입니다.", color=0x8ce137)
        embed.add_field(name="명령어 설명", value="`,프로필 <멘션>`를 입력하면 태그한 유저의 정보를 알려줍니다.\n`,프로필`만 입력하시면 메시지를 보낸 유저의 정보를 알려줍니다", inline=False)
        embed.set_footer(text="bot.lesh 도움말 내정보")
        await ctx.channel.send(embed=embed)

    elif help_opt == "봇정보":
        embed=discord.Embed(title="명령어 봇정보의 도움말 입니다.", color=0x8ce137)
        embed.add_field(name="명령어 설명", value="`,봇 정보`를 입력하면 bot.lesh의 정보를 알려줍니다.", inline=False)
        embed.set_footer(text="bot.lesh 도움말 봇정보")
        await ctx.channel.send(embed=embed)

    elif help_opt == "개발자정보":
        embed=discord.Embed(title="명령어 개발자정보의 도움말 입니다.", color=0x8ce137)
        embed.add_field(name="명령어 설명", value="`,개발자 정보`를 입력하면 bot.lesh를 개발한 개발자의 정보를 알려줍니다.", inline=False)
        embed.set_footer(text="bot.lesh 도움말 개발자정보")
        await ctx.channel.send(embed=embed)

    elif help_opt == "서버정보":
        embed=discord.Embed(title="명령어 서버정보의 도움말 입니다.", color=0x8ce137)
        embed.add_field(name="명령어 설명", value="`,서버정보`를 입력하면 메시지를 보낸 유저가 있는 서버의 정보를 알려줍니다.", inline=False)
        embed.set_footer(text="bot.lesh 도움말 서버정보")
        await ctx.channel.send(embed=embed)

    elif help_opt == "hex":
        embed=discord.Embed(title="명령어 hex의 도움말 입니다.", color=0x8ce137)
        embed.add_field(name="명령어 설명", value="`,hex <hex code>`를 입력하면 그에 맞는 색상을 알려드립니다.", inline=False)
        embed.set_footer(text="bot.lesh 도움말 코로나")
        await ctx.channel.send(embed=embed)

    elif help_opt == "메모":
        embed=discord.Embed(title="명령어 메모의 도움말 입니다.", color=0x8ce137)
        embed.add_field(name="명령어 설명", value="`,메모 <옵션>`을 입력하면 메모를 작성 해 줍니다.\n옵션: 생성, 불러오기, 수정, 삭제", inline=False)
        embed.set_footer(text="bot.lesh 도움말 내정보")
        await ctx.channel.send(embed=embed)

    elif help_opt == "도움말":
        embed=discord.Embed(title="명령어 도움말의 도움말 입니다.", color=0x8ce137)
        embed.add_field(name="명령어 설명", value="`,도움말`를 입력하면 레쉬봇이 실행할 수 있는 명령어를 알려드립니다.", inline=False)
        embed.set_footer(text="bot.lesh 도움말 도움말")
        await ctx.channel.send(embed=embed)

    elif help_opt == "초대":
        embed=discord.Embed(title="명령어 초대의 도움말 입니다.", color=0x8ce137)
        embed.add_field(name="명령어 설명", value="`,초대`를 입력하면 초대 링크를 알려드립니다.", inline=False)
        embed.set_footer(text="bot.lesh 도움말 초대")
        await ctx.channel.send(embed=embed)

    elif help_opt == "비웃어":
        embed=discord.Embed(title="명령어 비웃어의 도움말 입니다.", color=0x8ce137)
        embed.add_field(name="명령어 설명", value="`,비웃어`를 입력하면 레쉬봇이 대신 비웃어드립니다.\n\
            LESH가 개발한 봇에겐 꼭 들어가는 필수 기능입니다.", inline=False)
        embed.set_footer(text="bot.lesh 도움말 비웃어")
        await ctx.channel.send(embed=embed)

    elif help_opt == "핑":
        embed=discord.Embed(title="명령어 핑의 도움말 입니다.", color=0x8ce137)
        embed.add_field(name="명령어 설명", value="`,핑`를 입력하면 봇의 지연 시간을 알려드립니다.", inline=False)
        embed.set_footer(text="bot.lesh 도움말 핑")
        await ctx.channel.send(embed=embed)

    elif help_opt == "타이머":
        embed=discord.Embed(title="명령어 타이머의 도움말 입니다.", color=0x8ce137)
        embed.add_field(name="명령어 설명", value="`,타이머 <초>`를 입력하면 입력하신 초만큼 타이머를 맞춰줍니다.\n(최대 5분)", inline=False)
        embed.set_footer(text="bot.lesh 도움말 타이머")
        await ctx.channel.send(embed=embed)

    else:
        embed = discord.Embed(title="잘못된 입력입니다.", description="도움말 목록을 다시 확인하세요", color=0xff0000)
        await ctx.send(embed=embed)

@help.error #기존 도움말은 help_opt 값을 입력받지 않은 .도움말 형식이어야 함 도움말 설명을 넣으며 help_opt이 비었을 때의 에러를 기존 도움말로 변경
async def hlep_error(ctx, error):
    embed=discord.Embed(title="bot.lesh의 도움말 입니다", color=0x8ce137)
    embed.add_field(name="명령어 설명", value="`,도움말 <명령어>`으로 명령어에 대해 더 자세하게 알아보세요", inline=False)
    embed.add_field(name="명령어", value="`,도움말`, `,코로나`, `,hex`, `,메모`, `,타이머`\n`,프로필`, `,개발자정보`, `,봇정보`, `,서버정보`\n`,초대`, `,비웃어`, `,핑`, `디데이,일정(개발중)`", inline=False)
    embed.set_footer(text="bot.lesh 도움말")
    await ctx.channel.send(embed=embed)

@bot.command(aliases=['초대'])
async def invite(ctx):
    embed=discord.Embed(title="bot.lesh를 서버에 초대하세요!", color=0x8ce137)
    embed.add_field(name="링크입니다", value="[지금 바로 초대하세요](https://discord.com/api/oauth2/authorize?client_id=921288443869396992&permissions=8&scope=bot)")
    await ctx.send(embed=embed)

@bot.command(aliases=['타이머'])
#임베드로 ~초 남았습니다를 표시하고 1초가 지날때마다 임베드를 수정해서 출력
async def timer(ctx, times: int):
    if times <= 300:
        embed = discord.Embed(title='타이머', description='타이머 시작합니다.', color=0x00ff00)
        embed.set_footer(text=f'{ctx.author.display_name}님이 시작한 {times}s 타이머')
        msg = await ctx.send(embed=embed)
        while times > 0:
            embed.description = f'`{times//60}분 {times%60}초` 남았습니다.'
            await asyncio.sleep(1)
            await msg.edit(embed=embed)
            times -= 1
        embed.description = '시간이 종료되었습니다.'
        await msg.edit(embed=embed)

    else:
        embed = discord.Embed(title="잘못된 입력입니다.", description="타이머는 5분(300초) 까지 가능합니다.", color=0xff0000)
        await ctx.send(embed=embed)

@timer.error
async def timer_error(ctx, error):
    embed = discord.Embed(title='시간 목록', color=0x00ff00)
    embed.add_field(name='분->시간', value='```1분:60초\n2분:120초\n3분:180초\n4분:240초\n5분:300초```형식은 `,타이머 <초>` 입니다.\nex: `,타이머 300` ->5분 예약', inline=False)
    await ctx.send(embed=embed)

keep_alive()
bot.run('토큰입력하세요') #봇이 실행되면 토큰 파일을 읽어서 봇이 로그인함
