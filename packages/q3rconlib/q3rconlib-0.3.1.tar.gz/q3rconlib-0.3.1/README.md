# A Quake3 RCON interface in Python

Send rcon commands to Q3 compatible servers.

For an outline of past/future changes refer to: [CHANGELOG](CHANGELOG.md)

## Requirements

-   Python 3.11 or greater
-   The game must implement RCON using the Q3 protocol.

## Installation

```bash
pip install q3rconlib
```

## Use

```python
import os

import q3rconlib


def main():
    with q3rconlib.connect(
        host=os.environ["Q3RCON_HOST"],
        port=int(os.environ["Q3RCON_PORT"]),
        password=os.environ["Q3RCON_PASSWORD"],
    ) as rcon:
        resp = rcon.send("status")
        print(resp)


if __name__ == "__main__":
    main()
```

#### `q3rconlib.connect(host: str='host', port: int=port, password: str='strongrconpassword')`

The Q3Rcon class accepts the following keyword arguments:

-   `host`: hostname the gameserver resides on
-   `port`: port the gameserver accepts rcon requests on
-   `password`: rcon password
-   `login_timeout`: max timeout for a successful login
-   `default_timeout`: default amount of time we wait for a response from the game server
-   `timeouts`: a dict containing `cmd: timeout` mappings. 
    -   Some commands take more time to return a response or the response is returned in fragments. You may pass a timeouts dict to specify how long to wait for a given command.

#### `Timeouts`

Let's say that that restarting or rotating the map takes a long time, you could pass the following timeouts dict:

```python
timeouts = {
    "map_restart": 1,
    "map_rotate": 1,
}

with q3rconlib.connect(timeouts=timeouts, **config_from_toml()) as rcon:
    """do cool stuff"""
```

This will cause the program to wait for 1 second for all response fragments to come back from the server.
