from sanic import Sanic, response
import aioredis
import asyncio
import os

app = Sanic("comm")

@app.route("/produce", methods=["POST"])
async def produce(request):
    data = request.json
    await app.redis.rpush("queue", data)
    return response.json({"message": "Data added to queue"})

async def consumer():
    while True:
        _, data = await app.redis.blpop("queue")
        # Process the data
        print(f"Consumed: {data}")

async def main():
    server = app.create_server(return_asyncio_server=True)
    asyncio.create_task(consumer())
    await server.serve_forever()

async def setup_redis(app):
    redis_host = os.getenv("REDIS_HOST", "localhost")
    redis_port = os.getenv("REDIS_PORT", 6379)
    app.redis = await aioredis.create_redis_pool(f"redis://{redis_host}:{redis_port}")

async def close_redis(app):
    app.redis.close()
    await app.redis.wait_closed()

app.register_listener(setup_redis, "before_server_start")
app.register_listener(close_redis, "after_server_stop")

if __name__ == "__main__":
    asyncio.run(main())