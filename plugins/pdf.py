# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
"""
✘ Commands Available -
• `{i}pdf <page num> <reply to pdf file>`
    Extract nd Send page as a Image.(note-: For Extraction all pages just use .pdf)
    You Can use multi pages too like `{i}pdf 1-7`
• `{i}pdtext <page num> <reply to pdf file>`
    Extract Text From the Pdf.(note-: For Extraction all text just use .pdtext)
    You Can use multi pages too like `{i}pdf 1-7`
• `{i}pdscan <reply to image>`
    It scan, crop nd send img as pdf.
• `{i}pdsave <reply to image/pdf>`
    It scan, crop nd save file to merge u can merge many pages as a single pdf.
• `{i}pdsend `
    Merge nd send the Pdf to collected from .pdsave.
"""
import glob
import os
import shutil
import time


from pyrogram import Client

from . import *

if not os.path.isdir("pdf"):
    os.mkdir("pdf")

 def compile_pattern(data, hndlr):
    if HNDLR == " ":  # No handler feature
        return re.compile("^" + data.replace("^", "").replace(".", ""))
    return (
        re.compile(hndlr + data.replace("^", "").replace(".", ""))
        if data.startswith("^")
        else re.compile(hndlr + data)
    )
   
    
def ultroid_cmd(allow_sudo=should_allow_sudo(), **args):
    # With time and addition of Stuff
    # Decorator has turned lengthy and non attractive.
    # Todo : Make it better..
    args["func"] = lambda e: not e.fwd_from and not e.via_bot_id
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    pattern = args["pattern"]
    black_chats = args.get("chats", None)
    groups_only = args.get("groups_only", False)
    admins_only = args.get("admins_only", False)
    fullsudo = args.get("fullsudo", False)
    allow_all = args.get("allow_all", False)
    type = args.get("type", ["official"])
    only_devs = args.get("only_devs", False)
    allow_pm = args.get("allow_pm", False)
    if isinstance(type, str):
        type = [type]
    if "official" in type and DUAL_MODE:
        type.append("dualmode")
        
    args["forwards"] = False
    if pattern:
        args["pattern"] = compile_pattern(pattern, hndlr)
        reg = re.compile("(.*)")
        try:
            cmd = re.search(reg, pattern)
            try:
                cmd = (
                    cmd.group(1)
                    .replace("$", "")
                    .replace("?(.*)", "")
                    .replace("(.*)", "")
                    .replace("(?: |)", "")
                    .replace("| ", "")
                    .replace("( |)", "")
                    .replace("?((.|//)*)", "")
                    .replace("?P<shortname>\\w+", "")
                )
            except BaseException:
                pass
            try:
                LIST[file_test].append(cmd)
            except BaseException:
                LIST.update({file_test: [cmd]})
        except BaseException:
            pass
    args["blacklist_chats"] = True
    if len(black_list_chats) > 0:
        args["chats"] = black_list_chats
    if black_chats is not None:
        if len(black_chats) == 0:
            args["chats"] = []
        else:
            args["chats"] = black_chats

    for i in [
        "admins_only",
        "groups_only",
        "type",
        "allow_all",
        "fullsudo",
        "only_devs",
        "allow_pm",
    ]:
        if i in args:
            del args[i]
    
    
@Ultroid_cmd(
    pattern="pdf ?(.*)",
)
async def pdfseimg(event):
    ok = await event.get_reply_message()
    msg = event.pattern_match.group(1)
    if not (ok and (ok.document and (ok.document.mime_type == "application/pdf"))):
        await eor(event, "`Reply The pdf u Want to Download..`")
        return
    xx = await eor(event, get_string("com_1"))
    file = ok.media.document
    k = time.time()
    filename = "hehe.pdf"
    result = await downloader(
        "pdf/" + filename,
        file,
        xx,
        k,
        "Downloading " + filename + "...",
    )
    await xx.delete()
    pdfp = "pdf/hehe.pdf"
    pdfp.replace(".pdf", "")
    pdf = PdfFileReader(pdfp)
    if not msg:
        ok = []
        for num in range(pdf.numPages):
            pw = PdfFileWriter()
            pw.addPage(pdf.getPage(num))
            fil = os.path.join("pdf/ult{}.png".format(num + 1))
            ok.append(fil)
            with open(fil, "wb") as f:
                pw.write(f)
        os.remove(pdfp)
        for z in ok:
            await event.client.send_file(event.chat_id, z)
        shutil.rmtree("pdf")
        os.mkdir("pdf")
        await xx.delete()
    elif "-" in msg:
        ok = int(msg.split("-")[-1]) - 1
        for o in range(ok):
            pw = PdfFileWriter()
            pw.addPage(pdf.getPage(o))
            with open(os.path.join("ult.png"), "wb") as f:
                pw.write(f)
            await event.reply(
                file="ult.png",
            )
            os.remove("ult.png")
        os.remove(pdfp)
    else:
        o = int(msg) - 1
        pw = PdfFileWriter()
        pw.addPage(pdf.getPage(o))
        with open(os.path.join("ult.png"), "wb") as f:
            pw.write(f)
        os.remove(pdfp)
        try:
            await event.reply(file="ult.png")
        except PhotoSaveFileInvalidError:
            await event.reply(file="ult.png", force_document=True)
        os.remove("ult.png")
