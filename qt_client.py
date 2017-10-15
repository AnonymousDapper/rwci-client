import json
import asyncio
import sys
import shlex
import re
import os
import socket

try:
    import mistune
    from PyQt5 import QtCore, QtGui, QtWidgets
    from quamash import QEventLoop
    import websockets
except ModuleNotFoundError:
    print("Make sure to install the dependencies in qt_requirements.txt before running the program!")
    sys.exit(1)

if os.name == "nt":
    import ctypes
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(u"Dapper.RWCI.Client.02")

from datetime import datetime
from inspect import isawaitable
from getpass import getpass

from utils.ui.main_window_channels import Ui_MainWindow
from utils.ui.login_widget import Ui_LoginWindow

from utils.html_colors import paint, attr
from utils import time
from utils import config

LINK_EXTRACT = re.compile(r"^(https?|s?ftp|wss?:?)://([^\s/]+)/?")

class TextHistoryHandler(QtWidgets.QWidget):
    def __init__(self, client_window):
        QtWidgets.QWidget.__init__(self)
        self.client_window = client_window
        self.history = [""]
        self.history_index = 0

    def add_history(self, text):
        if self.history[0] != text:
            self.history.insert(1, text)

    def restore_last_line(self):
        self.client_window.MessageField.setText(self.history[self.history_index])

        self.client_window.MessageField.setFocus()

    def eventFilter(self, source, event):
        if source is self.client_window.MessageField and event.type() == QtCore.QEvent.KeyPress:
            key = event.key()

            if key == QtCore.Qt.Key_Up: # Up arrow
                if self.history_index < (len(self.history) - 1):
                    self.history_index += 1
                    self.restore_last_line()

                return 1

            elif key == QtCore.Qt.Key_Down: # Down arrow
                if self.history_index > 0:
                    self.history_index -= 1
                    self.restore_last_line()

                return 1

        return super().eventFilter(source, event)

class InlineLexer(mistune.InlineLexer):
    def enable_underscore(self):
        self.rules.underscore = re.compile(
            r"_"
            r"(.*?)"
            r"_"
        )
        self.default_rules.insert(3, "underscore")

    def output_underscore(self, match):
        text = match.group(1)
        return self.renderer.underscore(text)

class Renderer(mistune.Renderer):
    def double_emphasis(self, text):
        return attr(text, "bold")

    def emphasis(self, text):
        return attr(text, "italic")

    def underscore(self, text):
        return attr(text, "underscore")

    def strikethrough(self, text):
        return attr(text, "strikethru")

    def paragraph(self, text):
        return text

    def inline_html(self, html):
        return html

    def escape(self, text):
        return text

    def text(self, text):
        return text

    def block_html(self, html):
        return html

    def autolink(self, link, is_email=False):
        if is_email:
            return link

        return f"<a href={link} style=\"text-decoration: none\"><span style=\"color: #2196F3; text-decoration: none\">{link}</span></a>"

    def link(self, link, title, text):
        link_info = LINK_EXTRACT.match(link)
        if link_info is None:
            return link

        return f"<a href={link} style=\"text-decoration: none\"><span style=\"color: #2196F3; text-decoration: none\">{text}</span><span style=\"color: #BDBDBD; text-decoration: none\"> ({link_info.group(2)})</span></a>"

    def codespan(self, text):
        return paint(text, "a_green")

    def image(self, src, title, text):
        if title:
            return self.link(src, None, title)
        else:
            return self.url_link(src)

class Client(Ui_MainWindow):
    def __init__(self, dialog, username, password, settings):
        self._debug = any("debug" in arg.lower() for arg in sys.argv)
        self.username = username
        self.password = password
        self.mute = False
        self.user_list = []
        self.loop = asyncio.get_event_loop()
        self.user_colors = config.Config("qt_user_colors.json",)
        self.settings = settings

        self.ip = self.settings.get("server_ip")
        self.port = self.settings.get("server_port")

        renderer = Renderer()
        lexer = InlineLexer(renderer)

        lexer.enable_underscore()

        self.markdown = mistune.Markdown(renderer, inline=lexer)

        self.history_handler = TextHistoryHandler(self)

        Ui_MainWindow.__init__(self)
        self.setupUi(dialog)
        dialog.setWindowIcon(QtGui.QIcon("./utils/ui/files/icon.png"))

        self.MainWindow = dialog

        self.MessageField.installEventFilter(self.history_handler)

        self.MessageField.setFocus()

        self.MessageField.returnPressed.connect(self.read_input)

        self.connect_task = self.loop.create_task(self.connect())

    def dispatch(self, event, *args):
        method = "on_" + event
        if self._debug:
            self.print_local_message(f"DISP {method}", plain=True)
        if hasattr(self, method):
            asyncio.ensure_future(self._run_event(method, *args), loop=self.loop)

    def run_command(self, event, msg, *args):
        method = "command_" + event
        if self._debug:
            self.print_local_message(f"COMD {method}", plain=True)
        if hasattr(self, method):
            asyncio.ensure_future(self._run_event(method, msg, *args), loop=self.loop)
        else:
            self.print_local_message(f"Command '{event}' doesn't exist!", warning=True)

    async def _run_event(self, event, *args):
        try:
            await getattr(self, event)(*args)
        except:
            pass

    def find_user(self, name):
        for user in self.user_list:
            if user[:len(name)].lower().strip() == name.lower().strip():
                return user

    def parse_formatting(self, text):
        if self.settings.get("should_render_markdown") is True:
            return self.markdown(text)
        else:
            return text

    # Print Messages
    def add_text(self, text):
        text_field = self.MessageView

        if not self.mute:
            text_field.append(text)

    def clear(self):
        self.MessageBrowser.clear()

    def scroll_messages(self, up=False):
        if up:
            pass
        else:
            self.MessageScroller.ensureVisible(0, 123456789)

    def print_player_message(self, message, author):
        low_author = author.lower()
        if low_author in self.settings.get("blocked_users", []):
            return

        color = self.user_colors.get(low_author, "white")
        text = self.parse_formatting(message)
        timestamp = datetime.now().strftime(time.time_format)

        self.add_text(f"[{paint(timestamp, 'red')}] {paint(author, color)}: {text}")

    def print_server_broadcast(self, message):
        fg_color = "a_deep_purple"
        text = self.parse_formatting(message)
        timestamp = datetime.now().strftime(time.time_format)

        self.add_text(f"[{paint(timestamp, 'red')}] &lt;| SERVER |&gt; {paint(text, fg_color)}")

    def print_direct_message(self, author, recipient, message):
        author_color = "amber"
        recipient_color = "deep_orange"
        text = self.parse_formatting(message)
        timestamp = datetime.now().strftime(time.time_format)

        self.add_text(f"[{paint(timestamp, 'red')}] [{paint(author, author_color)} -> {paint(recipient, recipient_color)}]: {text}")

    def print_user_join(self, username):
        self.add_text(paint(f"+ {username} joined", "a_blue"))

    def print_user_quit(self, username):
        self.add_text(paint(f"- {username} left", "a_red"))

    def print_local_message(self, message, plain=False, **kwargs):
        if kwargs.get("error"):
            fg_color = "red"
        elif kwargs.get("warning"):
            fg_color = "orange"
        elif kwargs.get("success"):
            fg_color = "green"
        elif kwargs.get("info"):
            fg_color = "cyan"
        else:
            fg_color = "cyan"

        # text = self.parse_formatting(message)
        if plain:
            response = f"|  {paint(message, fg_color)}"
        else:
            response = f"&lt;&lt; {paint(message, fg_color)} &gt;&gt;"

        self.add_text(response)

    # Sending Data
    async def _raw_send(self, data):
        try:
            if isinstance(data, dict):
                data = json.dumps(data)
            if self._debug:
                self.print_local_message(f"SEND {data}", plain=True)

            await self.ws.send(data)
        except websockets.exceptions.ConnectionClosed as e:
            self.print_local_message(f"Server unexpectedly closed", error=True)
            await self.close()

    async def send_message(self, message):
        if message == "" or message is None:
            return

        payload = {
            "type": "message",
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
        if message == "" or message is None:
            return

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

    async def poll(self):
        try:
            data = await self.ws.recv()
            await self.process_data(data)
        except websockets.exceptions.ConnectionClosed as e:
            self.print_local_message("Server unexpectedly closed", error=True)
            await self.close()

    def decode_data(self, data):
        try:
            data = json.loads(data)
        except:
            pass
        return data

    async def process_data(self, data):
        message = self.decode_data(data)

        if not isinstance(message, dict):
            return

        packet_type = message.get("type")

        if self._debug:
            self.print_local_message(f"RECV {data}", plain=True)

        if packet_type == "message":
            self.dispatch("message", message)

        elif packet_type == "broadcast":
            self.dispatch("broadcast", message)

        elif packet_type == "auth":
            self.dispatch("auth_response", message)

        elif packet_type == "join":
            self.dispatch("join", message)

        elif packet_type == "quit":
            self.dispatch("quit", message)

        elif packet_type == "direct_message":
            self.dispatch("direct_message", message)

        elif packet_type == "user_list":
            self.dispatch("user_list", message)

        elif packet_type == "typing":
            self.dispatch("typing", message)

        else:
            if self._debug:
                self.print_local_message(f"Unknown Packet Type: {data}", plain=True, warning=True)

    async def process_command(self, text):
        try:
            parts = shlex.split(text[1:])
        except:
            parts = text[1:].split()

        command_name = parts[0]
        self.run_command(command_name, text[2 + len(command_name):], *parts[1:])

    # Connections
    def read_input(self):
        text = self.MessageField.text()

        self.history_handler.add_history(text)

        if text.startswith("/"):
            asyncio.run_coroutine_threadsafe(self.process_command(text), self.loop)
        else:
            asyncio.run_coroutine_threadsafe(self.send_message(text), self.loop)
        self.MessageField.clear()

    async def close(self, complete=False):
        self.connect_task.cancel()
        try:
            await self.ws.close()
        except:
            pass

        if complete:
            self.MainWindow.close()
            sys.exit()

    async def connect(self):
        self.print_local_message("Attempting connection..", plain=True)
        try:
            self.ws = await websockets.client.connect(f"ws://{self.ip}:{self.port}")
        except socket.gaierror:
            self.print_local_message(f"Unable to resolve {self.ip}")
            await self.close()

        try:
            await self.send_auth()
        except websockets.exceptions.ConnectionClosed as e:
            self.print_local_message("Server unexpectedly closed", error=True)
            await self.close()

        self.print_local_message(f"Successfully connected to RWCI server", plain=True, success=True)

        while self.ws.open:
            try:
                await self.poll()
            except websockets.exceptions.ConnectionClosed as e:
                self.print_local_message("Server unexpectedly closed", error=True)
                await self.close()

    # Dispatcher Events
    async def on_message(self, data):
        self.print_player_message(data["message"], data["author"])

    async def on_broadcast(self, data):
        self.print_server_broadcast(data["message"])

    async def on_auth_response(self, data):
        status = data["success"]
        registered = data["new_account"]

        if status is True:
            if registered is True:
                self.print_local_message("Registered and logged in ok", warning=True)
            else:
                self.print_local_message("Logged in ok", success=True)
        else:
            self.print_local_message("Login failed", error=True)
            self.mute = True

    async def on_join(self, data):
        username = data["username"]
        self.print_user_join(username)
        if username not in self.user_list:
            self.user_list.append(username)

    async def on_quit(self, data):
        username = data["username"]
        self.print_user_quit(username)
        if username in self.user_list:
            self.user_list.remove(username)

    async def on_direct_message(self, data):
        self.print_direct_message(data["author"], "Me", data["message"])

    async def on_user_list(self, data):
        self.user_list = data["users"]

    # Commands
    async def command_color(self, msg, color_name, *user_name):
        username = self.find_user(" ".join(user_name))

        if username is None:
            self.print_local_message(f"'{user_name} isn't online", error=True)
            return

        user = username.lower()

        await self.user_colors.put(user, color_name)

        self.print_local_message(f"Set color for {username} to {color_name}", success=True)

    async def command_clear_color(self, user_name, *args):
        username = self.find_user(user_name)

        if username is None:
            self.print_local_message(f"'{user_name}' isn't online", error=True)
            return

        user = username.lower()

        if user in self.user_colors:
            await self.user_colors.remove(user)
            self.print_local_message(f"Removed color for {username}", success=True)
        else:
            self.print_local_message(f"No color set for {username}", warning=True)

    async def command_me(self, msg, *args):
        await self.send_message(f"*{msg}*")

    async def command_quit(self, quit_message="", *args):
        if quit_message != "":
            await self.send_message(quit_message)
        self.print_local_message("Exited", plain=True)
        await self.close(complete=True)

    async def command_block(self, username, *args):
        username = self.find_user(" ".join(username))

        if username is None:
            self.print_local_message("That user isn't online", error=True)
            return

        user = username.lower()

        if user in self.settings.get("blocked_users", []):
            self.settings.get("blocked_users").remove(user)
            self.print_local_message(f"Unblocked {username}")
        else:
            self.settings.get("blocked_users").append(user)
            self.print_local_message(f"Blocked {username}")

        await self.settings.save()

    async def command_blocked(self, msg, *args):
        blocked_users = self.settings.get("blocked_users")
        self.print_local_message(f"{len(blocked_users)} users blocked")
        for user in blocked_users:
            self.print_local_message(user, plain=True)

    async def command_who(self, msg, *args):
        self.print_local_message(f"{len(self.user_list)} users online")
        for user in self.user_list:
            self.print_local_message(user, plain=True)

    async def command_w(self, msg, recipient, *message):
        username = self.find_user(recipient)

        if username.lower() == self.username.lower() and self._debug is False:
            self.print_local_message("You can't DM yourself!", error=True)
            return

        if username is None:
            self.print_local_message("That user isn't online", error=True)
            return

        message = " ".join(message)
        await self.send_direct_message(username, message)
        self.print_direct_message("Me", username, message)

    async def command_clean(self, msg):
        self.clean()
        self.print_local_message("Cleaned!", success=True)

    async def command_eval(self, msg, *args):
        code = msg
        try:
            precompiled = compile(code, "<eval>", "eval")
            result = eval(precompiled)

        except SyntaxError as e:
            self.print_local_message(f"{e.text}")
            self.print_local_message(f"{'^':>{e.offset}}", plain=True)
            self.print_local_message(f"{type(e).__name__}: {e}", plain=True, error=True)
            return

        except Exception as e:
            self.print_local_message(f"{type(e).__name__}: {e}", plain=True, warning=True)
            return

        if isawaitable(result):
            result = await result

        result = str(result)

        self.print_local_message(result, plain=True, success=True)

    async def command_markdown(self, msg, *args):
        if self.settings.get("should_render_markdown") is True:
            await self.settings.put("should_render_markdown", False)
            self.print_local_message("Disabled markdown rendering!")
        else:
            await self.settings.put("should_render_markdown", True)
            self.print_local_message("Enabled markdown rendering!")

    async def command_json(self, json_data, *args):
        await self._raw_send(json_data)
        self.print_local_message("Sent!")

    async def command_debug(self, msg, *args):
        self._debug = not self._debug
        if self._debug:
            self.print_local_message("Debug mode enabled")
        else:
            self.print_local_message("Debug mode disabled")

class LoginHandler(Ui_LoginWindow):
    def __init__(self, dialog):
        self.settings = config.Config("settings.json", default={"blocked_users": [], "server_ip": "", "server_port": "", "should_render_markdown": True})
        self.window = dialog

        Ui_LoginWindow.__init__(self)
        self.setupUi(dialog)
        dialog.setWindowIcon(QtGui.QIcon("./utils/ui/files/icon.png"))

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

        try:
            socket.getaddrinfo(self.AddressField.text(), self.PortField.text())
        except socket.gaierror:
            self.ErrorText.setText("IP address could not be resolved")
            return

        try:
            port = int(self.PortField.text())
            assert(port <= 65535 and port >= 1)
        except ValueError:
            self.ErrorText.setText("Port is not an integer")
            return

        except AssertionError:
            self.ErrorText.setText("Port is not a valid port number")




app = QtWidgets.QApplication(sys.argv)
loop = QEventLoop(app)
asyncio.set_event_loop(loop)
window = QtWidgets.QMainWindow()

login_handler = LoginHandler(window)
window.setWindowTitle("RWCI Login")

#handler = Client(window, username, password, settings)
#window.setWindowTitle(f"RWCI Client - {username}")

window.show()
with loop:
    loop.run_forever()

sys.exit()