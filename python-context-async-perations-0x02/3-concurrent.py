import asyncio
import aiosqlite


async def async_fetch_users():
    async with aiosqlite.connect("users.db") as db:
        cursor = await db.execute("SELECT * FROM users")
        return await cursor.fetchall()


async def async_fetch_older_users():
    async with aiosqlite.connect("users.db") as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > 40")
        return await cursor.fetchall()


async def fetch_concurrently():
    # Run both queries at the same time
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    all_users, older_users = results

    print("All Users:", all_users)
    print("Users Older Than 40:", older_users)


# Run the concurrent fetch
asyncio.run(fetch_concurrently())
