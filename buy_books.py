import asyncio
from config import bot, dp
from handlers import clients, admin


async def main():
    dp.include_router(admin.router)
    dp.include_router(clients.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    print('work')
    asyncio.run(main())
