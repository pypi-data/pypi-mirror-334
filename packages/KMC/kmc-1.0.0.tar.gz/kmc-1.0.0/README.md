<!--
SPDX-FileCopyrightText: 2025 Anthony Zimmermann

SPDX-License-Identifier: GPL-3.0-only
-->

# KMC - Keyboard Mouse Connect

Forward keyboard and mouse input to another machine via a software communication protocol like ethernet.

## Running KMC client

With a client configuration file `client.conf`, kmc client can be executed like this:

```bash
kmc -c client.conf
```

### Example client configuration

```
# Filename: client.conf
[display.tcp.display1]
host = display1-hostname
port = 12345
keymap = <shift>+<ctrl>+<up>
```
## Running KMC server

With a server configuration file `server.conf`, kmc server can be executed like this:

```bash
kmc-server -c server.conf
```

### Example server configuration

```
# Filename: server.conf
[display.tcp.display1]
host = localhost
port = 12345
```

---

**KMC Version 1.0.0<!-- VERSION -->**

---
