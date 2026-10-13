# ═══════════════════════════════════════════════════════════
#  THE VOID TCP BOT — single file
#  telegram frontend + free fire tcp engine
#  dev : VOID · @voidisking
# ═══════════════════════════════════════════════════════════

import os, sys, json, time, random, asyncio, logging
import ssl, struct, hashlib, binascii, base64, re, threading
import requests, aiohttp, urllib3
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

import jwt, pytz, psutil
from cfonts import render, say
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from google.protobuf.timestamp_pb2 import Timestamp
from protobuf_decoder.protobuf_decoder import Parser

from telegram import Update, BotCommand
from telegram.constants import ParseMode
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, ContextTypes,
)

from Pb2 import (
    DEcwHisPErMsG_pb2, MajoRLoGinrEs_pb2, PorTs_pb2,
    MajoRLoGinrEq_pb2, sQ_pb2, Team_msg_pb2, GenWhisperMsg_pb2, Fo_pb2,
)
import RemoveFriend_Req_pb2
from byte import Encrypt_ID, encrypt_api

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ═══════════════════════════════════════════════════════════
#  CONFIG
# ═══════════════════════════════════════════════════════════

BOT_TOKEN  = os.getenv("BOT_TOKEN", "").strip()
VOID_UID   = os.getenv("VOID_UID", "").strip()
VOID_PASS  = os.getenv("VOID_PASS", "").strip()
ADMIN_UID  = int(os.getenv("ADMIN_UID", "0"))

BOT_NAME   = "ᴛʜᴇ ᴠᴏɪᴅ ᴛᴄᴘ ʙᴏᴛ"
SUPPORT_1  = "@voidisking"
SUPPORT_2  = "@lordofzone"
CHANNEL    = "https://t.me/kingvoidofficial"
GROUP      = "https://t.me/voidofficialgc"

if not BOT_TOKEN:               raise SystemExit("BOT_TOKEN missing")
if not VOID_UID or not VOID_PASS: raise SystemExit("VOID_UID / VOID_PASS missing")
if ADMIN_UID == 0:              raise SystemExit("ADMIN_UID missing")

logging.basicConfig(
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)
log = logging.getLogger("void")

# ═══════════════════════════════════════════════════════════
#  GLOBAL STATE
# ═══════════════════════════════════════════════════════════

online_writer  = None
whisper_writer = None
bot_uid        = None
key_global     = None
iv_global      = None
region         = None
ToKen          = None

spam_room      = False
spammer_uid    = None
spam_chat_id   = None
spam_uid       = None
Spy            = False
Chat_Leave     = False

evo_cycle_running = False
evo_cycle_task    = None
EVO_IDS = [
    909000063, 909000075, 909040010, 909000081, 909039011,
    909045001, 909038012, 909042008, 909051003, 909035012,
    909000098, 909033002, 909037011, 909049010, 909041005,
    909038010, 909033001, 909035007, 909000090, 909000085,
    909000068,
]

spam_targets  = set()
spm_tasks     = {}
spam_task     = None
spam_running  = False
SPAM_INTERVAL = 0.5

pending_ghost_future = None
ghost_team_id        = None
ghost_squad_code     = None

ban_task    = None
ban_running = False
ban_targets = set()

admin_uid = str(ADMIN_UID)

Hr = {
    "User-Agent": "UnityPlayer/2018.4.12f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)",
    "Accept": "*/*",
    "Accept-Encoding": "deflate, gzip",
    "X-Ga-Sv": "1789534056",
    "Authorization": "Bearer",
    "X-Ga": "v1 1",
    "Releaseversion": "OB55",
    "Content-Type": "application/x-www-form-urlencoded",
    "X-Unity-Version": "2018.4.12f1",
}

# ═══════════════════════════════════════════════════════════
#  ═══ PASTE HERE : xC4.py contents ═══
#  copy the entire body of xC4.py (everything after its import block)
#  into this exact spot.
# ═══════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════
#  ═══ PASTE HERE : xP.py contents ═══
#  copy the entire body of xP.py (everything after its import block).
# ═══════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════
#  ═══ PASTE HERE : xHeaders.py contents ═══
#  copy the entire body of xHeaders.py (everything after its import block).
# ═══════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════
#  ═══ PASTE HERE : main.py helper funcs ═══
#  copy everything from your original main.py BETWEEN the constants
#  block and the bottom `if __name__ == '__main__':` block.
#
#  THEN apply these edits:
#    1. inside MaiiiinE(), replace:
#           Uid, Pw = 'ADD_YOUR_UID', 'ADD_YOUR_PASS'
#       with:
#           Uid, Pw = VOID_UID, VOID_PASS
#
#    2. inside MaiiiinE(), right after `iv = MajoRLoGinauTh.iv`, add:
#           global key_global, iv_global
#           key_global = key
#           iv_global  = iv
#
#    3. inside TcPChaT(), DELETE the entire `if inPuTMsG.startswith(...)`
#       chain. KEEP whisper parsing, auto-accept, kick detection,
#       .ready / .unready.
#
#    4. do NOT paste the `if __name__ == '__main__':` block.
# ═══════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════
#  PUBLIC API — telegram handlers call these
# ═══════════════════════════════════════════════════════════

def engine_alive() -> bool:
    return whisper_writer is not None and online_writer is not None

async def cmd_team(size: int):
    if not engine_alive(): return False, "ᴇɴɢɪɴᴇ ᴏꜰꜰʟɪɴᴇ"
    try:
        PAc = await OpEnSq(key_global, iv_global, region)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
        await asyncio.sleep(0.5)
        C = await cHSq(size, bot_uid, key_global, iv_global, region)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', C)
        await asyncio.sleep(0.5)
        V = await SEnd_InV(size, bot_uid, key_global, iv_global, region)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', V)
        await asyncio.sleep(3.5)
        E = await ExiT(None, key_global, iv_global)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', E)
        return True, f"ᴛᴇᴀᴍ {size} ᴅᴏɴᴇ"
    except Exception as e:
        return False, f"ᴇʀʀᴏʀ: {e}"

async def cmd_join(code: str):
    if not engine_alive(): return False, "ᴇɴɢɪɴᴇ ᴏꜰꜰʟɪɴᴇ"
    try:
        EM = await JoinSq_original(code, key_global, iv_global)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', EM)
        return True, f"ᴊᴏɪɴᴇᴅ {code}"
    except Exception as e:
        return False, f"ᴇʀʀᴏʀ: {e}"

async def cmd_ghost(code: str, name: str):
    if not engine_alive(): return False, "ᴇɴɢɪɴᴇ ᴏꜰꜰʟɪɴᴇ"
    try:
        tid, scode = await get_squad_info(code, key_global, iv_global)
        if not tid: return False, "ɴᴏ ʀᴇsᴘᴏɴsᴇ ꜰʀᴏᴍ sǫᴜᴀᴅ"
        ex = await ExiT(None, key_global, iv_global)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', ex)
        await asyncio.sleep(0.2)
        for _ in range(4):
            gp = await GhostPakcet(tid, name, scode, key_global, iv_global)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', gp)
            await asyncio.sleep(0.1)
        return True, f"ɢʜᴏsᴛs sᴇɴᴛ ᴛᴏ {code} ᴀs {name}"
    except Exception as e:
        return False, f"ᴇʀʀᴏʀ: {e}"

async def cmd_lag(code: str, count: int = 30):
    if not engine_alive(): return False, "ᴇɴɢɪɴᴇ ᴏꜰꜰʟɪɴᴇ"
    try:
        for _ in range(count):
            jp = await JoinSq_original(code, key_global, iv_global)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', jp)
            await asyncio.sleep(0.3)
            lp = await xSKINZxLag(key_global, iv_global)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', lp)
            await asyncio.sleep(0.2)
            ex = await ExiT(None, key_global, iv_global)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', ex)
            await asyncio.sleep(0.2)
        return True, f"ʟᴀɢ x{count} ᴅᴏɴᴇ"
    except Exception as e:
        return False, f"ᴇʀʀᴏʀ: {e}"

async def cmd_spam_msg(code: str, text: str, count: int = 30):
    if not engine_alive(): return False, "ᴇɴɢɪɴᴇ ᴏꜰꜰʟɪɴᴇ"
    try:
        jp = await GenJoinSquadsPacket(code, key_global, iv_global)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', jp)
        await asyncio.sleep(1.5)
        for _ in range(count):
            mp = await SEndMsG(0, f"[b][c]{get_random_color()}{text}",
                               bot_uid, code, key_global, iv_global)
            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', mp)
            await asyncio.sleep(0.3)
        ex = await ExiT(None, key_global, iv_global)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', ex)
        return True, f"sᴇɴᴛ x{count} ᴍsɢs ᴛᴏ {code}"
    except Exception as e:
        return False, f"ᴇʀʀᴏʀ: {e}"

async def cmd_ban(uid: str):
    if not engine_alive(): return False, "ᴇɴɢɪɴᴇ ᴏꜰꜰʟɪɴᴇ"
    try:
        p = await xBaNchaTxSkInZ(uid, key_global, iv_global)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', p)
        return True, f"ʙᴀɴ sᴇɴᴛ ᴛᴏ {uid}"
    except Exception as e:
        return False, f"ᴇʀʀᴏʀ: {e}"

async def cmd_info(uid: str):
    try:
        ok, d = await get_player_info(uid)
        if ok:
            m1, m2, m3 = format_player_info(d)
            return True, f"{m1}\n{m2}\n{m3}"
        return False, f"ꜰᴀɪʟ: {d}"
    except Exception as e:
        return False, f"ᴇʀʀᴏʀ: {e}"

async def cmd_check(uid: str):
    try:
        ok, d = await check_banned(uid)
        if ok: return True, format_check_result(d)
        return False, f"ꜰᴀɪʟ: {d}"
    except Exception as e:
        return False, f"ᴇʀʀᴏʀ: {e}"

async def cmd_spm(uid: str):
    if not engine_alive(): return False, "ᴇɴɢɪɴᴇ ᴏꜰꜰʟɪɴᴇ"
    global spam_targets, spm_tasks
    if uid in spm_tasks:
        spm_tasks[uid].cancel(); del spm_tasks[uid]
    spam_targets.add(uid)
    spm_tasks[uid] = asyncio.create_task(spm_loop(uid, key_global, iv_global))
    return True, f"sᴘᴀᴍ sᴛᴀʀᴛᴇᴅ {uid}"

async def cmd_stp(uid: str):
    global spam_targets, spm_tasks
    if uid in spm_tasks:
        spm_tasks[uid].cancel(); del spm_tasks[uid]
        spam_targets.discard(uid)
        return True, f"sᴘᴀᴍ sᴛᴏᴘᴘᴇᴅ {uid}"
    return False, "ɴᴏ ᴀᴄᴛɪᴠᴇ sᴘᴀᴍ"

async def cmd_exit():
    if not engine_alive(): return False, "ᴇɴɢɪɴᴇ ᴏꜰꜰʟɪɴᴇ"
    try:
        ex = await ExiT(bot_uid, key_global, iv_global)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', ex)
        return True, "ʟᴇꜰᴛ sǫᴜᴀᴅ"
    except Exception as e:
        return False, f"ᴇʀʀᴏʀ: {e}"

async def cmd_add(uid: str):
    try:
        return await send_friend_request(uid, ToKen, region)
    except Exception as e:
        return False, f"ᴇʀʀᴏʀ: {e}"

async def cmd_remove(uid: str):
    try:
        return await remove_friend(uid, ToKen, region)
    except Exception as e:
        return False, f"ᴇʀʀᴏʀ: {e}"

async def cmd_evos(uids):
    global evo_cycle_running, evo_cycle_task
    if evo_cycle_task and not evo_cycle_task.done():
        evo_cycle_running = False
        evo_cycle_task.cancel()
        await asyncio.sleep(0.5)
    evo_cycle_running = True
    evo_cycle_task = asyncio.create_task(
        evo_gun_cycle(uids, EVO_IDS, key_global, iv_global, region))
    return True, "ᴇᴠᴏ ᴄʏᴄʟᴇ sᴛᴀʀᴛᴇᴅ"

async def cmd_sevos():
    global evo_cycle_running, evo_cycle_task
    if evo_cycle_task and not evo_cycle_task.done():
        evo_cycle_running = False
        evo_cycle_task.cancel()
        return True, "ᴇᴠᴏ ᴄʏᴄʟᴇ sᴛᴏᴘᴘᴇᴅ"
    return False, "ɴᴏ ᴀᴄᴛɪᴠᴇ ᴄʏᴄʟᴇ"

async def engine_loop():
    while True:
        try:
            await asyncio.wait_for(MaiiiinE(), timeout=7 * 60 * 60)
        except asyncio.TimeoutError:
            log.warning("[engine] token expired · restarting")
        except Exception as e:
            log.exception(f"[engine] crash · restarting · {e}")
        await asyncio.sleep(2)

# ═══════════════════════════════════════════════════════════
#  TELEGRAM LAYER
# ═══════════════════════════════════════════════════════════

def esc(t): return str(t).replace("<", "&lt;").replace(">", "&gt;")
def strip_tags(t): return re.sub(r"\[/?[a-zA-Z0-9#]+\]", "", str(t))
def is_admin(uid): return int(uid) == int(ADMIN_UID)

HELP_TEXT = (
    "ℹ️ <b>ᴛʜᴇ ᴠᴏɪᴅ ᴛᴄᴘ ʙᴏᴛ — ᴄᴏᴍᴍᴀɴᴅs</b>\n\n"
    "🚀 <b>ᴛᴇᴀᴍs</b>\n"
    "╭──────────────\n"
    "│ /5 — ᴄʀᴇᴀᴛᴇ ᴛᴇᴀᴍ 5\n"
    "│ /6 — ᴄʀᴇᴀᴛᴇ ᴛᴇᴀᴍ 6\n"
    "│ /join &lt;code&gt; — ᴊᴏɪɴ sǫᴜᴀᴅ\n"
    "│ /exit — ʟᴇᴀᴠᴇ sǫᴜᴀᴅ\n"
    "╰──────────────\n\n"
    "🎯 <b>ᴀᴛᴛᴀᴄᴋs</b>\n"
    "╭──────────────\n"
    "│ /gh &lt;code&gt; &lt;name&gt; — sᴇɴᴅ ɢʜᴏsᴛs\n"
    "│ /lag &lt;code&gt; [n] — ʟᴀɢ ᴀᴛᴛᴀᴄᴋ\n"
    "│ /msg &lt;code&gt; &lt;text&gt; — sᴘᴀᴍ ᴍsɢs\n"
    "│ /spm &lt;uid&gt; — sᴘᴀᴍ ᴊᴏɪɴs\n"
    "│ /stp &lt;uid&gt; — sᴛᴏᴘ sᴘᴀᴍ\n"
    "│ /ban &lt;uid&gt; — ʙᴀɴ ʟᴏᴏᴘ\n"
    "╰──────────────\n\n"
    "📊 <b>ɪɴꜰᴏ</b>\n"
    "╭──────────────\n"
    "│ /info &lt;uid&gt; — ᴘʟᴀʏᴇʀ ɪɴꜰᴏ\n"
    "│ /check &lt;uid&gt; — ʙᴀɴ ᴄʜᴇᴄᴋ\n"
    "│ /status — ᴇɴɢɪɴᴇ sᴛᴀᴛᴜs\n"
    "╰──────────────\n\n"
    "🎮 <b>ᴇᴠᴏ ɢᴜɴ</b>\n"
    "╭──────────────\n"
    "│ /evos [uid ...] — sᴛᴀʀᴛ ᴄʏᴄʟᴇ\n"
    "│ /sevos — sᴛᴏᴘ ᴄʏᴄʟᴇ\n"
    "╰──────────────\n\n"
    "👑 <b>ᴀᴅᴍɪɴ ᴏɴʟʏ</b>\n"
    "╭──────────────\n"
    "│ /add &lt;uid&gt; — ꜰʀɪᴇɴᴅ ʀᴇǫᴜᴇsᴛ\n"
    "│ /remove &lt;uid&gt; — ʀᴇᴍᴏᴠᴇ ꜰʀɪᴇɴᴅ\n"
    "╰──────────────\n\n"
    f"📱 {SUPPORT_1} · {SUPPORT_2}"
)

async def t_start(update, ctx):
    u = update.effective_user
    txt = (
        f"👋 ʜɪ, <b>{esc(u.first_name)}</b>  ✨\n\n"
        f"😎 ᴜꜱᴇʀ : <b>{esc(u.first_name)}</b>\n"
        f"👑 ɪᴅ   : <code>{u.id}</code>\n\n"
        f"✨ <b>ᴛʜᴇ ᴠᴏɪᴅ ᴛᴄᴘ ʙᴏᴛ</b> ✨\n\n"
        f"ᴛʏᴘᴇ /help ꜰᴏʀ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs.\n"
        f"ᴛᴀᴘ / ᴛᴏ sᴇᴇ ᴛʜᴇ ᴀᴜᴛᴏ-ᴄᴏᴍᴘʟᴇᴛᴇ ʟɪsᴛ.\n\n"
        f"📢 {CHANNEL}\n💬 {GROUP}\n\n"
        f"📱 {SUPPORT_1} · {SUPPORT_2}"
    )
    await update.message.reply_text(txt, parse_mode=ParseMode.HTML,
                                    disable_web_page_preview=True)

async def t_help(update, ctx):
    await update.message.reply_text(HELP_TEXT, parse_mode=ParseMode.HTML,
                                    disable_web_page_preview=True)

async def t_status(update, ctx):
    alive = engine_alive()
    txt = (
        f"🛰 <b>ᴇɴɢɪɴᴇ sᴛᴀᴛᴜs</b>\n\n"
        f"╭──────────────\n"
        f"│ ꜱᴛᴀᴛᴇ  : {'🟢 ᴏɴʟɪɴᴇ' if alive else '🔴 ᴏꜰꜰʟɪɴᴇ'}\n"
        f"│ ʙᴏᴛ ᴜɪᴅ: <code>{bot_uid or '—'}</code>\n"
        f"│ ʀᴇɢɪᴏɴ : {region or '—'}\n"
        f"╰──────────────"
    )
    await update.message.reply_text(txt, parse_mode=ParseMode.HTML)

async def t_5(update, ctx):
    ok, m = await cmd_team(5)
    await update.message.reply_text(f"{'✅' if ok else '❌'} {esc(m)}",
                                    parse_mode=ParseMode.HTML)

async def t_6(update, ctx):
    ok, m = await cmd_team(6)
    await update.message.reply_text(f"{'✅' if ok else '❌'} {esc(m)}",
                                    parse_mode=ParseMode.HTML)

async def t_join(update, ctx):
    if not ctx.args:
        await update.message.reply_text("ᴜsᴀɢᴇ: /join &lt;code&gt;",
                                        parse_mode=ParseMode.HTML); return
    ok, m = await cmd_join(ctx.args[0])
    await update.message.reply_text(f"{'✅' if ok else '❌'} {esc(m)}",
                                    parse_mode=ParseMode.HTML)

async def t_exit(update, ctx):
    ok, m = await cmd_exit()
    await update.message.reply_text(f"{'✅' if ok else '❌'} {esc(m)}",
                                    parse_mode=ParseMode.HTML)

async def t_gh(update, ctx):
    if len(ctx.args) < 2:
        await update.message.reply_text("ᴜsᴀɢᴇ: /gh &lt;code&gt; &lt;name&gt;",
                                        parse_mode=ParseMode.HTML); return
    code, name = ctx.args[0], " ".join(ctx.args[1:])
    await update.message.reply_text("⏳ ᴡᴏʀᴋɪɴɢ...")
    ok, m = await cmd_ghost(code, name)
    await update.message.reply_text(f"{'✅' if ok else '❌'} {esc(m)}",
                                    parse_mode=ParseMode.HTML)

async def t_lag(update, ctx):
    if not ctx.args:
        await update.message.reply_text("ᴜsᴀɢᴇ: /lag &lt;code&gt; [count]",
                                        parse_mode=ParseMode.HTML); return
    code = ctx.args[0]
    n = int(ctx.args[1]) if len(ctx.args) > 1 and ctx.args[1].isdigit() else 30
    await update.message.reply_text(f"⏳ ʟᴀɢ x{n} ᴏɴ {esc(code)}...",
                                    parse_mode=ParseMode.HTML)
    ok, m = await cmd_lag(code, n)
    await update.message.reply_text(f"{'✅' if ok else '❌'} {esc(m)}",
                                    parse_mode=ParseMode.HTML)

async def t_msg(update, ctx):
    if len(ctx.args) < 2:
        await update.message.reply_text("ᴜsᴀɢᴇ: /msg &lt;code&gt; &lt;text&gt;",
                                        parse_mode=ParseMode.HTML); return
    code, text = ctx.args[0], " ".join(ctx.args[1:])
    await update.message.reply_text("⏳ sᴘᴀᴍᴍɪɴɢ...")
    ok, m = await cmd_spam_msg(code, text, 30)
    await update.message.reply_text(f"{'✅' if ok else '❌'} {esc(m)}",
                                    parse_mode=ParseMode.HTML)

async def t_spm(update, ctx):
    if not ctx.args:
        await update.message.reply_text("ᴜsᴀɢᴇ: /spm &lt;uid&gt;",
                                        parse_mode=ParseMode.HTML); return
    ok, m = await cmd_spm(ctx.args[0])
    await update.message.reply_text(f"{'✅' if ok else '❌'} {esc(m)}",
                                    parse_mode=ParseMode.HTML)

async def t_stp(update, ctx):
    if not ctx.args:
        await update.message.reply_text("ᴜsᴀɢᴇ: /stp &lt;uid&gt;",
                                        parse_mode=ParseMode.HTML); return
    ok, m = await cmd_stp(ctx.args[0])
    await update.message.reply_text(f"{'✅' if ok else '❌'} {esc(m)}",
                                    parse_mode=ParseMode.HTML)

async def t_ban(update, ctx):
    if not ctx.args:
        await update.message.reply_text("ᴜsᴀɢᴇ: /ban &lt;uid&gt;",
                                        parse_mode=ParseMode.HTML); return
    ok, m = await cmd_ban(ctx.args[0])
    await update.message.reply_text(f"{'✅' if ok else '❌'} {esc(m)}",
                                    parse_mode=ParseMode.HTML)

async def t_info(update, ctx):
    if not ctx.args:
        await update.message.reply_text("ᴜsᴀɢᴇ: /info &lt;uid&gt;",
                                        parse_mode=ParseMode.HTML); return
    await update.message.reply_text("⏳ ꜰᴇᴛᴄʜɪɴɢ...")
    ok, m = await cmd_info(ctx.args[0])
    await update.message.reply_text(f"{'✅' if ok else '❌'}\n{esc(strip_tags(m))}",
                                    parse_mode=ParseMode.HTML)

async def t_check(update, ctx):
    if not ctx.args:
        await update.message.reply_text("ᴜsᴀɢᴇ: /check &lt;uid&gt;",
                                        parse_mode=ParseMode.HTML); return
    await update.message.reply_text("⏳ ᴄʜᴇᴄᴋɪɴɢ...")
    ok, m = await cmd_check(ctx.args[0])
    await update.message.reply_text(f"{'✅' if ok else '❌'}\n{esc(strip_tags(m))}",
                                    parse_mode=ParseMode.HTML)

async def t_evos(update, ctx):
    uids = ctx.args if ctx.args else [str(update.effective_user.id)]
    ok, m = await cmd_evos(uids)
    await update.message.reply_text(f"{'✅' if ok else '❌'} {esc(m)}",
                                    parse_mode=ParseMode.HTML)

async def t_sevos(update, ctx):
    ok, m = await cmd_sevos()
    await update.message.reply_text(f"{'✅' if ok else '❌'} {esc(m)}",
                                    parse_mode=ParseMode.HTML)

async def t_add(update, ctx):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔ ᴀᴅᴍɪɴ ᴏɴʟʏ"); return
    if not ctx.args:
        await update.message.reply_text("ᴜsᴀɢᴇ: /add &lt;uid&gt;",
                                        parse_mode=ParseMode.HTML); return
    ok, m = await cmd_add(ctx.args[0])
    await update.message.reply_text(f"{'✅' if ok else '❌'} {esc(m)}",
                                    parse_mode=ParseMode.HTML)

async def t_remove(update, ctx):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔ ᴀᴅᴍɪɴ ᴏɴʟʏ"); return
    if not ctx.args:
        await update.message.reply_text("ᴜsᴀɢᴇ: /remove &lt;uid&gt;",
                                        parse_mode=ParseMode.HTML); return
    ok, m = await cmd_remove(ctx.args[0])
    await update.message.reply_text(f"{'✅' if ok else '❌'} {esc(m)}",
                                    parse_mode=ParseMode.HTML)

async def t_unknown(update, ctx):
    await update.message.reply_text("❓ ᴜɴᴋɴᴏᴡɴ ᴄᴏᴍᴍᴀɴᴅ.\nᴛʀʏ /help",
                                    parse_mode=ParseMode.HTML)

COMMANDS = [
    BotCommand("start",  "🚀 ʟᴀᴜɴᴄʜ"),
    BotCommand("help",   "ℹ️ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs"),
    BotCommand("status", "🛰 ᴇɴɢɪɴᴇ sᴛᴀᴛᴜs"),
    BotCommand("5",      "👥 ᴄʀᴇᴀᴛᴇ ᴛᴇᴀᴍ 5"),
    BotCommand("6",      "👥 ᴄʀᴇᴀᴛᴇ ᴛᴇᴀᴍ 6"),
    BotCommand("join",   "🔗 ᴊᴏɪɴ sǫᴜᴀᴅ"),
    BotCommand("exit",   "🚪 ʟᴇᴀᴠᴇ sǫᴜᴀᴅ"),
    BotCommand("gh",     "👻 sᴇɴᴅ ɢʜᴏsᴛs"),
    BotCommand("lag",    "⚡ ʟᴀɢ ᴀᴛᴛᴀᴄᴋ"),
    BotCommand("msg",    "💬 sᴘᴀᴍ ᴍsɢs"),
    BotCommand("spm",    "🌊 sᴘᴀᴍ ᴊᴏɪɴs"),
    BotCommand("stp",    "🛑 sᴛᴏᴘ sᴘᴀᴍ"),
    BotCommand("ban",    "☠️ ʙᴀɴ ʟᴏᴏᴘ"),
    BotCommand("info",   "📊 ᴘʟᴀʏᴇʀ ɪɴꜰᴏ"),
    BotCommand("check",  "🩺 ʙᴀɴ ᴄʜᴇᴄᴋ"),
    BotCommand("evos",   "🎮 ᴇᴠᴏ ᴄʏᴄʟᴇ ᴏɴ"),
    BotCommand("sevos",  "🛑 ᴇᴠᴏ ᴄʏᴄʟᴇ ᴏꜰꜰ"),
    BotCommand("add",    "👑 ᴀᴅᴍɪɴ: ꜰʀɪᴇɴᴅ"),
    BotCommand("remove", "👑 ᴀᴅᴍɪɴ: ʀᴇᴍᴏᴠᴇ"),
]

# ═══════════════════════════════════════════════════════════
#  HEALTH SERVER — for render web service
# ═══════════════════════════════════════════════════════════

class _Health(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", "2")
        self.end_headers()
        self.wfile.write(b"ok")
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
    def log_message(self, *a):
        pass

def _serve_health():
    port = int(os.getenv("PORT", "8080"))
    srv = HTTPServer(("0.0.0.0", port), _Health)
    log.info(f"health server on :{port}")
    srv.serve_forever()

# ═══════════════════════════════════════════════════════════
#  BOOT
# ═══════════════════════════════════════════════════════════

def main():
    threading.Thread(target=_serve_health, daemon=True).start()

    app = Application.builder().token(BOT_TOKEN).build()

    async def _post_init(application):
        await application.bot.set_my_commands(COMMANDS)
        asyncio.create_task(engine_loop())
        log.info("engine loop scheduled · command menu registered")

    app.post_init = _post_init

    app.add_handler(CommandHandler("start",  t_start))
    app.add_handler(CommandHandler("help",   t_help))
    app.add_handler(CommandHandler("status", t_status))
    app.add_handler(CommandHandler("5",      t_5))
    app.add_handler(CommandHandler("6",      t_6))
    app.add_handler(CommandHandler("join",   t_join))
    app.add_handler(CommandHandler("exit",   t_exit))
    app.add_handler(CommandHandler("gh",     t_gh))
    app.add_handler(CommandHandler("lag",    t_lag))
    app.add_handler(CommandHandler("msg",    t_msg))
    app.add_handler(CommandHandler("spm",    t_spm))
    app.add_handler(CommandHandler("stp",    t_stp))
    app.add_handler(CommandHandler("ban",    t_ban))
    app.add_handler(CommandHandler("info",   t_info))
    app.add_handler(CommandHandler("check",  t_check))
    app.add_handler(CommandHandler("evos",   t_evos))
    app.add_handler(CommandHandler("sevos",  t_sevos))
    app.add_handler(CommandHandler("add",    t_add))
    app.add_handler(CommandHandler("remove", t_remove))

    log.info("🚀 ᴛʜᴇ ᴠᴏɪᴅ ᴛᴄᴘ ʙᴏᴛ sᴛᴀʀᴛɪɴɢ")
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

if __name__ == "__main__":
    main()
