
# directdb

A simple library that makes handling SQL databases in python easy without the need to understand the syntax. The library would act like an interface between your code and the database server parsing the data to SQL format.

If you enjoy using this project, consider giving it a star as it helps out a ton <3

Currently Supported Databases:
- PostgreSQL
- SQLite

## Github Repository

https://github.com/cannonballchris/directdb

## Installation

To install the library, use `pip install directdb`

    
## License

[GPL-3.0](https://choosealicense.com/licenses/gpl-3.0/)


## Documentation

[Documentation](https://indigodev.gitbook.io/directdb)


## Usage/Examples

Using the library with a discord bot

```py
import asyncio

import discord
from discord.ext import commands
from directdb import Postgresql

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix = "!", intents = discord.Intents.all())
    
    async def setup_hook(self):
        setattr(self, "db", Postgresql(
            host = "localhost",
            user = "username",
            password = "password",
            database = "Database name here",
            port = 5000 #Your db port address here
        ))
        await self.db.connect()
        print("DB Ready")

if __name__ == "__main__":
    asyncio.run(MyBot().run("TOKEN"))
```

Using the library normally without a discord bot context.

```py
import asyncio

from directdb import Postgresql

async def database(host, user, password, database, port):
    db = Postgresql(host = host, user= user, password = password, database = database, port = port)
    await db.connect()

asyncio.run(database(...))
```





## Contributing

You can contribute to this project by providing valueable suggestions and reporting issues in our [Discord Server](https://discord.gg/sj2c7gzPzE)

