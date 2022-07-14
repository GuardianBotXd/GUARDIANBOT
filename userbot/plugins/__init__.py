import math
import os
import re
import time

import heroku3
import lottie
import requests
import spamwatch as spam_watch
from validators.url import url

from .. import *
from ..Config import Config
from ..core.logger import logging
from ..core.managers import eod, eor
from ..core.session import guardian
from ..helpers import *
from ..helpers.utils import _format, _guardiantools, _guardianutils, install_pip, reply_id
from ..sql_helper.globals import gvarstatus

# =================== CONSTANT ===================
bot = guardian
LOGS = logging.getLogger(__name__)
USERID = legend.uid if Config.OWNER_ID == 0 else Config.OWNER_ID
ALIVE_NAME = Config.ALIVE_NAME
AUTONAME = Config.AUTONAME
DEFAULT_BIO = Config.DEFAULT_BIO


Heroku = heroku3.from_key(Config.API_KEY)
heroku_api = "https://api.heroku.com"
APP_NAME = Config.APP_NAME
API_KEY = Config.API_KEY

thumb_image_path = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")


# mention user
mention = f"[{Config.ALIVE_NAME}](tg://user?id={USERID})"
hmention = f"<a href = tg://user?id={USERID}>{Config.ALIVE_NAME}</a>"


GUARDIAN_USER = guardian.me.first_name
DinoGuardian = guardian.uid
Guardian_mention = f"[{GUARDIAN_USER}](tg://user?id={DinoGuardian})"


# pic
gban_pic = "./userbot/resources/pics/gban.mp4"
main_pic = "./userbot/resources/pics/main.jpg"
core_pic = "./userbot/resources/pics/core.jpg"
chup_pic = "./userbot/resources/pics/chup.mp4"
bsdk_pic = "./userbot/resources/pics/bsdk.jpg"
bsdkwale_pic = "./userbot/resources/pics/bsdk_wale.jpg"
chutiya_pic = "./userbot/resources/pics/chutiya.jpg"
promote_pic = "./userbot/resources/pics/promote.jpg"
demote_pic = "./userbot/resources/pics/demote.jpg"
mute_pic = "./userbot/resources/pics/mute.jpg"
ban_pic = "./userbot/resources/pics/ban.jpg"


# channel
my_channel = Config.YOUR_CHANNEL or "GuardianBot_AI"
my_group = Config.YOUR_GROUP or "GuardianBot_Support"
if "@" in my_channel:
    my_channel = my_channel.replace("@", "")
if "@" in my_group:
    my_group = my_group.replace("@", "")

# My Channel
chnl_link = "https://t.me/GuardianBot_AI"
Guardian_channel = f"[𝐓𝐇𝐄 𝐆𝐔𝐀𝐑𝐃𝐈𝐀𝐍𝐁𝐎𝐓 ]({chnl_link})"
grp_link = "https://t.me/GuardianBot_Support"
Guardian_grp = f"[𝐓𝐇𝐄 𝐆𝐔𝐀𝐑𝐃𝐈𝐀𝐍𝐁𝐎𝐓 ]({grp_link})"


PM_START = []
PMMESSAGE_CACHE = {}
PMMENU = "pmpermit_menu" not in Config.NO_LOAD


TMP_DOWNLOAD_DIRECTORY = Config.TMP_DOWNLOAD_DIRECTORY

# spamwatch support
if Config.SPAMWATCH_API:
    token = Config.SPAMWATCH_API
    spamwatch = spam_watch.Client(token)
else:
    spamwatch = None


# ================================================

if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
    os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)


# thumb image
if Config.THUMB_IMAGE is not None:
    check = url(Config.THUMB_IMAGE)
    if check:
        try:
            with open(thumb_image_path, "wb") as f:
                f.write(requests.get(Config.THUMB_IMAGE).content)
        except Exception as e:
            LOGS.info(str(e))


def set_key(dictionary, key, value):
    if key not in dictionary:
        dictionary[key] = value
    elif isinstance(dictionary[key], list):
        if value in dictionary[key]:
            return
        dictionary[key].append(value)
    else:
        dictionary[key] = [dictionary[key], value]


async def make_gif(event, reply, quality=None, fps=None):
    fps = fps or 1
    quality = quality or 256
    result_p = os.path.join("temp", "animation.gif")
    animation = lottie.parsers.tgs.parse_tgs(reply)
    with open(result_p, "wb") as result:
        await _guardianutils.run_sync(
            lottie.exporters.gif.export_gif, animation, result, quality, fps
        )
    return result_p
