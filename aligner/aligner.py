import aioredis
import asyncio
import json

async def align_lyrics(data):
    # Implement your alignment logic here
    print(f"Aligning lyrics for: {data['song_name']}")

async def aligner_consumer(redis):
    while True:
        _, message = await redis.blpop("align_queue")
        data = json.loads(message.decode("utf-8"))
        await align_lyrics(data)
        # Optionally, produce a message for another service or update the database

async def main():
    redis = await aioredis.create_redis_pool("redis://localhost")
    await aligner_consumer(redis)

if __name__ == "__main__":
    asyncio.run(main())
