# Official Weebsockets RFC #001

This RFC details the proposed communication format and server-client expectations.

The protocol (Raspberry Pi Electronic Nested Internet Server Netscape Chat Communication Internet Relay Chat Weebsocket Chat Isn't Internet Relay Chat) shall be referred to as RWCI and the server (Pi Electronic Nested Internet Server) shall be referred as server.

This RFC includes the server and any clients that wish to be compliant.


## Authentication

To login and start communicating, the client must first authorize itself with an `auth` type packet.

```json
{
  "type": "auth",
  "username": "your_username_here",
  "password": "your_password_here"
}
```

The server will then respond with first an `auth` message stating the success (or failure) of the login attempt. If login fails, the server will close the websocket connection.
If the login attempt is successful (the username is not already connected, and the password/username combo is present in the database), the server will respond with a list of online users and then broadcast a `join` packet.

### Server Responses

Login Success (Pre-existing Account):

```json
{
  "type": "auth",
  "status": "Logged in ok",
  "success": true
}
```

Login Success (New Account):

```json
{
  "type": "auth",
  "status": "Registered and logged in ok",
  "success": true
}
```

Login Failure:

```json
{
  "type": "auth",
  "status": "Login failed",
  "success": false
}
```

## Online User List

The server sends a list of online users once a client has successfully logged in.

```json
{
  "type": "user_list",
  "users": [
    "User_1",
    "User_2",
    "User_...",
    "User_x"
  ]
}
```

This packet is only sent once, so clients must handle joins and disconnects themselves.

## Server Broadcasts

The server may send broadcast packets, which are effectively public messages from the server. The server will not send join or disconnect messages via broadcast, these are sent via `join` and `quit` packets.

```json
{
  "type": "broadcast",
  "message": "Server broadcast message"
}
```

## Public User Message

Each client has the capability to send public and direct messages. Public messages are replicated to every client.

```json
{
  "type": "message",
  "message": "authors_message"
}
```

Packets of `message` type with empty content will not be replicated, and message packets with a non-authorized usernames will have their connections closed.
The server will use the username the connection logged in with for the message author.

The server will send a packet to every client:

```json
{
  "type": "message",
  "author": "authors_name",
  "message": "authors_message"
}
```

## Direct User Message

The server and clients also have the capability to send direct messages to individual clients. The server can send DMs to clients, although the reverse is not true.

```json
{
  "type": "direct_message",
  "recipient": "recipients_username",
  "message": "authors_message"
}
```

The server will use the username the connection logged in with for the message author.

The server will send a packet to the recipient consisting of:

```json
{
  "type": "direct_message",
  "author": "authors_name",
  "message": "authors_message"
}
```

## User Join

When a client successfully connects, the server will send a `join` packet to each client, including the one that connected.

```json
{
  "type": "join",
  "username": "user_who_joined"
}
```

## User Quit

When a connected client disconnects (this does not include failed connections), the server will send a `quit` packet to each client.

```json
{
  "type": "quit",
  "username": "user_who_left"
}
```

## User Typing

Clients may choose to send typing packets, which indicated that the user is typing a message to be sent soon.

```json
{
  "type": "typing",
  "username": "user_who_is_typing"
}
```

## Old Format Packets

The server will drop any packets that do not include a `type` field, as well as any packets with a `type` field of an unknown type.