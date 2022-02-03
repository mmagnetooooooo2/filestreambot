# (c) Code-X-Mania

from Code_X_Mania.bot import StreamBot
from Code_X_Mania.vars import Var
from Code_X_Mania.utils.human_readable import humanbytes
from Code_X_Mania.utils.database import Database
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
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

@StreamBot.on_message(filters.command('start') & filters.private & ~filters.edited)
async def start(b, m):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await b.send_message(
            Var.BIN_CHANNEL,
            f"**Yeni Bir Kullanıcı :** \n\n__Yeni Arkadaşım__ [{m.from_user.first_name}](tg://user?id={m.from_user.id}) __Botu Çalıştırdı !!__"
        )
    usr_cmd = m.text.split("_")[-1]
    if usr_cmd == "/start":
        if Var.UPDATES_CHANNEL != "None":
            try:
                user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
                if user.status == "kicked":
                    await b.send_message(
                        chat_id=m.chat.id,
                        text="__Üzgünüm Beni Kullanman Yasaklandı__",
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="<i>Kanalımıza Katılın 🔐</i>",
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
                await b.send_message(
                    chat_id=m.chat.id,
                    text="<i>Bir şeyler ters gitti !</i>",
                    parse_mode="HTML",
                    disable_web_page_preview=True)
                return
        await m.reply_text(
            text="""
<i>👋 Selam ! Ben bağlantı oluşturmaya yarayan bir botum.</i>\n
<i>Bana bir dosya gönder ve sonra sihri gör !<i>\n
<i><u>Uyarı 🚸</u></i>\n
<b>Spam Yapmayınız.</b>""",
            parse_mode="HTML",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup( [ [InlineKeyboardButton('Sahip', url=f"https://t.me/{Var.OWNER_USERNAME}"),
                                                                                       InlineKeyboardButton('Grubuma katıl', url='https://t.me/anagrupp') ] ]  ) )
                                                                                       
                                                                                       
                                                                            
    else:
        if Var.UPDATES_CHANNEL != "None":
            try:
                user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
                if user.status == "kicked":
                    await b.send_message(
                        chat_id=m.chat.id,
                        text="**Beni Kullanman Yasak !",
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="**Lütfen Kanalımıza Katılın**!",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🤖 Kanalımıza Katıl ", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                            ],
                            [
                                InlineKeyboardButton("🔄 Yenile / Tekrar Deneyin",
                                                     url=f"https://t.me/{Var.APP_NAME}.herokuapp.com/{usr_cmd}") # Chnage ur app name
                            ]
                        ]
                    ),
                    parse_mode="markdown"
                )
                return
            except Exception:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="**Hay Aksi Birşeyler Ters Gidiyor !** [Hydrathalles](https://t.me/hydrathalles).",
                    parse_mode="markdown",
                    disable_web_page_preview=True)
                return

        get_msg = await b.get_messages(chat_id=Var.BIN_CHANNEL, message_ids=int(usr_cmd))

        file_size = None
        if get_msg.video:
            file_size = f"{humanbytes(get_msg.video.file_size)}"
        elif get_msg.document:
            file_size = f"{humanbytes(get_msg.document.file_size)}"
        elif get_msg.audio:
            file_size = f"{humanbytes(get_msg.audio.file_size)}"

        file_name = None
        if get_msg.video:
            file_name = f"{get_msg.video.file_name}"
        elif get_msg.document:
            file_name = f"{get_msg.document.file_name}"
        elif get_msg.audio:
            file_name = f"{get_msg.audio.file_name}"

        stream_link = Var.URL + 'izle/' + str(log_msg.message_id)
        shortlink = get_shortlink(stream_link)
        if shortlink:
            stream_link = shortlink
        online_link = Var.URL + 'indir/' + str(log_msg.message_id)
        shortlinka = get_shortlink(online_link)
        if shortlinka:
            online_link = shortlinka

        msg_text ="""
<i><u>Bağlantın Oluşturuldu !</u></i>

<b>📂 Dosya Adı :</b> <i>{}</i>

<b>📦 Dosya Boyutu :</b> <i>{}</i>

<b>📥 İndir :</b> <i>{}</i>

<b> 🖥 İzle  :</b> <i>{}</i>

<b>🚸 Not : Bağlantılar Süresizdir ! </b>

<i>@quickwaste</i>"""

        await m.reply_text(
            text=msg_text.format(file_name, file_size, online_link, stream_link),
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("İzle 🖥", url=stream_link), #Stream Link
                                                InlineKeyboardButton('İndir 📥', url=online_link)]]) #Download Link
        )


@StreamBot.on_message(filters.command('help') & filters.private & ~filters.edited)
async def help_handler(bot, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
        await bot.send_message(
            Var.BIN_CHANNEL,
            f"**Yeni Bir Kullanıcı**\n\n__Yeni Arkadaşım__ [{message.from_user.first_name}](tg://user?id={message.from_user.id}) __Botu Çalıştırdı !!__"
        )
    if Var.UPDATES_CHANNEL is not None:
        try:
            user = await bot.get_chat_member(Var.UPDATES_CHANNEL, message.chat.id)
            if user.status == "kicked":
                await bot.send_message(
                    chat_id=message.chat.id,
                    text="<i>Üzgünüm Beni Kullanman Yasaklandı !</i>",
                    parse_mode="HTML",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await bot.send_message(
                chat_id=message.chat.id,
                text="**Lütfen Kanalımıza Katılın !**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🤖 Şimdi Katıl ", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await bot.send_message(
                chat_id=message.chat.id,
                text="__Birşeyler yanlış gitti !__[Sahip](https://t.me/mmagneto).",
                parse_mode="markdown",
                disable_web_page_preview=True)
            return
   
    await message.reply_text(
       text="Bana Bir Dosya Gönder ve Sihri Gör :)",
            parse_mode="HTML",
            
          reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("🏵 SAHİP", url="https://t.me/mmagneto")],
                [InlineKeyboardButton("🍺 TAKİP ET", url="https://t.me/anagrupp")]
            ]
        )
    )
