import discord
import yfinance as yf
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

CHANNEL_ID = 1354818507975430408
TICKER = "005930.KS"
TARGET_PRICE = 72000

intents = discord.Intents.default()
client = discord.Client(intents=intents)

last_sent_price = None  # 마지막으로 보낸 가격 저장용

@client.event
async def on_ready():
    print(f'봇 로그인 완료: {client.user}')
    guild = client.guilds[0]
    channel = discord.utils.get(guild.text_channels, id=CHANNEL_ID)

    if channel is None:
        print("❌ 채널을 찾을 수 없습니다!")
        return

    async def check_stock():
        global last_sent_price
        while True:
            stock = yf.Ticker(TICKER)
            try:
                price = stock.history(period="5d")["Close"].dropna().iloc[-1]
                print(f"현재 가격: {price}")
                if price <= TARGET_PRICE and price != last_sent_price:
                    await channel.send(f"📉 삼성전자 주가가 {price}원으로 하락했어요!")
                    last_sent_price = price
            except Exception as e:
                print(f"에러 발생: {e}")

            await asyncio.sleep(60)

    client.loop.create_task(check_stock())

client.run(TOKEN)