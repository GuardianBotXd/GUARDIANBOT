import importlib
import sys
from pathlib import Path

from userbot import CMD_HELP, LOAD_PLUG

from ..Config import Config
from ..core import LOADED_CMDS, PLG_INFO
from ..core.logger import logging
from ..core.managers import eod, eor
from ..core.session import guardian
from ..helpers.tools import media_type
from ..helpers.utils import _format, _guardiantools, _guardianutils, install_pip, reply_id
from .decorators import admin_cmd, sudo_cmd

LOGS = logging.getLogger("GuardianUserBot")


def load_module(shortname, plugin_path=None):
    if shortname.startswith("__"):
        pass
    elif shortname.endswith("_"):
        path = Path(f"userbot/plugins/{shortname}.py")
        checkplugins(path)
        name = "userbot.plugins.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        LOGS.info("Successfully imported " + shortname)
    else:
        if plugin_path is None:
            path = Path(f"userbot/plugins/{shortname}.py")
            name = f"userbot.plugins.{shortname}"
        else:
            path = Path((f"{plugin_path}/{shortname}.py"))
            name = f"{plugin_path}/{shortname}".replace("/", ".")
        checkplugins(path)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        mod.bot = guardian
        mod.LOGS = LOGS
        mod.Config = Config
        mod._format = _format
        mod.tgbot = guardian.tgbot
        mod.sudo_cmd = sudo_cmd
        mod.CMD_HELP = CMD_HELP
        mod.reply_id = reply_id
        mod.admin_cmd = admin_cmd
        mod._guardianutils = _guardianutils
        mod._guardiantools = _guardiantools
        mod.media_type = media_type
        mod.eod = eod
        mod.install_pip = install_pip
        mod.parse_pre = _format.parse_pre
        mod.eor = eor
        mod.logger = logging.getLogger(shortname)
        mod.borg = guardian
        spec.loader.exec_module(mod)
        # for imports
        sys.modules["userbot.plugins." + shortname] = mod
        LOGS.info("GuardianBot " + shortname)


def start_spam(shortname):
    if shortname.startswith("__"):
        pass
    elif shortname.endswith("_"):
        import importlib
        import sys
        from pathlib import Path

        path = Path(f"userbot/plugins/Spam/{shortname}.py")
        name = "userbot.plugins.Spam.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        print("Starting Your Spam Bot.")
        print("SpamBot Sucessfully imported " + shortname)
    else:
        import importlib
        import sys
        from pathlib import Path

        path = Path(f"userbot/plugins/Spam/{shortname}.py")
        name = "userbot.plugins.Spam.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        mod.tgbot = guardian.tgbot
        spec.loader.exec_module(mod)
        sys.modules["Spam" + shortname] = mod
        print("[🔰Spam🔰 3.0] ~ HAS ~ 💞Installed💞 ~" + shortname)


def remove_plugin(shortname):
    try:
        cmd = []
        if shortname in PLG_INFO:
            cmd += PLG_INFO[shortname]
        else:
            cmd = [shortname]
        for cmdname in cmd:
            if cmdname in LOADED_CMDS:
                for i in LOADED_CMDS[cmdname]:
                    guardian.remove_event_handler(i)
                del LOADED_CMDS[cmdname]
        return True
    except Exception as e:
        LOGS.error(e)
    try:
        for i in LOAD_PLUG[shortname]:
            guardian.remove_event_handler(i)
        del LOAD_PLUG[shortname]
    except BaseException:
        pass
    try:
        name = f"userbot.plugins.{shortname}"
        for i in reversed(range(len(guardian._event_builders))):
            ev, cb = guardian._event_builders[i]
            if cb.__module__ == name:
                del guardian._event_builders[i]
    except BaseException:
        raise ValueError


def checkplugins(filename):
    with open(filename, "r") as f:
        filedata = f.read()
    filedata = filedata.replace("sendmessage", "send_message")
    filedata = filedata.replace("sendfile", "send_file")
    filedata = filedata.replace("editmessage", "edit_message")
    with open(filename, "w") as f:
        f.write(filedata)
