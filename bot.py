import discord
from discord.ext import tasks, commands
import feedparser

# 初始化 Bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# 設定 RSS 來源與 Discord 頻道 ID
RSS_URL = "https://wololo.net/feed/"
CHANNEL_ID = 123456789012345678  # 替換為你的 Discord 頻道 ID
last_title = ""

@bot.event
async def on_ready():
    print(f"機器人已上線：{bot.user.name}")
    check_ps5_news.start() # 啟動背景定時任務

@tasks.loop(minutes=30) # 每 30 分鐘檢查一次
async def check_ps5_news():
    global last_title
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        return

    feed = feedparser.parse(RSS_URL)
    if feed.entries:
        latest_entry = feed.entries[0]
        
        # 篩選標題包含 PS5 的文章，且避免重複發送
        if "PS5" in latest_entry.title and latest_entry.title != last_title:
            last_title = latest_entry.title
            
            # 建立 Discord 卡片訊息 (Embed)
            embed = discord.Embed(
                title=latest_entry.title,
                url=latest_entry.link,
                description=latest_entry.summary[:200] + "...",
                color=0x0070D1 # PS 經典藍
            )
            embed.set_footer(text="來源：Wololo.net")
            
            await channel.send(content="📢 **發現最新 PS5 破解情報！**", embed=embed)

# 手動查詢指令
@bot.command()
async def ps5news(ctx):
    feed = feedparser.parse(RSS_URL)
    ps5_posts = [entry for entry in feed.entries if "PS5" in entry.title][:3]
    
    if not ps5_posts:
        await ctx.send("目前沒有最新的 PS5 相關新聞。")
        return

    for entry in ps5_posts:
        embed = discord.Embed(title=entry.title, url=entry.link, color=0x0070D1)
        await ctx.send(embed=embed)

bot.run("YOUR_DISCORD_BOT_TOKEN")