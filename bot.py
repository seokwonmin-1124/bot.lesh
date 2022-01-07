#--------update log--------#
#LESH_21.12.18_코로나 크롤링 기능 구현 완료
#LESH_22.01.01_사용자 프로필 기능 구현 완료
#LESH_22.01.02_HEX 코드 뷰어 가눙 구현 완료
#사용 시 출처를 남겨주세요
#-------모듈 import--------#
import discord
from bs4 import BeautifulSoup
import requests
from discord.ext import commands

#--------봇 상태 설정--------#
game = discord.Game(".도움말")
bot = commands.Bot(command_prefix='.', status=discord.Status.idle, activity=game)#봇이 하고있는 게임(~하는중), 상태 설정

#--------초기세팅--------#
@bot.event 
async def on_ready():
    print("logged in as {0.user}".format(bot)) #봇이 로그인 하면 로그인 정보를 출력

async def on_message(message):
    if message.author == bot.user: #봇이 보낸 메시지는 무시(유저만 받음)
        return

@bot.command() #ping
async def 핑(ctx):
    await ctx.channel.send(f'`{bot.latency * 1000:.0f}ms`') #봇의 지연시간(핑)을 출력

@bot.command()
async def 비웃어(ctx):
    await ctx.channel.send("`ㅋ`") #봇이 ㅋ을 출력

#--------메인기능들--------#
#----코로나 함수----#
url = 'http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=13&ncvContSeq=&contSeq=&board_id=&gubun=' #이 링크에서 크롤링
res = requests.get(url)
res.raise_for_status()

soup = BeautifulSoup(res.text, 'lxml')
covid19_all = soup.select_one('#content > div > div.data_table.midd.mgt24 > table > tbody > tr.sumline > td:nth-child(5)').text #전체 확진자 수
covid19_today = soup.select_one('#mapAll > div > ul > li:nth-child(6) > div:nth-child(2) > span').text #오늘 확진자 수
covid19_die = soup.select_one('#mapAll > div > ul > li:nth-child(1) > div:nth-child(2) > span').text #사망자 수
covid19_die_plus = soup.select_one('#mapAll > div > ul > li:nth-child(2) > div:nth-child(2) > span').text #전일대비 사망자 증가율
covid19_date = soup.select_one('#content > div > div.timetable > p > span').text #최종 갱신일
#covid19_date = covid19_date.replace('.', '-') #최종 갱신일에서 .을 -로 바꿈

@bot.command() #COVID19
async def 코로나(ctx):
    embed=discord.Embed(title="코로나 확진자 정보", color=0x8ce137) #임베드 생성
    embed.set_thumbnail(url="https://yt3.ggpht.com/ytc/AKedOLRx1o4FfsK5isI9U-EHzAt7S57Knoyv7MoEIGKpGw=s900-c-k-c0x00ffffff-no-rj" ) #썸네일 설정
    embed.add_field(name="총 확진자", value=f'{covid19_all}명{covid19_today}', inline=True) #임베드에 필드 추가
    embed.add_field(name="총 사망자", value=f'{covid19_die}명{covid19_die_plus}', inline=True) #임베드에 필드 추가
    embed.set_footer(text=f'{covid19_date}시 기준 확진자 정보입니다' ) #임베드에 푸터 추가
    await ctx.channel.send(embed=embed) #메시지 전송


@bot.command() #USER_PROFILE
async def 내정보(ctx):
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

@bot.command()
async def hex(ctx, hex_number_with_hashtag):
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
        
    else: #그렇지 않다면 에러 임베드 전송

        embed = discord.Embed(title="잘못된 입력입니다.", description="올바른 입력은 #으로 시작하는 6자리의 숫자 또는 문자 조합입니다.", color=0xff0000)
        await ctx.send(embed=embed)

@bot.command() #도움말
async def 도움말(ctx):
    embed=discord.Embed(title="bot.lesh의 도움말 입니다", color=0x8ce137)
    embed.add_field(name="메인 명령어", value="`.도움말`: bot.lesh의 도움말을 알려줍니다.\n`.코로나`: 하루마다 업데이트 되는 코로나 확진자 수를 알려줍니다\n`.내정보`: 내 서버별명, 고유이름, 디스코드를 시작한 날짜, 프로필 사진 등을 알려줍니다.\n`.hex #(hex_code)`: hex 코드를 이미지로 보여줍니다.\n", inline=False)
    embed.add_field(name="잡기능들", value="`.비웃어`: 봇이 `ㅋ`하고 비웃어 줍니다.\n`.핑`:핑 상태를 알려줍니다", inline=False)
    embed.add_field(name="봇 초대 방법", value="`.초대` 를 이용하여 봇을 초대해 보세요!\n 봇 인스타그램에도 초대 주소가 있습니다`instagram`:bot.lesh", inline=False)
    embed.add_field(name="개발자 정보", value="07년생 중등 개발자 입니다.\n`Didcord`:LESH#3201\n`Blog`: blog.naver.com/seokwonmin\n`instagram`: LESH_1124", inline=False)
    embed.set_footer(text="bot.lesh")
    await ctx.channel.send(embed=embed)

@bot.command()
async def 초대(ctx):
    embeds = discord.Embed(title="bot.lesh를 서버에 초대하세요!", color=0x8ce137)
    embeds.add_field(name="링크입니다", value="[지금 바로 초대하세요](https://discord.com/api/oauth2/authorize?client_id=921288443869396992&permissions=380104624192&scope=bot)")
    await ctx.send(embed=embeds)

#--------토큰--------#
bot.run(InputYourBotToken) #봇이 실행되면 토큰 파일을 읽어서 봇이 로그인함
