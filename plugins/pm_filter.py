#Kanged From @TroJanZheX
from info import AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, API_KEY, AUTH_GROUPS, BUTTON
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
import re
from pyrogram.errors import UserNotParticipant
from utils import get_filter_results, get_file_details, is_subscribed, get_poster
BUTTONS = {}
BOT = {}
@Client.on_message(filters.text & filters.private & filters.incoming & filters.user(AUTH_USERS) if AUTH_USERS else filters.text & filters.private & filters.incoming)
async def filter(client, message):
    if message.text.startswith("/"):
        return
    if AUTH_CHANNEL:
        invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
        try:
            user = await client.get_chat_member(int(AUTH_CHANNEL), message.from_user.id)
            if user.status == "kicked":
                await client.send_message(
                    chat_id=message.from_user.id,
                    text="Sorry Sir, You are Banned to use me.",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await client.send_message(
                chat_id=message.from_user.id,
                text="**🔊 𝗝𝗼𝗶𝗻 𝗢𝘂𝗿 𝗠𝗮𝗶𝗻 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 🤭** \n \n Are You Looking for References ?! \n Then First Join Our 🦷𝔻𝕖𝕟𝕥𝕒𝕝 ℂ𝕒𝕤𝕖 𝕊𝕥𝕦𝕕𝕪🔎 Channel...😁 Then Try Again... Press /start 😁 and You will Get Your Requests Here...! \n \n 🪐Powered by: \n 🔬 @dent_tech_for_u 📚",
     
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("𝗝𝗼𝗶𝗻 🦷𝔻𝕖𝕟𝕥𝕒𝕝 ℂ𝕒𝕤𝕖 𝕊𝕥𝕦𝕕𝕪🔎", url=invite_link.invite_link)
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await client.send_message(
                chat_id=message.from_user.id,
                text="Something went Wrong.",
                parse_mode="markdown",
                disable_web_page_preview=True
            )
            return
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 100:    
        btn = []
        search = message.text
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"[{get_size(file.file_size)}] {file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}",callback_data=f"subinps#{file_id}")]
                    )
        else:
            await client.send_sticker(chat_id=message.from_user.id, sticker='CAACAgUAAxkBAAEDV55hnEhbJYmRSYDfz-E-dGpAVXfvnwACEAMAAvnZ4VSjsvEouvHC4SIE')
            return

        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="📃 Pages 1/1",callback_data="pages")]
            )
            if BUTTON:
                buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")])
            poster=None
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                await message.reply_photo(photo=poster, caption=f"<b>{message.from_user.mention}, ☕️ 𝗛𝗲𝗿𝗲 𝗶𝘀 𝗪𝗵𝗮𝘁 𝗜 𝗙𝗼𝘂𝗻𝗱 𝗳𝗼𝗿 𝗬𝗼𝘂𝗿 𝗤𝘂𝗲𝗿𝘆 ❝{search}❞ ‌‌‌‌‎ ­  ­  ­  ­  ­  </b>", reply_markup=InlineKeyboardMarkup(buttons))

            else:
                await message.reply_text(f"<b>{message.from_user.mention}, ☕️ 𝗛𝗲𝗿𝗲 𝗶𝘀 𝗪𝗵𝗮𝘁 𝗜 𝗙𝗼𝘂𝗻𝗱 𝗳𝗼𝗿 𝗬𝗼𝘂𝗿 𝗤𝘂𝗲𝗿𝘆 ❝{search}❞ ‌‌‌‌‎ ­  ­  ­  ­  ­  </b>", reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="NEXT ⏩",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"📃 Pages 1/{data['total']}",callback_data="pages")]
        )
        if BUTTON:
            buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")])
        poster=None
        if API_KEY:
            poster=await get_poster(search)
        if poster:
            await message.reply_photo(photo=poster, caption=f"<b>{message.from_user.mention}, ☕️ 𝗛𝗲𝗿𝗲 𝗶𝘀 𝗪𝗵𝗮𝘁 𝗜 𝗙𝗼𝘂𝗻𝗱 𝗳𝗼𝗿 𝗬𝗼𝘂𝗿 𝗤𝘂𝗲𝗿𝘆 ❝{search}❞ ‌‌‌‌‎ ­  ­  ­  ­  ­  </b>", reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_text(f"<b>{message.from_user.mention}, ☕️ 𝗛𝗲𝗿𝗲 𝗶𝘀 𝗪𝗵𝗮𝘁 𝗜 𝗙𝗼𝘂𝗻𝗱 𝗳𝗼𝗿 𝗬𝗼𝘂𝗿 𝗤𝘂𝗲𝗿𝘆 ❝{search}❞ ‌‌‌‌‎ ­  ­  ­  ­  ­  </b>", reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_message(filters.text & filters.group & filters.incoming & filters.chat(AUTH_GROUPS) if AUTH_GROUPS else filters.text & filters.group & filters.incoming)
async def group(client, message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 50:    
        btn = []
        search = message.text
        nyva=BOT.get("username")
        if not nyva:
            botusername=await client.get_me()
            nyva=botusername.username
            BOT["username"]=nyva
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"[{get_size(file.file_size)}] {file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}", url=f"https://telegram.dog/{nyva}?start=subinps_-_-_-_{file_id}")]
                )
        else:
            return
        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="📃 Pages 1/1",callback_data="pages")]
            )
            if BUTTON:
                buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")])
            poster=None
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                await message.reply_photo(photo=poster, caption=f"<b>{message.from_user.mention}, ☕️ 𝗛𝗲𝗿𝗲 𝗶𝘀 𝗪𝗵𝗮𝘁 𝗜 𝗙𝗼𝘂𝗻𝗱 𝗳𝗼𝗿 𝗬𝗼𝘂𝗿 𝗤𝘂𝗲𝗿𝘆 ❝{search}❞ ‌‌‌‌‎ ­  ­  ­  ­  ­  </b>", reply_markup=InlineKeyboardMarkup(buttons))
            else:
                await message.reply_text(f"<b>{message.from_user.mention}, ☕️ 𝗛𝗲𝗿𝗲 𝗶𝘀 𝗪𝗵𝗮𝘁 𝗜 𝗙𝗼𝘂𝗻𝗱 𝗳𝗼𝗿 𝗬𝗼𝘂𝗿 𝗤𝘂𝗲𝗿𝘆 ❝{search}❞ ‌‌‌‌‎ ­  ­  ­  ­  ­  </b>", reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="NEXT ⏩",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"📃 Pages 1/{data['total']}",callback_data="pages")]
        )
        if BUTTON:
            buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")])
        poster=None
        if API_KEY:
            poster=await get_poster(search)
        if poster:
            await message.reply_photo(photo=poster, caption=f"<b>{message.from_user.mention}, ☕️ 𝗛𝗲𝗿𝗲 𝗶𝘀 𝗪𝗵𝗮𝘁 𝗜 𝗙𝗼𝘂𝗻𝗱 𝗳𝗼𝗿 𝗬𝗼𝘂𝗿 𝗤𝘂𝗲𝗿𝘆 ❝{search}❞ ‌‌‌‌‎ ­  ­  ­  ­  ­  </b>", reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_text(f"<b>{message.from_user.mention}, ☕️ 𝗛𝗲𝗿𝗲 𝗶𝘀 𝗪𝗵𝗮𝘁 𝗜 𝗙𝗼𝘂𝗻𝗱 𝗳𝗼𝗿 𝗬𝗼𝘂𝗿 𝗤𝘂𝗲𝗿𝘆 ❝{search}❞ ‌‌‌‌‎ ­  ­  ­  ­  ­  </b>", reply_markup=InlineKeyboardMarkup(buttons))

    
def get_size(size):
    """Get size in readable format"""

    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])

def split_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]          



@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    clicked = query.from_user.id
    try:
        typed = query.message.reply_to_message.from_user.id
    except:
        typed = query.from_user.id
        pass
    if (clicked == typed):

        if query.data.startswith("next"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == int(data["total"]) - 2:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪ BACK", callback_data=f"back_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 Pages {int(index)+2}/{data['total']}", callback_data="pages")]
                )
                if BUTTON:
                    buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")])

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪ BACK", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 Pages {int(index)+2}/{data['total']}", callback_data="pages")]
                )
                if BUTTON:
                    buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")])

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return


        elif query.data.startswith("back"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == 1:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 Pages {int(index)}/{data['total']}", callback_data="pages")]
                )
                if BUTTON:
                    buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")])

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return   
            else:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪ BACK", callback_data=f"back_{int(index)-1}_{keyword}"),InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 Pages {int(index)}/{data['total']}", callback_data="pages")]
                )
                if BUTTON:
                    buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")])

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
        elif query.data == "about":
            buttons = [
                [
                    InlineKeyboardButton('𝗝𝗼𝗶𝗻 🦷𝔻𝕖𝕟𝕥𝕒𝕝 ℂ𝕒𝕤𝕖 𝕊𝕥𝕦𝕕𝕪🔎', url='https://t.me/dental_case_study')
                ],[    
                    InlineKeyboardButton('➕ Join 🦷 Discussion Group ➕', url='https://t.me/dent_tech_for_u')
                ]
                ]
            await query.message.edit(text="<b>Developer : <a href='https://t.me/dent_tech_for_books'>📚🅳🆃 📖 🆁🅾🅾🅼📚</a>\nLanguage : <code>Python3</code>\nLibrary : <a href='https://t.me/dent_tech_library'>🔬𝔻𝕖𝕟𝕥 𝕋𝕖𝕔𝕙 𝕃𝕚𝕓𝕣𝕒𝕣𝕪📚</a>\nDiscussion Group: <a href='https://t.me/dent_tech_for_u'>Click Here</a>\n𝗝𝗼𝗶𝗻 🦷𝔻𝕖𝕟𝕥𝕒𝕝 ℂ𝕒𝕤𝕖 𝕊𝕥𝕦𝕕𝕪🔎: <a href='https://t.me/dental_case_study'>Click Here</a></b>", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)



        elif query.data.startswith("subinps"):
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=get_size(files.file_size)
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{files.file_name}"
                buttons = [
                    [
                        InlineKeyboardButton('📚🅳🆃 📖 🆁🅾🅾🅼📚', url='https://t.me/dent_tech_for_books')
                    ],[
                        InlineKeyboardButton('𝗝𝗼𝗶𝗻 🦷𝔻𝕖𝕟𝕥𝕒𝕝 ℂ𝕒𝕤𝕖 𝕊𝕥𝕦𝕕𝕪🔎', url='https://t.me/dental_case_study')
                    ]
                    ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
        elif query.data.startswith("checksub"):
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer("I Like Your Smartness, But Don't Be Oversmart 😒",show_alert=True)
                return
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=get_size(files.file_size)
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{title}"
                buttons = [
                    [
                        InlineKeyboardButton('📚🅳🆃 📖 🆁🅾🅾🅼📚', url='https://t.me/dent_tech_for_books'),
                        InlineKeyboardButton('𝗝𝗼𝗶𝗻 🦷𝔻𝕖𝕟𝕥𝕒𝕝 ℂ𝕒𝕤𝕖 𝕊𝕥𝕦𝕕𝕪🔎', url='https://t.me/dental_case_study')
                    ]
                    ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )


        elif query.data == "pages":
            await query.answer()
        elif query.data == "close":
            try:
                await query.message.reply_to_message.delete()
                await query.message.delete()
            except:
                await query.message.delete()
                
    else:
        await query.answer("It Will Not Work for You, as It was Not Requested by You 😒",show_alert=True)
