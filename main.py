import requests
from bs4 import BeautifulSoup
from astrbot import on_command

def get_flightsim_user_stats(username: str):
    url = f"https://zh.flightsim.to/profile/{username}"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        return None
    
    soup = BeautifulSoup(r.text, "html.parser")

    # 找到统计栏
    stats_div = soup.find("div", class_="flightsim-stats")
    if not stats_div:
        return None

    spans = stats_div.find_all("span")

    stats = {}
    # 按顺序读取
    # 0: Karma, 1: Uploads, 2: Downloads, 3: Followers, 4: Likes
    try:
        stats["karma"] = spans[0].strong.text.strip()
        stats["uploads"] = spans[1].strong.text.strip()
        stats["downloads"] = spans[2].strong.text.strip()
        stats["followers"] = spans[3].strong.text.strip()
        stats["likes"] = spans[4].strong.text.strip()
    except:
        return None

    return stats


@on_command("fs")
async def flightsim_user(session):
    args = session.current_arg_text.strip().split()
    if not args:
        await session.send("用法：/fs <用户名>")
        return
    
    username = args[0]
    stats = get_flightsim_user_stats(username)
    if not stats:
        await session.send(f"无法获取用户 {username} 的信息。")
        return

    msg = (
        f"📊 Flightsim.to 用户 {username} 数据：\n"
        f"🔥 Karma: {stats['karma']}\n"
        f"📦 上传数: {stats['uploads']}\n"
        f"⬇️ 下载量: {stats['downloads']}\n"
        f"👥 关注数: {stats['followers']}\n"
        f"👍 点赞数: {stats['likes']}"
    )
    await session.send(msg)

