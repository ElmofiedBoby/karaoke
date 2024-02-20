import aioredis
import asyncio
import json

async def download_song(data):
    # Implement your download logic here
    print(f"Downloading song: {data['song_name']}")

async def downloader_consumer(redis):
    while True:
        _, message = await redis.blpop("download_queue")
        data = json.loads(message.decode("utf-8"))
        await download_song(data)
        # Produce a message for the Isolator service
        await redis.rpush("isolate_queue", json.dumps(data))

async def main():
    redis = await aioredis.create_redis_pool("redis://localhost")
    await downloader_consumer(redis)

if __name__ == "__main__":
    asyncio.run(main())