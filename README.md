# rwci-client
Python 3.6 client for the RWCI server

This is a custom IRC-style client for the RWCI communication protocol (detailed [here](https://gist.github.com/AnonymousDapper/33f45f7bf27151542330ce3a67658ba0)).

# Setup And First Run

You don't need to do anything besides make sure the file is there and you've installed the dependencies.

To install the dependencies, run `pip install -r qt_requirements.txt`

# Commands

## Text Color

Changes the text color for a given user.
`/color <color> <user>`

Examples:
`/color green chaten`

`/color a_deep_orange cyber`

## Clear Colors

Clears a users set colors.
`/clear_color <user>`

## Me Text

Sends a message using action text.
`/me <action>`

## Logoff

Disconnects from the server, with an optional quit message.
`/quit [message]`

## Block Toggle

Toggles blocked status of a given user.
`/block <user>`

## Blocked List

Shows blocked users.
`/blocked`

## Online List

Shows who is online.
`/who`

## Direct Message (Whisper)

Sends a message directly to another user.
`/w <user> <msg>`

(You can simply type the first few letters of their name and hit enter, the command will find them anyway)

## Code Eval

Runs python code directly in the chat window.
`/eval <code>`

## Markdown Toggle

Toggles markdown renderering.
`/markdown`

## Raw JSON Sending

Sends given raw data directly to the server.
`/json <json_data>`

## Debug Toggle

Toggles debug mode. You can only send DMs to yourself with debug mode enabled.
`/debug`

## Join Channel

Join a chat channel. All messages are saved corresponding to their channels, so you can still get messages for other channels.
`/join <channel>`

(You can simply type the first few letters of the channel name and hit enter, the command will find it anyway)

## Quick Reply

Quickly reply to the last person to send you a DM.
`/r <msg>`

# Self-hosted Server

If you would like to host a server, simply clone/download this repository and grab the two files from [this gist](https://gist.github.com/AnonymousDapper/e1658328a915a2a5e2b6f5820a510222).

Run `server.py` using Python 3.6 and enjoy