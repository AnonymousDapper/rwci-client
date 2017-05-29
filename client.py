import json
import asyncio
import sys
import shlex
import re
import os

try:
    import mistune
    import websockets
except ModuleNotFoundError:
    print("Make sure to install the dependencies in requirements.txt before running the program!")
    sys.exit(1)

from datetime import datetime
from inspect import isawaitable
from getpass import getpass

from utils.colors import paint, back, attr
from utils import time
from utils import config

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
        return attr(text, "reverse")

    def underscore(self, text):
        return attr(text, "score")

    def paragraph(self, text):
        return text

    def codespan(self, text):
        return paint(text, "b_green")

    def autolink(self, link, is_email=False):
        return link

    def link(self, link, title, text):
        return link

    def block_quote(self, text):
        return f">{text}"

    def block_html(self, html):
        return html

    def text(self, text):
        return text

    def escape(self, text):
        return text

    def inline_html(self, html):
        return html

class Handler:
    def __init__(self, username, password):
        self._debug = False
        self.username = username
        self.password = password
        self.user_list = []
        self.loop = asyncio.get_event_loop()
        self.user_colors = config.Config("user_colors.json")
        self.settings = config.Config("settings.json")

        self.ip = self.settings.get("server_ip")
        self.port = self.settings.get("server_port")
        renderer = Renderer()
        lexer = InlineLexer(renderer)
        lexer.enable_underscore()
        self.clean = lambda: os.system("cls" if os.name == "nt" else "clear")

        self.markdown = mistune.Markdown(renderer, inline=lexer)

    def dispatch(self, event, *args, **kwargs):
        method = "on_" + event
        if hasattr(self, method):
            asyncio.ensure_future(self._run_event(method, *args, **kwargs), loop=self.loop)

    def run_command(self, command, *args, **kwargs):
        method = "command_" + command
        if hasattr(self, method):
            asyncio.ensure_future(self._run_event(method, *args, **kwargs), loop=self.loop)
        else:
            self.print_local_message(f"Command '{command}' doesn't exist!", warning=True)

    async def _run_event(self, event, *args, **kwargs):
        try:
            await getattr(self, event)(*args, **kwargs)
        except Exception as e:
            print(f"{type(e).__name__}: {e}")

    def log(self, text):
        print(text)

    def find_user(self, name):
        for user in self.user_list:
            if user[:len(name)].lower().strip() == name.lower().strip():
                return user

    def parse_formatting(self, text):
        if self.settings.get("should_render_markdown") is True:
            return self.markdown(text)
        else:
            return text

    # Print types
    def print_player_message(self, message, author):
        low_author = author.lower()
        if low_author in self.settings.get("blocked_users", []):
            return

        fg_color = self.user_colors.get(low_author, {}).get("fg", "white")
        bg_color = self.user_colors.get(low_author, {}).get("bg", "black")
        text = self.parse_formatting(message)
        timestamp = datetime.now().strftime(time.time_format)

        print(f"[{paint(timestamp, 'red')}] {paint(back(author, bg_color), fg_color)}: {text}")

    def print_server_broadcast(self, message):
        fg_color = "b_magenta"
        text = self.parse_formatting(message)
        timestamp = datetime.now().strftime(time.time_format)

        print(f"[{paint(timestamp, 'red')}] <| SERVER |> {paint(text, fg_color)}")

    def print_direct_message(self, author, recipient, message):
        author_color = "yellow"
        recipient_color = "b_red"
        message_color = "magenta" if author == "Server" else "white"
        text = self.parse_formatting(message)
        timestamp = datetime.now().strftime(time.time_format)

        print(f"[{paint(timestamp, 'red')}] [{paint(author, author_color)} -> {paint(recipient, recipient_color)}]: {paint(message, message_color)}")

    def print_user_join(self, username):
        print(paint(f"+ {username} has joined", "b_blue"))

    def print_user_quit(self, username):
        print(paint(f"- {username} has left", "b_red"))

    def print_local_message(self, message, plain=False, **kwargs):
        if kwargs.get("error"):
            fg_color = "b_red"
        elif kwargs.get("warning"):
            fg_color = "yellow"
        elif kwargs.get("info"):
            fg_color = "cyan"
        elif kwargs.get("success"):
            fg_color = "b_green"
        else:
            fg_color = "cyan"

        if plain:
            print(f"|  {paint(message, fg_color)}")
        else:
            print(f"<< {paint(message, fg_color)} >>")

    async def _raw_send(self, data):
        try:
            if isinstance(data, dict):
                data = json.dumps(data)
            if self._debug:
                print("SEND", data)

            await self.ws.send(data)
        except websockets.exceptions.ConnectionClosed as e:
            print(f"Server closed unexpectedly ({e.reason})")
            await self.close()
        except Exception as e:
            print(f"{type(e).__name__}: {e}")

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
        payload = {
            "type": "direct_message",
            "recipient": recipient,
            "message": message
        }
        await self._raw_send(payload)

    async def poll(self):
        try:
            data = await self.ws.recv()
            await self.process_data(data)
        except websockets.exceptions.ConnectionClosed as e:
            print(f"Server closed unexpectedly ({e.reason})")
            await self.close()
        except Exception as e:
            print(f"{type(e).__name__}: {e}")

    def decode_data(self, data):
        try:
            data = json.loads(data)
        except:
            pass
        return data

    async def process_data(self, data):
        message = self.decode_data(data)

        if not isinstance(message, dict):
            print(type(message), message)
            return

        packet_type = message.get("type")

        if self._debug:
            print("RECV", message)

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

        else:
            print(message)

    async def process_command(self, text):
        try:
            parts = shlex.split(text[1:])
        except:
            parts = text[1:].split()
        command_name = parts[0]
        self.run_command(command_name, text[2 + len(command_name):], *parts[1:])

    async def read_input(self):
        while True:
            message = await self.loop.run_in_executor(None, sys.stdin.readline)
            if message.startswith("/"):
                await self.process_command(message.strip())
            else:
                await self.send_message(message.strip())

    async def close(self):
        self.input_task.cancel()

        self.loop.stop()
        try:
            await self.ws.close()
        except:
            pass

        sys.exit()

    async def __call__(self):
        self.log(f"Attempting websocket connection to {paint(self.ip, 'green')}:{paint(self.port, 'yellow')}")
        self.ws = await websockets.client.connect(f"ws://{self.ip}:{self.port}")

        try:
            await self.send_auth()
            self.log("Successfully connected to websocket server")
        except websockets.exceptions.ConnectionClosed as e:
            print(f"Server closed unexpectedly ({e.reason})")
            await self.close()
        except Exception as e:
            print(f"Failed to connect [{type(e).__name__}]: {e}")
            await self.close()

        self.input_task = self.loop.create_task(self.read_input())

        while self.ws.open:
            try:
                await self.poll()
            except websockets.exceptions.ConnectionClosed as e:
                print(f"Server closed unexpectedly ({e.reason})")
                await self.close()
            except Exception as e:
                print(f"{type(e).__name__}: {e}")
                await self.close()

    # Dispatch events
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

    async def on_join(self, data):
        username = data["username"]
        self.print_user_join(username)
        if username not in self.user_list:
            self.user_list.append(username)

    async def on_quit(self, data):
        username = data["username"]
        self.print_user_quit(username)
        try:
            self.user_list.remove(username)
        except:
            pass

    async def on_direct_message(self, data):
        self.print_direct_message(data["author"], "Me", data["message"])

    async def on_user_list(self, data):
        self.user_list = data["users"]

    # Commands
    async def command_fgcolor(self, msg, color_name, *username):
        username = self.find_user(" ".join(username))

        if username is None:
            self.print_local_message("That user isn't online", error=True)
            return

        user = username.lower()

        if user in self.user_colors:
            user_data = self.user_colors.get(user)
            user_data["fg"] = color_name
            await self.user_colors.put(user, user_data)
        else:
            await self.user_colors.put(user, dict(fg=color_name))

        self.print_local_message(f"Set foreground color for {username} to {color_name}", success=True)

    async def command_bgcolor(self, msg, color_name, *username):
        username = self.find_user(" ".join(username))

        if username is None:
            self.print_local_message("That user isn't online", error=True)
            return

        user = username.lower()

        if user in self.user_colors:
            user_data = self.user_colors.get(user)
            user_data["bg"] = color_name
            await self.user_colors.put(user, user_data)
        else:
            await self.user_colors.put(user, dict(bg=color_name))

        self.print_local_message(f"Set background color for {username} to {color_name}", success=True)

    async def command_clear_color(self, username, *args):
        username = self.find_user(username)

        if username is None:
            self.print_local_message("That user isn't online", error=True)
            return

        user = username.lower()

        if user in self.user_colors:
            await self.user_colors.remove(user)
            self.print_local_message(f"Removed colors for {username}", success=True)
        else:
            self.print_local_message(f"No colors set for {username}", warning=True)

    async def command_me(self, msg, *args):
        await self.send_message(f"*{msg}*")

    async def command_quit(self, quit_message="", *args):
        if quit_message != "":
            await self.send_message(quit_message)
        self.print_local_message("Exited", plain=True)
        await self.close()

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
        if recipient.lower() == self.username.lower() and self._debug is False:
            self.print_local_message("You can't DM yourself!", error=True)
            return

        username = self.find_user(recipient)
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
            #return f"{e.text}\n{'^':>{e.offset}}\n{type(e).__name__}: {e}"
            self.print_local_message(f"{e.text}")
            self.print_local_message(f"{'^':>{e.offset}}", plain=True)
            self.print_local_message(f"{type(e).__name__}: {e}", plain=True, error=True)
            return

        except Exception as e:
            #return f"{type(e).__name__}: {e}"
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
        if self._debug:
            self._debug = False
            self.print_local_message("Debug mode disabled")
        else:
            self._debug = True
            self.print_local_message("Debug mode enabled")


username = input(paint("Username: ", "b_green"))
password = getpass(paint("Password: ", "b_blue"))

websocket_handler = Handler(username, password)
loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(websocket_handler())

except KeyboardInterrupt:
    asyncio.ensure_future(websocket_handler.ws.close())

finally:
    sys.exit()