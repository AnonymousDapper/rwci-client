# rwci-client
Python 3.6 client for the RWCI server

This is a custom IRC-style client for the RWCI communication protocol (detailed [here](https://gist.github.com/SpoopySaitama/33f45f7bf27151542330ce3a67658ba0) and [here](https://drzach-demo.readthedocs.io/en/latest/netscape-chat/information/)).

# Setup And First Run

Remove the `demo` extension from the json files. (Or create new files with the same structure)

In `settings.json`, change the `"server_ip": "",` line to include the server's IP address in quotes.

Once that's done, you can start the client and login!

`qt_client.py` runs in a GUI, is basically a cleaner version of the console client.
`client.py` runs in the console and can run on termux on Android devices.