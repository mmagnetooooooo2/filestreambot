# (c) Code-X-Mania

import asyncio
from Code_X_Mania.bot import StreamBot
from Code_X_Mania.utils.database import Database
from Code_X_Mania.utils.human_readable import humanbytes
from Code_X_Mania.vars import Var
from pyrogram import filters, Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
db = Database(Var.DATABASE_URL, Var.SESSION_NAME)
from pyshorteners import Shortener



def get_shortlink(url):
   shortlink = False 
   try:
      shortlink = Shortener().dagd.short(url)
   except Exception as err:
       print(err)
       pass
   return shortlink
@StreamBot.on_message(filters.private & (filters.document | filters.video | filters.audio) & ~filters.edited, group=4)
async def private_receive_handler(c: Client, m: Message):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await c.send_message(
            Var.BIN_CHANNEL,
            f"Yeni Bir Kullanıcı : \n\n İsim : [{m.from_user.first_name}](tg://user?id={m.from_user.id}) Botu Çalıştırdı !!"
        )
    if Var.UPDATES_CHANNEL != "None":
        try:
            user = await c.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
            if user.status == "kicked":
                await c.send_message(
                    chat_id=m.chat.id,
                    text="__Üzgünüm, Yasaklandın!.__",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await c.send_message(
                chat_id=m.chat.id,
                text="""<i>Kanalımıza Katılın 🔐</i>""",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Şimdi Katıl 🔓", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                        ]
                    ]
                ),
                parse_mode="HTML"
            )
            return
        except Exception:
            await c.send_message(
                chat_id=m.chat.id,
                text="**Birşeyler Ters Gitti !**",
                parse_mode="markdown",
                disable_web_page_preview=True)
            return
    try:
        log_msg = await m.forward(chat_id=Var.BIN_CHANNEL)
        stream_link = Var.URL + 'izle/' + str(log_msg.message_id)
        shortlink = get_shortlink(stream_link) 
        if shortlink:
            stream_link = shortlink
        online_link = Var.URL + 'indir/'+ str(log_msg.message_id) 
        shortlinka = get_shortlink(online_link)
        if shortlinka:
            online_link = shortlinka
        
        file_size = None
        if m.video:
            file_size = f"{humanbytes(m.video.file_size)}"
        elif m.document:
            file_size = f"{humanbytes(m.document.file_size)}"
        elif m.audio:
            file_size = f"{humanbytes(m.audio.file_size)}"

        file_name = None
        if m.video:
            file_name = f"{m.video.file_name}"
        elif m.document:
            file_name = f"{m.document.file_name}"
        elif m.audio:
            file_name = f"{m.audio.file_name}"

        msg_text ="""
<i><u>Bağlantın Oluşturuldu !</u></i>

<b>📂 Dosya Adı :</b> <i>{}</i>

<b>📦 Dosya Boyutu :</b> <i>{}</i>

<b>📥 İndir :</b> <i>{}</i>

<b> 🖥 İzle :</b> <i>{}</i>

<b>🚸 Not : Bağlantılar Süresizdir  </b>

<i>© @filmplatosu </i>"""

        await log_msg.reply_text(text=f"**Tarafından :** [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n**Kullanıcı ɪᴅ :** `{m.from_user.id}`\n**İndirme Linki :** {stream_link}", disable_web_page_preview=True, parse_mode="Markdown", quote=True)
        await m.reply_text(
            text=msg_text.format(file_name, file_size, online_link, stream_link),
            parse_mode="HTML", 
            quote=True,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("İzle 🖥", url=stream_link), #Stream Link
                                                InlineKeyboardButton('İndir 📥', url=online_link)]]) #Download Link
        )
    except FloodWait as e:
        print(f"Sleeping for {str(e.x)}s")
        await asyncio.sleep(e.x)
        await c.send_message(chat_id=Var.BIN_CHANNEL, text=f"Bekleme Süresi {str(e.x)}s from [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n\n**Kullanıcı 𝙸𝙳 :** `{str(m.from_user.id)}`", disable_web_page_preview=True, parse_mode="Markdown")


@StreamBot.on_message(filters.channel & (filters.document | filters.video) & ~filters.edited, group=-1)
async def channel_receive_handler(bot, broadcast):
    if int(broadcast.chat.id) in Var.BANNED_CHANNELS:
        await bot.leave_chat(broadcast.chat.id)
        return
    try:
        log_msg = await broadcast.forward(chat_id=Var.BIN_CHANNEL)
        stream_link = Var.URL + 'izle/' + str(log_msg.message_id) 
        online_link = Var.URL + 'indir/' + str(log_msg.message_id) 
        await log_msg.reply_text(
            text=f"**Kanal Adı:** `{broadcast.chat.title}`\n**Kanal ID:** `{broadcast.chat.id}`\n**Kullanıcı ᴜʀʟ:** {stream_link}",
            quote=True,
            parse_mode="Markdown"
        )
        await bot.edit_message_reply_markup(
            chat_id=broadcast.chat.id,
            message_id=broadcast.message_id,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("İzle 🖥", url=stream_link),
                     InlineKeyboardButton('İndir 📥', url=online_link)] 
                ]
            )
        )
    except FloodWait as w:
        print(f"Uyku Vakti İçin {str(w.x)}s")
        await asyncio.sleep(w.x)
        await bot.send_message(chat_id=Var.BIN_CHANNEL,
                             text=f"Bekleme Süresi {str(w.x)}s from {broadcast.chat.title}\n\n**Kanal ID:** `{str(broadcast.chat.id)}`",
                             disable_web_page_preview=True, parse_mode="Markdown")
    except Exception as e:
        await bot.send_message(chat_id=Var.BIN_CHANNEL, text=f"**#ᴇʀʀᴏʀ_ᴛʀᴀᴄᴇʙᴀᴄᴋ:** `{e}`", disable_web_page_preview=True, parse_mode="Markdown")
        print(f"Yayın mesajı düzenlenemiyor. \nHata:  **Bana güncellemelerde ve bin Chanell'de düzenleme izni ver{e}**")
