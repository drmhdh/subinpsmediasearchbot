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

import numpy as np
import PIL
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
from pyUltroid.functions.tools import four_point_transform
from skimage.filters import threshold_local
from telethon.errors.rpcerrorlist import PhotoSaveFileInvalidError

from . import *

if not os.path.isdir("pdf"):
    os.mkdir("pdf")


@Client_cmd(
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
