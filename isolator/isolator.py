import aioredis
import asyncio
import json

async def isolate_vocals(data):
    # Implement your isolation logic here
    print(f"Isolating vocals for: {data['song_name']}")

async def isolator_consumer(redis):
    while True:
        _, message = await redis.blpop("isolate_queue")
        data = json.loads(message.decode("utf-8"))
        await isolate_vocals(data)
        # Produce a message for the Aligner service
        await redis.rpush("align_queue", json.dumps(data))

async def main():
    redis = await aioredis.create_redis_pool("redis://localhost")
    await isolator_consumer(redis)

if __name__ == "__main__":
    asyncio.run(main())
