import json
import asyncio
import sys
import shlex
import re
import os
import inspect
import socket

try:
    import mistune
    from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia
    from quamash import QEventLoop
    import websockets
    from getpass import getpass

except ModuleNotFoundError:
    print("Make sure to install the dependencies in requirements.txt before running the program!")
    sys.exit(1)

if os.name == "nt":
    import ctypes
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(u"Dapper.RWCI.Client.1.0")

from datetime import datetime

from utils.ui.main_window import Ui_MainWindow
from utils.ui.login_widget import Ui_LoginWindow

from utils.html_colors import paint, attr
from utils import config
from utils import mistune_custom

TIME_FORMAT = "%H:%M:%S"

BLANK_HTML = '''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><style type="text/css">
p, li { white-space: pre-wrap; }
</style></head><body style=" font-family:'Consolas'; font-size:10pt; font-weight:400; font-style:normal;">
<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p></body></html>
'''

SCROLLBAR_STYLE = '''
QScrollBar:vertical {
    background: transparent;
    border: transparent;
    width: 15px;
    margin: 22px 0 22px 0;
}

QScrollBar::handle:vertical {
    background: #00bfa5;
    min-height: 20px;
}

QScrollBar::add-line:vertical {
    border: transparent;
    background: transparent;
    height: 20px;
    border-width: 2px 0 0 0;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}

QScrollBar::sub-line:vertical {
    border: transparent;
    background: transparent;
    height: 20px;
    border-width: 0 0 2px 0;
    subcontrol-position: top;
    subcontrol-origin: margin;
}

QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
    border: transparent;
    width: 9px;
    height: 9px;
    background: transparent;
}

 QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
     background: #515151;
 }
'''

class TextHistoryHandler(QtWidgets.QWidget):
    def __init__(self, client):
        QtWidgets.QWidget.__init__(self)

        self.client = client
        self.history = [""]
        self.history_index = 0

    def add_history(self, text):
        if (len(self.history) > 1 and self.history[1] != text) or len(self.history) == 1:
            self.history.insert(1, text)

    def restore_last_line(self):
        self.client.MessageField.setText(self.history[self.history_index])

        self.client.MessageField.setFocus()

    def eventFilter(self, source, event):
        if source is self.client.MessageField and event.type() == QtCore.QEvent.KeyPress:
            key = event.key()

            if key == QtCore.Qt.Key_Up:
                if self.history_index < (len(self.history) - 1):
                    self.history_index += 2
                    self.restore_last_line()

                return 1

            elif key == QtCore.Qt.Key_Down:
                if self.history_index > 0:
                    self.history_index -= 1
                    self.restore_last_line()

                return 1

        return QtWidgets.QWidget.eventFilter(self, source, event)

class RWCIClient(Ui_MainWindow):
    def __init__(self):
        self.user_list = []
        self.channel_list = {}

        self.events = {}
        self.commands = {} # Valid fields are `func`, and `docs`, dict is indexed by `name`

        self.quick_settings = {
            "active_channel": "",
            "default_channel": "",
            "last_dm": "",
            "debug": any("debug" in arg.lower() for arg in sys.argv),
        }

        app = QtWidgets.QApplication(sys.argv)
        loop = QEventLoop(app)
        asyncio.set_event_loop(loop)

        self.loop = loop
        self.user_colors = config.Config("user_colors.json")

        mistune_renderer = mistune_custom.Renderer()
        mistune_lexer = mistune_custom.InlineLexer(mistune_renderer)

        mistune_lexer.enable_underscore()

        self.markdown = mistune.Markdown(mistune_renderer, inline=mistune_lexer)

        self.history_handler = TextHistoryHandler(self)

    # Command decorator
    def command(self, *args, **kwargs):

        def decorator(function):
            func_name = kwargs.get("name", function.__name__)

            if func_name not in self.commands:
                self.commands[func_name] = {"func": function, "docs": inspect.cleandoc(function.__doc__ if function.__doc__ else "")}

        return decorator

    # Kludgy hack for asyncio
    async def _run_event(self, event, *args):
        try:
            await getattr(self, event)(*args)

        except:
            pass

    # More hax
    async def _run_command(self, name, *args, **kwargs):
        try:
            await self.commands[name]["func"](*args, **kwargs)

        except:
            pass

    def dispatch(self, event, *args):
        method = "on_" + event

        if self.quick_settings["debug"]:
            self.print_local_message(f"DISP {method}", plain=True)

        if hasattr(self, method):
            asyncio.ensure_future(self._run_event(method, *args), loop=self.loop)

    def run_command(self, func_name, word_list):
        if self.quick_settings["debug"]:
            self.print_local_message(f"COMD {func_name}", plain=True)

        if func_name in self.commands:
            arg_list = []
            kwarg_list = {}

            command = self.commands[func_name]
            func_sig = inspect.signature(command["func"])

            params = list(func_sig.parameters.items())

            for name, param in params:

                if name != "self":
                    transformer = param.annotation if param.annotation is not inspect._empty else str

                    if len(word_list) > 0 or (param.default is not inspect._empty):

                        if param.kind == param.POSITIONAL_OR_KEYWORD:
                            try:
                                arg = transformer(word_list[0])

                            except ValueError as e:
                                self.print_local_message(f"Failed converting '{name}' for {func_name}: {e}", error=True)
                                return

                            except Exception as e:
                                print(e)

                            del word_list[0]
                            arg_list.append(arg)

                        elif param.kind == param.KEYWORD_ONLY:
                            raw_arg = " ".join(word_list)
                            try:
                                arg = transformer(raw_arg)

                            except ValueError as e:
                                self.print_local_message(f"Failed converting '{name}' for {func_name}: {e}", error=True)
                                return

                            except Exception as e:
                                print(e)

                            kwarg_list[name] = arg
                            break

                    else:
                        self.print_local_message(f"Not enough arguments for {func_name}. Usage: {command['docs']}", warning=True)
                        return

            asyncio.ensure_future(self._run_command(func_name, *arg_list, **kwarg_list))

        else:
            self.print_local_message(f"'{func_name}' isn't a valid command", error=True)

    # Utility functions

    def _find_in(self, search_in, search):
        for item in search_in:
            if item[:len(search)].lower().strip() == search.lower().strip():
                return item

    def find_user(self, name):
        return self._find_in(self.user_list, name)

    def find_channel(self, name):
        return self._find_in(list(self.channel_list.keys()), name)

    def clear(self):
        for channel in self.channel_list:
            channel["html"] = BLANK_HTML

        self.update_view()

    def parse_formatting(self, text):
        if self.settings.get("should_render_markdown"):
            return self.markdown(text)
        else:
            return text

    def scroll_messages(self, up=False):
        scrollbar = self.MessageView.verticalScrollBar()

        if up:
            scrollbar.setValue(scrollbar.minimum())
        else:
            scrollbar.setValue(scrollbar.maximum())

    def update_view(self):
        if len(self.channel_list) > 0:
            self.MessageView.setHtml(self.channel_list[self.quick_settings["active_channel"]]["html"])

        self.scroll_messages()

    def update_channel_list(self):
        channel_str = "[==] Channels [==]<br /><br />"

        for channel_name, channel in list(self.channel_list.items()):
            if channel_name == self.quick_settings["active_channel"]:
                channel_str += f"# &gt; {paint(channel_name, 'green')} &lt;<br />"
            elif channel["mentioned_in"]:
                channel_str += f"# {paint(channel_name, 'a_deep_orange')} !<br />"
            else:
                channel_str += f"# {channel_name}{' *' if channel['new_messages'] else ''}<br />"

        self.ChannelView.setHtml(channel_str)

    def update_user_list(self):
        user_str = "&lt;--&gt; Online Users &lt;--&gt;<br /><br />"

        for user in self.user_list:
            user_str += f"{user}{paint(' X', 'red') if user.lower() in self.settings.get('blocked_users') else ''}<br />"

        self.OnlineUsersView.setHtml(user_str)

    def add_text(self, text, channel=""):
        if len(self.channel_list) == 0:
            self.MessageView.append(text)

        else:
            if channel:
                self.channel_list[channel]["html"] += "<br />" + text

            else:
                for channel in list(self.channel_list.keys()):
                    self.channel_list[channel]["html"] += "<br />" + text

        self.update_view()

    def mentioned_in(self, text):
        return f"@{self.username.lower()}" in text.lower()

    async def close(self, complete=False):
        self.connect_task.cancel()
        try:
            await self.ws.close()

        except:
            pass

        if complete:
            self.window.close()
            sys.exit()

    def decode_data(self, data):
        try:
            data = json.loads(data)

        except:
            pass

        return data

    # Output functions

    def print_player_message(self, message, author, channel):
        low_author = author.lower()
        if low_author not in self.settings.get("blocked_users"):
            color = self.user_colors.get(low_author, "white")
            text = self.parse_formatting(message)
            timestamp = datetime.now().strftime(TIME_FORMAT)

            text_color = "white"
            if self.mentioned_in(message):
                text_color = "a_orange"

            self.add_text(f"[{paint(timestamp, 'red')}] {paint(author, color)}: {paint(text, text_color)}", channel)

    def print_server_broadcast(self, message):
        color = "deep_purple"
        text = self.parse_formatting(message)
        timestamp = datetime.now().strftime(TIME_FORMAT)

        self.add_text(f"[{paint(timestamp, 'red')}] &lt;| SERVER |&gt; {paint(text, color)}")

    def print_direct_message(self, author, recipient, message):
        author_color = "amber"
        recipient_color = "deep_orange"
        text = self.parse_formatting(message)
        timestamp = datetime.now().strftime(TIME_FORMAT)

        self.add_text(f"[{paint(timestamp, 'red')}] [{paint(author, author_color)} -> {paint(recipient, recipient_color)}]: {text}")

    def print_user_join(self, username):
        self.add_text(paint(f"+ {username} joined", "a_blue"))

    def print_user_quit(self, username):
        self.add_text(paint(f"- {username} left", "a_red"))

    def print_local_message(self, message, plain=False, **kwargs):
        if kwargs.get("error"):
            color = "red"
        elif kwargs.get("warning"):
            color = "orange"
        elif kwargs.get("success"):
            color = "green"
        else:
            color = "cyan"

        if plain:
            response = f"|  {paint(message, color)}"
        else:
            response = f"&lt;&lt; {paint(message, color)} &gt;&gt;"

        self.add_text(response)

    # Data sending

    async def _raw_send(self, raw_data):
        try:
            if isinstance(raw_data, dict):
                data = json.dumps(raw_data)
            if self.quick_settings["debug"]:
                self.print_local_message(f"SEND {raw_data if raw_data['type'] != 'auth' else 'AUTH [REDACTED]'}")

            await self.ws.send(data)

        except websockets.exceptions.ConnectionClosed:
            self.print_local_message("Server unexpectedly closed", error=True)
            await self.close()

    async def send_message(self, message):
        if message:
            payload = {
                "type": "message",
                "channel": self.quick_settings["active_channel"],
                "message": message
            }

            await self._raw_send(payload)

    async def send_auth(self):
        payload = {
            "type": "auth",
            "username": self.username,
            "password": self.password
        }

        await self._raw_send(payload)

    async def send_direct_message(self, recipient, message):
        if message:
            payload = {
                "type": "direct_message",
                "recipient": recipient,
                "message": message
            }

            await self._raw_send(payload)

    async def send_typing(self):
        payload = {
            "type": "typing"
        }

        await self._raw_send(payload)

    # Data handling

    async def poll(self):
        try:
            data = await self.ws.recv()
            await self.process_data(data)

        except websockets.exceptions.ConnectionClosed:
            self.print_local_message("Server unexpectedly closed", error=True)
            await self.close()

    async def process_data(self, data):
        message = self.decode_data(data)

        if isinstance(message, dict):
            packet_type = message.get("type")

            if self.quick_settings["debug"]:
                self.print_local_message(f"RECV {data}", plain=True)

            if packet_type in ["message", "broadcast", "auth", "join", "quit", "direct_message", "user_list", "channel_list", "default_channel", "channel_create", "channel_delete"]:
                self.dispatch(packet_type, message)

            else:
                if self.quick_settings["debug"]:
                    self.print_local_message(f"Unknown packet type: {data}", plain=True, warning=True)



    async def process_command(self, text):
        text = text.strip()

        try:
            parts = shlex.split(text[1:])

        except:
            parts = text[1:].split()

        command_name = parts[0]
        self.run_command(command_name, parts[1:])

    # Connection functions

    def read_input(self):
        text = self.MessageField.text()

        self.history_handler.add_history(text)

        if text.startswith("/"):
            asyncio.run_coroutine_threadsafe(self.process_command(text), self.loop)
        else:
            asyncio.run_coroutine_threadsafe(self.send_message(text), self.loop)

        self.MessageField.clear()

    async def connect(self):
        self.print_local_message("Attempting connection..", plain=True)
        try:
            self.ws = await websockets.client.connect(f"ws://{self.ip}:{self.port}")

        except socket.gaierror:
            self.print_local_message(f"Unable to resolve {self.ip}:{self.port}", error=True)
            await self.close()

        await self.send_auth()
        self.print_local_message("Successfully connected to RWCI server", plain=True, success=True)

        while self.ws.open:
            await self.poll()

    # Dispatcher events

    async def on_message(self, data):
        channel = data["channel"]
        message = data["message"]

        if channel != self.quick_settings["active_channel"]:
            if self.mentioned_in(message):
                self.channel_list[channel]["mentioned_in"] = True
                # self.alert_tone.play()

            else:
                self.channel_list[channel]["new_messages"] = True

        self.update_channel_list()

        self.print_player_message(message, data["author"], channel)

    async def on_broadcast(self, data):
        self.print_server_broadcast(data["message"])

    async def on_auth(self, data):
        status = data["success"]
        registered = data["new_account"]

        if status:
            if registered:
                self.print_local_message("Registered and logged in ok", warning=True)
            else:
                self.print_local_message("Logged in ok", success=True)
        else:
            self.print_local_message("Login failed", error=True)

    async def on_join(self, data):
        username = data["username"]
        self.print_user_join(username)

        if username not in self.user_list:
            self.user_list.append(username)

            self.update_user_list()

    async def on_quit(self, data):
        username = data["username"]
        self.print_user_quit(username)

        if username in self.user_list:
            self.user_list.remove(username)

            self.update_user_list()

    async def on_direct_message(self, data):
        self.quick_settings["last_dm"] = data["author"]
        self.print_direct_message(data["author"], "Me", data["message"])

    async def on_user_list(self, data):
        self.user_list = data["users"]
        self.update_user_list()

    async def on_channel_list(self, data):
        for channel_name in data["channels"]:
            self.channel_list[channel_name] = {"html": self.MessageView.toHtml(), "mentioned_in": False, "new_messages": False}

    async def on_default_channel(self, data):
        self.quick_settings["active_channel"] = data["channel"]
        self.quick_settings["default_channel"] = data["channel"]

        self.update_channel_list()
        self.update_view()

    async def on_channel_create(self, data):
        self.channel_list[data["channel"]] = {"html": BLANK_HTML, "mentioned_in": False, "new_messages": False}

        self.update_channel_list()

    async def on_channel_delete(self, data):
        if self.quick_settings["active_channel"] == data["channel"]:
            self.quick_settings["active_channel"] = self.quick_settings["default_channel"]

        del self.channel_list[data["channel"]]
        self.update_channel_list()

    def __call__(self, window, username, password, settings):
        self.username = username
        self.password = password
        self.settings = settings

        self.ip = self.settings.get("server_ip")
        self.port = self.settings.get("server_port")

        self.window = window

        Ui_MainWindow.__init__(self)

        self.setupUi(window)
        window.setWindowIcon(QtGui.QIcon("./utils/ui/files/icon.png"))

        # self.alert_tone = QtMultimedia.QSound("./utils/ui/files/alert.wav")

        self.MessageView.verticalScrollBar().setStyleSheet(SCROLLBAR_STYLE)
        self.ChannelView.verticalScrollBar().setStyleSheet(SCROLLBAR_STYLE)
        self.OnlineUsersView.verticalScrollBar().setStyleSheet(SCROLLBAR_STYLE)

        self.MessageField.installEventFilter(self.history_handler)
        self.MessageField.returnPressed.connect(self.read_input)
        self.MessageField.setFocus()

        self.connect_task = self.loop.create_task(self.connect())

client = RWCIClient()

@client.command(name="help")
async def command_help(*, command_name=""):
    if command_name:
        if command_name in client.commands:
            client.print_local_message(f"{command_name} - {client.commands[command_name]['docs']}", plain=True)
    else:
        client.print_local_message(f"{len(client.commands)} commands")
        for command_name, command in list(client.commands.items()):
            client.print_local_message(f"{command_name} - {command['docs']}", plain=True)

@client.command(name="color")
async def command_color(color_name, *, user_name):
    """/color color_name user_name"""
    username = client.find_user(user_name)

    if username:
        await client.user_colors.put(username.lower(), color_name)

        client.print_local_message(f"Set {username}'s color to {color_name}", success=True)

    else:
        client.print_local_message(f"'{user_name}' isn't online", error=True)

@client.command(name="clear_color")
async def command_clear_color(*, user_name):
    """/clear_color user_name"""
    username = client.find_user(user_name)

    if username:
        user = username.lower()

        if user in client.user_colors:
            await client.user_colors.remove(user)
            client.print_local_message(f"Removed {username}'s color", success=True)

        else:
            client.print_local_message(f"{username} has no color set", warning=True)

    else:
        client.print_local_message(f"'{user_name}' isn't online", error=True)

@client.command(name="me")
async def command_me(*, message):
    """/me message"""
    await client.send_message(f"*{message}*")

@client.command(name="quit")
async def command_quit():
    """/quit"""
    client.print_local_message("Exited", plain=True)
    await client.close(complete=True)

@client.command(name="block")
async def command_block(*, user_name):
    """/block user_name"""
    username = client.find_user(user_name)

    if username:
        user = username.lower()

        if user in client.settings.get("blocked_users"):
            client.settings.get("blocked_users").remove(user)
            client.print_local_message(f"Unblocked {username}")

        else:
            client.settings.get("blocked_users").append(user)
            client.print_local_message(f"Blocked {username}")

        await client.settings.save()
        client.update_user_list()

    else:
        client.print_local_message(f"'{user_name}' isn't online", error=True)

@client.command(name="blocked")
async def command_blocked():
    """/blocked"""
    blocked_users = client.settings.get("blocked_users")
    client.print_local_message(f"{len(blocked_users)} users blocked")
    for user in blocked_users:
        client.print_local_message(user, plain=True)

@client.command(name="who")
async def command_who():
    """/who"""
    client.print_local_message(f"{len(client.user_list)} users online")
    for user in client.user_list:
        client.print_local_message(user, plain=True)

@client.command(name="w")
async def command_w(recipient, *, message):
    """/w recipient message"""
    username = client.find_user(recipient)

    if username:
        if (username.lower() != client.username.lower()) or (username.lower() == client.username.lower() and client.quick_settings["debug"]):
            await client.send_direct_message(username, message)
            client.print_direct_message("Me", username, message)

        elif client.quick_settings["debug"] is False:
            client.print_local_message("You can't DM yourself!", error=True)

    else:
        client.print_local_message(f"'{recipient}' isn't online", error=True)

@client.command(name="clean")
async def command_clean():
    """/clean"""
    client.clean()

@client.command(name="eval")
async def command_eval(*, code):
    """/eval code"""
    try:
        precompiled = compile(code, "<eval>", "eval")
        result = eval(precompiled)

    except SyntaxError as e:
        client.print_local_message(f"{e.text}")
        client.print_local_message(f"{'^':>{e.offset}}", plain=True)
        client.print_local_message(f"{type(e).__name__}: {e}", plain=True, error=True)
        return

    except Exception as e:
        client.print_local_message(f"{type(e).__name__}: {e}", plain=True, error=True)
        return

    if inspect.isawaitable(result):
        result = await result

    result = str(result)

    client.print_local_message(result, plain=True, success=True)

@client.command(name="markdown")
async def command_markdown():
    """/markdown"""
    await client.settings.put("should_render_markdown", not client.settings.get("should_render_markdown"))

    if client.settings.get("should_render_markdown"):
        client.print_local_message("Enabled markdown rendering!")

    else:
        client.print_local_message("Disabled markdown rendering!")

@client.command(name="json")
async def command_json(*, json_data):
    """/json json_data"""
    await client._raw_send(json_data)
    client.print_local_message("Sent!")

@client.command(name="debug")
async def command_debug():
    """/debug"""
    client.quick_settings["debug"] = not client.quick_settings["debug"]

    if client.quick_settings["debug"]:
        client.print_local_message("Debug mode enabled")

    else:
        client.print_local_message("Debug mode disabled")

@client.command(name="join")
async def command_join(*, channel_name):
    """/join channel_name"""
    channel = client.find_channel(channel_name)

    if channel and channel in client.channel_list:
        client.quick_settings["active_channel"] = channel
        client.channel_list[channel]["new_messages"] = False
        client.channel_list[channel]["mentioned_in"] = False

        client.print_local_message(f"Joined #{channel}", plain=True, success=True)

        client.update_channel_list()
        client.update_view()

    else:
        client.print_local_message(f"'{channel_name}' isn't available", error=True)

@client.command(name="r")
async def command_r(*, message):
    """/r message"""
    if client.quick_settings["last_dm"] in client.user_list:
        await client.send_direct_message[client.quick_settings["last_dm"], message]
        client.print_direct_message("me", client.quick_settings["last_dm"], message)

class LoginHandler(Ui_LoginWindow):
    def __init__(self, window):
        self.settings = config.Config("settings.json", default={"blocked_users": [], "server_ip": "", "server_port": "", "should_render_markdown": True})
        self.window = window

        Ui_LoginWindow.__init__(self)
        self.setupUi(window)
        window.setWindowIcon(QtGui.QIcon("./utils/ui/files/icon.png"))

        server_ip = self.settings.get("server_ip")
        server_port = self.settings.get("server_port")
        do_markdown = self.settings.get("should_render_markdown")

        if server_ip:
            self.AddressField.setText(server_ip)

        if server_port:
            self.PortField.setText(server_port)

        if isinstance(do_markdown, bool):
            self.MarkdownCheck.setChecked(do_markdown)
        else:
            do_markdown = True
            self.MarkdownCheck.setChecked(True)

        self.LoginButton.clicked.connect(self.validate_input)

    def validate_input(self):
        self.ErrorText.setText("")

        server_ip = self.AddressField.text()
        server_port = self.PortField.text()

        try:
            socket.getaddrinfo(server_ip, server_port)

        except socket.gaierror:
            self.ErrorText.setText("IP address could not be resolved")
            return

        try:
            port = int(server_port)
            assert(port <= 65535 and port >= 1)

        except ValueError:
            self.ErrorText.setText("Port is not an integer")
            return

        except AssertionError:
            self.ErrorText.setText("Port is not a valid port number")

        username = self.UsernameField.text()
        password = self.PasswordField.text()

        if (len(username) > 32) or (len(password) > 32):
            self.ErrorText.setText("Usernames and passwords are limited to 32 characters")

        self.settings._db["server_ip"] = server_ip
        self.settings._db["server_port"] = server_port
        self.settings._db["should_render_markdown"] = self.MarkdownCheck.isChecked()
        self.settings._dump()

        self.window.close()

        window = QtWidgets.QMainWindow()

        client(window, username, password, self.settings)
        window.setWindowTitle(f"RWCI Client - {username}")

        window.show()

loop = asyncio.get_event_loop()
window = QtWidgets.QMainWindow()

login_handler = LoginHandler(window)
window.setWindowTitle("RWCI Login")

window.show()
with loop:
    loop.run_forever()

sys.exit()