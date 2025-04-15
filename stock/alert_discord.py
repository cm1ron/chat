import discord
import yfinance as yf
import asyncio
from dotenv import load_dotenv
import os
import sys
import atexit
import tempfile

LOCK_FILE = os.path.join(tempfile.gettempdir(), "alert_discord.lock")

def already_running():
    if os.path.exists(LOCK_FILE):
        return True
    with open(LOCK_FILE, "w") as f:
        f.write("running")
    return False

def remove_lock_file():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

if already_running():
    print("이미 실행 중입니다.")
    sys.exit()

atexit.register(remove_lock_file)


# ===== 디스코드 봇 설정 =====
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

CHANNEL_ID = 1361577299861835801  # 디스코드 채널 ID
TICKER = "005930.KS"              # 종목 코드
TARGET_PRICE = 60000              # 목표 가격

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'봇 로그인 완료: {client.user}')
    guild = client.guilds[0]
    channel = discord.utils.get(guild.text_channels, id=CHANNEL_ID)

    if channel is None:
        print("❌ 채널을 찾을 수 없습니다!")
        return

    async def check_stock():
        while True:
            stock = yf.Ticker(TICKER)
            try:
                price = stock.history(period="5d")["Close"].dropna().iloc[-1]
                print(f"현재 가격: {price}")
                if price <= TARGET_PRICE:
                    await channel.send(f"📉 삼성전자 주가가 {price}원으로 하락했어요!")
            except Exception as e:
                print(f"에러 발생: {e}")

            await asyncio.sleep(60)  # 60초마다 확인

    client.loop.create_task(check_stock())

client.run(TOKEN)
