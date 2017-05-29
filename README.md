# rwci-client
Python 3.6 client for the RWCI server

This is a custom IRC-style client for the RWCI communication protocol (detailed [here](https://gist.github.com/SpoopySaitama/33f45f7bf27151542330ce3a67658ba0) and [here](https://drzach-demo.readthedocs.io/en/latest/netscape-chat/information/)).

# Setup And First Run

Remove the `demo` extension from the json files. (Or create new files with the same structure)

In `settings.json`, change the `"server_ip": "",` line to include the server's IP address in quotes.

Once that's done, you can start the client and login!

`qt_client.py` runs in a GUI, is basically a cleaner version of the console client.
`client.py` runs in the console and can run on termux on Android devices.

# Commands

## Foreground Color

Changes the foreground color for a given user.
`/fgcolor <color> <user>`

Examples:
`/fgcolor green chaten`

`/fgcolor a_deep_orange cyber`

## Background Color

Changes the background color for a given user.
`/bgcolor <color> <user>`

Examples:
`/bgcolor white Nick`

`/bgcolor black zachary`

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