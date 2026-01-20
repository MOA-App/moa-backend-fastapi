import asyncio
from app.shared.infrastructure.database.init_db import create_tables

if __name__ == "__main__":
    asyncio.run(create_tables())
