#LESH_21.12.18_코로나 크롤링 기능 구현 완료
#LESH_22.01.01_사용자 프로필 기능 구현 완료
#사용 시 출처를 남겨주세요
import discord
from bs4 import BeautifulSoup
import requests
from keep_alive import keep_alive

#봇이 하고있는 게임, 상태 설정
game = discord.Game("LESH와 개발놀이")
client = discord.Client(status=discord.Status.idle, activity=game)

#코로나 19 웹 크롤링 함수들
url = 'http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=13&ncvContSeq=&contSeq=&board_id=&gubun=' #이 링크에서 크롤링
res = requests.get(url)
res.raise_for_status()

soup = BeautifulSoup(res.text, 'lxml')
covid19_all = soup.select_one('#content > div > div.data_table.midd.mgt24 > table > tbody > tr.sumline > td:nth-child(5)').text #전체 확진자 수
covid19_today = soup.select_one('#mapAll > div > ul > li:nth-child(6) > div:nth-child(2) > span').text #오늘 확진자 수
covid19_die = soup.select_one('#mapAll > div > ul > li:nth-child(1) > div:nth-child(2) > span').text #사망자 수
covid19_die_plus = soup.select_one('#mapAll > div > ul > li:nth-child(2) > div:nth-child(2) > span').text #전일대비 사망자 증가율
covid19_date = soup.select_one('#content > div > div.timetable > p > span').text #최종 갱신일

#봇이 보낼 메시지들
@client.event 
async def on_ready():
    print("logged in as {0.user}".format(client)) #봇이 로그인 하면 로그인 정보를 출력

@client.event
async def on_message(message):
    if message.author == client.user: #봇이 보낸 메시지는 무시(유저만 받음)
        return

    if message.content.startswith('.코로나'): #봇이 받은 메시지가 .코로나로 시작하면
        embed=discord.Embed(title="코로나 확진자 정보", color=0x8ce137) #임베드 에브리드 생성
        embed.set_thumbnail(url="https://yt3.ggpht.com/ytc/AKedOLRx1o4FfsK5isI9U-EHzAt7S57Knoyv7MoEIGKpGw=s900-c-k-c0x00ffffff-no-rj" ) #썸네일 설정
        embed.add_field(name="총 확진자", value=f'{covid19_all}명{covid19_today}', inline=True) #임베드에 필드 추가
        embed.add_field(name="총 사망자", value=f'{covid19_die}명{covid19_die_plus}', inline=True) #임베드에 필드 추가
        embed.set_footer(text=f'{covid19_date}시 기준 확진자 정보입니다' ) #임베드에 푸터 추가
        await message.channel.send(embed=embed) #메시지 전송
    
    if message.content.startswith('.내정보'):
        #user_name = message.author.name
        user_server_name = message.author.display_name
        #user_tag = message.author.discriminator
        user_name_with_tag = message.author
        #user_id = message.author.id
        user_start_discord_date= message.author.created_at
        user_profile_img = message.author.avatar_url
        user_mention = message.author.mention

        await message.channel.send(f'bot.lesh가 알려주는 {user_mention} 님의 정보입니다!')
        embed=discord.Embed(title=f'{user_server_name}님의 정보', color=0x8ce137)
        embed.add_field(name='고유 이름', value=user_name_with_tag, inline=True)
        embed.add_field(name='서버 별명', value=user_server_name, inline=True)
        embed.add_field(name='디스코드를 시작한 날',  value=user_start_discord_date.strftime('%Y-%m-%d'), inline=True)
        embed.set_thumbnail(url=user_profile_img)
        embed.set_footer(text='.봇정보 으로 봇의 정보도 알아보세요' )
        await message.channel.send(embed=embed)

    if message.content.startswith('.핑'): #봇이 받은 메시지가 .핑으로 시작하면
        await message.channel.send(f'`{client.latency * 1000:.0f}ms`') #봇의 지연시간(핑)을 출력
    
    if message.content.startswith(".비웃어"): #봇이 받은 메시지가 .비웃어로 시작하면
        await message.channel.send("`ㅋ`") #봇이 ㅋ을 출력

    

keep_alive()
client.run('토큰입력') #봇이 실행되면 토큰 파일을 읽어서 봇이 로그인함

