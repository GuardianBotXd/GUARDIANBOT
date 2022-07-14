import glob
import os
import sys
from datetime import timedelta
from pathlib import Path

from telethon import Button, functions, types, utils
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest

from userbot import BOTLOG, BOTLOG_CHATID, PM_LOGGER_GROUP_ID

from ..Config import Config
from ..core.logger import logging
from ..core.session import guardian
from ..helpers.utils import install_pip
from ..sql_helper.global_collection import (
    del_keyword_collectionlist,
    get_item_collectionlist,
)
from ..sql_helper.globals import addgvar, gvarstatus
from .pluginmanager import load_module, start_spam
from .tools import create_supergroup

ENV = bool(os.environ.get("ENV", False))

LOGS = logging.getLogger("GuardianUserBot")
cmdhr = Config.HANDLER


if ENV:
    VPS_NOLOAD = ["vps"]
elif os.path.exists("config.py"):
    VPS_NOLOAD = ["heroku"]


async def setup_bot():
    """
    To set up bot for userbot
    """
    try:
        await guardian.connect()
        config = await guardian(functions.help.GetConfigRequest())
        for option in config.dc_options:
            if option.ip_address == guardian.session.server_address:
                if guardian.session.dc_id != option.id:
                    LOGS.warning(
                        f"Fixed DC ID in session from {guardian.session.dc_id}"
                        f" to {option.id}"
                    )
                guardian.session.set_dc(option.id, option.ip_address, option.port)
                guardiam.session.save()
                break
        bot_details = await guardian.tgbot.get_me()
        Config.BOT_USERNAME = f"@{bot_details.username}"
        guardian.me = await guardian.get_me()
        guardian.uid = guardian.tgbot.uid = utils.get_peer_id(guardian.me)
        if Config.OWNER_ID == 0:
            Config.OWNER_ID = utils.get_peer_id(guardian.me)
    except Exception as e:
        LOGS.error(f"GUARDIAN_STRING - {e}")
        sys.exit()


async def startupmessage():
    """
    Start up message in telegram logger group
    """
    try:
        if BOTLOG:
            Config.GUARDIANUBLOGO = await guardian.tgbot.send_file(
                BOTLOG_CHATID,
                "https://telegra.ph/file/992bb3e9e8863f6492b94.jpg",
                caption="**Your GuardianBot has been started successfully.**",
                buttons=[(Button.url("Support", "https://t.me/GuardianBot_Support"),)],
            )
    except Exception as e:
        LOGS.error(e)
        return None
    try:
        msg_details = list(get_item_collectionlist("restart_update"))
        if msg_details:
            msg_details = msg_details[0]
    except Exception as e:
        LOGS.error(e)
        return None
    try:
        if msg_details:
            await guardian.check_testcases()
            message = await guardian.get_messages(msg_details[0], ids=msg_details[1])
            text = message.text + "\n\n**Ok Bot is Back and Alive.**"
            await guardian.edit_message(msg_details[0], msg_details[1], text)
            if gvarstatus("restartupdate") is not None:
                await guardian.send_message(
                    msg_details[0],
                    f"{cmdhr}ping -a",
                    reply_to=msg_details[1],
                    schedule=timedelta(seconds=10),
                )
            del_keyword_collectionlist("restart_update")
    except Exception as e:
        LOGS.error(e)
        return None


async def add_bot_to_logger_group(chat_id):
    """
    To add bot to logger groups
    """
    bot_details = await guardian.tgbot.get_me()
    lol = bot_details.username
    addgvar("BOT_USERNAME", lol)
    try:
        await guardian(
            functions.messages.AddChatUserRequest(
                chat_id=chat_id,
                user_id=lol,
                fwd_limit=1000000,
            )
        )
    except BaseException:
        try:
            await guardian(
                functions.channels.InviteToChannelRequest(
                    channel=chat_id,
                    users=[lol],
                )
            )
        except Exception as e:
            LOGS.error(str(e))


async def load_plugins(folder):
    """
    To load plugins from the mentioned folder
    """
    path = f"userbot/{folder}/*.py"
    plugin_path = f"userbot/{folder}"
    files = glob.glob(path)
    files.sort()
    success = 0
    failure = []
    for name in files:
        with open(name) as f:
            path1 = Path(f.name)
            shortname = path1.stem
            pluginname = shortname.replace(".py", "")
            try:
                if (pluginname not in Config.NO_LOAD) and (
                    pluginname not in VPS_NOLOAD
                ):
                    flag = True
                    check = 0
                    while flag:
                        try:
                            load_module(
                                pluginname,
                                plugin_path=plugin_path,
                            )
                            if shortname in failure:
                                failure.remove(shortname)
                            success += 1
                            break
                        except ModuleNotFoundError as e:
                            install_pip(e.name)
                            check += 1
                            if shortname not in failure:
                                failure.append(shortname)
                            if check > 5:
                                break
                else:
                    os.remove(Path(f"userbot/{folder}/{shortname}.py"))
            except Exception as e:
                if shortname not in failure:
                    failure.append(shortname)
                os.remove(Path(f"{plugin_path}/{shortname}.py"))
                LOGS.info(
                    f"unable to load {shortname} because of error {e}\nBase Folder {plugin_path}"
                )
            LOGS.info(f'Imported : {success} Plugins \nFailed : {", ".join(failure)}')


async def hekp():
    try:
        os.environ[
            "GUARDIAN_STRING"
        ] = "String Is A Sensitive Data \nSo Its Protected By GuardianBot"
    except Exception as e:
        print(str(e))
    try:
        await guardian(JoinChannelRequest("@GuardianBot_Support"))
    except BaseException:
        pass
    try:
        await guardian(LeaveChannelRequest("@GuardianBot_AI"))
    except BaseException:
        pass
    try:
        await guardian(LeaveChannelRequest("@GuardianCommunity"))
    except BaseException:
        pass


spam = Config.SPAM


async def scammer(username):
    i = 0
    xx = 0
    async for x in guardian.iter_dialogs():
        if x.is_group or x.is_channel:
            try:
                await guardian.edit_permissions(x.id, username, view_messages=False)
                i += 1
            except:
                xx += 1
    print(f"OP {i-xx}")


async def spams():
    if spam == "ON":
        import glob

        path = "userbot/plugins/Spam/*.py"
        files = glob.glob(path)
        for name in files:
            with open(name) as f:
                path1 = Path(f.name)
                shortname = path1.stem
                start_spam(shortname.replace(".py", ""))
    else:
        print("⚠️Spam Not Loading⚠️")


async def verifyLoggerGroup():
    """
    Will verify the both loggers group
    """
    type = False
    if BOTLOG:
        try:
            entity = await guardian.get_entity(BOTLOG_CHATID)
            if not isinstance(entity, types.User) and not entity.creator:
                if entity.default_banned_rights.send_messages:
                    LOGS.info(
                        "Permissions missing to send messages for the specified PRIVATE_GROUP_BOT_API_ID."
                    )
                if entity.default_banned_rights.invite_users:
                    LOGS.info(
                        "Permissions missing to addusers for the specified PRIVATE_GROUP_BOT_API_ID."
                    )
        except ValueError:
            LOGS.error(
                "PRIVATE_GROUP_BOT_API_ID cannot be found. Make sure it's correct."
            )
        except TypeError:
            LOGS.error(
                "PRIVATE_GROUP_BOT_API_ID is unsupported. Make sure it's correct."
            )
        except Exception as e:
            LOGS.error(
                "An Exception occured upon trying to verify the PRIVATE_GROUP_BOT_API_ID.\n"
                + str(e)
            )
    else:
        descript = "Don't delete this group or change to group(If you change group all your previous snips, welcome will be lost.)"
        _, groupid = await create_supergroup(
            "GuardianBot Log Group", guardian, Config.BOT_USERNAME, descript
        )
        addgvar("PRIVATE_GROUP_BOT_API_ID", groupid)
        print(
            "Private Group for PRIVATE_GROUP_BOT_API_ID is created successfully and added to vars."
        )
        type = True
    if PM_LOGGER_GROUP_ID != -100:
        try:
            entity = await guardian.get_entity(PM_LOGGER_GROUP_ID)
            if not isinstance(entity, types.User) and not entity.creator:
                if entity.default_banned_rights.send_messages:
                    LOGS.info(
                        "Permissions missing to send messages for the specified PM_LOGGER_GROUP_ID."
                    )
                if entity.default_banned_rights.invite_users:
                    LOGS.info(
                        "Permissions missing to addusers for the specified PM_LOGGER_GROUP_ID."
                    )
        except ValueError:
            LOGS.error("PM_LOGGER_GROUP_ID cannot be found. Make sure it's correct.")
        except TypeError:
            LOGS.error("PM_LOGGER_GROUP_ID is unsupported. Make sure it's correct.")
        except Exception as e:
            LOGS.error(
                "An Exception occured upon trying to verify the PM_LOGGER_GROUP_ID.\n"
                + str(e)
            )
    if type:
        executable = sys.executable.replace(" ", "\\ ")
        args = [executable, "-m", "userbot"]
        os.execle(executable, *args, os.environ)
        sys.exit(0)
