import io
from pyrogram import filters, bot
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.filters_mdb import(
   add_filter,
   get_filters,
   delete_filter,
   count_filters
)

from database.connections_mdb import active_connection
from utils import get_file_id, parser, split_quotes
from info import ADMINS


@Client.on_message(filters.command(['filter', 'add']) & filters.incoming)
async def addfilter(bot, cmd):
    userid = cmd.from_user.id if cmd.from_user else None
    if not userid:
        return await cmd.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
    chat_type = cmd.chat.type
    args = cmd.text.html.split(None, 1)

    if chat_type == "private":
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await bot.get_chat(grpid)
                title = chat.title
            except:
                await cmd.reply_text("Make sure I'm present in your group!!", quote=True)
                return
        else:
            await cmd.reply_text("I'm not connected to any groups!", quote=True)
            return

    elif chat_type in ["group", "supergroup"]:
        grp_id = cmd.chat.id
        title = cmd.chat.title

    else:
        return

    st = await bot.get_chat_member(grp_id, userid)
    if (
        st.status != "administrator"
        and st.status != "creator"
        and str(userid) not in ADMINS
    ):
        return


    if len(args) < 2:
        await cmd.reply_text("Command Incomplete :(", quote=True)
        return

    extracted = split_quotes(args[1])
    text = extracted[0].lower()

    if not cmd.reply_to_message and len(extracted) < 2:
        await cmd.reply_text("Add some content to save your filter!", quote=True)
        return

    if (len(extracted) >= 2) and not cmd.reply_to_message:
        reply_text, btn, alert = parser(extracted[1], text)
        fileid = None
        if not reply_text:
            await cmd.reply_text("You cannot have buttons alone, give some text to go with it!", quote=True)
            return

    elif cmd.reply_to_message and cmd.reply_to_message.reply_markup:
        try:
            rm = cmd.reply_to_message.reply_markup
            btn = rm.inline_keyboard
            msg = get_file_id(cmd.reply_to_message)
            if msg:
                fileid = msg.file_id
                reply_text = cmd.reply_to_message.caption.html
            else:
                reply_text = cmd.reply_to_message.text.html
                fileid = None
            alert = None
        except:
            reply_text = ""
            btn = "[]" 
            fileid = None
            alert = None

    elif cmd.reply_to_message and cmd.reply_to_message.media:
        try:
            msg = get_file_id(cmd.reply_to_message)
            fileid = msg.file_id if msg else None
            reply_text, btn, alert = parser(extracted[1], text) if cmd.reply_to_message.sticker else parser(cmd.reply_to_message.caption.html, text)
        except:
            reply_text = ""
            btn = "[]"
            alert = None
    elif cmd.reply_to_message and cmd.reply_to_message.text:
        try:
            fileid = None
            reply_text, btn, alert = parser(cmd.reply_to_message.text.html, text)
        except:
            reply_text = ""
            btn = "[]"
            alert = None
    else:
        return

    await add_filter(grp_id, text, reply_text, btn, fileid, alert)

    await cmd.reply_text(
        f"Filter for  `{text}`  added in  **{title}**",
        quote=True,
        parse_mode="md"
    )


@Client.on_message(filters.command(['viewfilters', 'filters']) & filters.incoming)
async def get_all(bot, cmd):
    
    chat_type = cmd.chat.type
    userid = cmd.from_user.id if cmd.from_user else None
    if not userid:
        return awaitcmd.reply(f"You are anonymous admin. Use /connect {cmd.chat.id} in PM")
    if chat_type == "private":
        userid = cmd.from_user.id
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await cmd.reply_text("Make sure I'm present in your group!!", quote=True)
                return
        else:
            await cmd.reply_text("I'm not connected to any groups!", quote=True)
            return

    elif chat_type in ["group", "supergroup"]:
        grp_id = cmd.chat.id
        title = cmd.chat.title

    else:
        return

    st = await bot.get_chat_member(grp_id, userid)
    if (
        st.status != "administrator"
        and st.status != "creator"
        and str(userid) not in ADMINS
    ):
        return

    texts = await get_filters(grp_id)
    count = await count_filters(grp_id)
    if count:
        filterlist = f"Total number of filters in **{title}** : {count}\n\n"

        for text in texts:
            keywords = " ×  `{}`\n".format(text)

            filterlist += keywords

        if len(filterlist) > 4096:
            with io.BytesIO(str.encode(filterlist.replace("`", ""))) as keyword_file:
                keyword_file.name = "keywords.txt"
                await cmd.reply_document(
                    document=keyword_file,
                    quote=True
                )
            return
    else:
        filterlist = f"There are no active filters in **{title}**"

    await cmd.reply_text(
        text=filterlist,
        quote=True,
        parse_mode="md"
    )
        
@Client.on_message(filters.command('del') & filters.incoming)
async def deletefilter(bot, cmd):
    userid = cmd.from_user.id if cmd.from_user else None
    if not userid:
        return await cmd.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
    chat_type = cmd.chat.type

    if chat_type == "private":
        grpid  = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await bot.get_chat(grpid)
                title = chat.title
            except:
                await cmd.reply_text("Make sure I'm present in your group!!", quote=True)
                return
        else:
            await cmd.reply_text("I'm not connected to any groups!", quote=True)

    elif chat_type in ["group", "supergroup"]:
        grp_id = cmd.chat.id
        title = cmd.chat.title

    else:
        return

    st = await bot.get_chat_member(grp_id, userid)
    if (
        st.status != "administrator"
        and st.status != "creator"
        and str(userid) not in ADMINS
    ):
        return

    try:
        cmd, text = cmd.text.split(" ", 1)
    except:
        await cmd.reply_text(
            "<i>Mention the filtername which you wanna delete!</i>\n\n"
            "<code>/del filtername</code>\n\n"
            "Use /viewfilters to view all available filters",
            quote=True
        )
        return

    query = text.lower()

    await delete_filter(cmd, query, grp_id)
        

@Client.on_message(filters.command('delall') & filters.incoming)
async def delallconfirm(bot, mcmd):
    userid = cmd.from_user.id if cmd.from_user else None
    if not userid:
        return await cmd.reply(f"You are anonymous admin. Use /connect {cmd.chat.id} in PM")
    chat_type = cmd.chat.type

    if chat_type == "private":
        grpid  = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await cmd.reply_text("Make sure I'm present in your group!!", quote=True)
                return
        else:
            await cmd.reply_text("I'm not connected to any groups!", quote=True)
            return

    elif chat_type in ["group", "supergroup"]:
        grp_id = cmd.chat.id
        title = cmd.chat.title

    else:
        return

    st = await bot.get_chat_member(grp_id, userid)
    if (st.status == "creator") or (str(userid) in ADMINS):
        await cmd.reply_text(
            f"This will delete all filters from '{title}'.\nDo you want to continue??",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text="YES",callback_data="delallconfirm")],
                [InlineKeyboardButton(text="CANCEL",callback_data="delallcancel")]
            ]),
            quote=True
        )
