import asyncio
import websockets
import json
import random
import os
import time

with open("stocks.json", "r") as f:
    stock_data = json.load(f)

clients = set()

# Environment variables
WS_HOST = os.environ.get("SM_HOST", "localhost")
WS_PORT = os.environ.get("SM_PORT", "8765")
SEED = os.environ.get("SM_SEED", 42)

random.seed(SEED)

epoch_time = lambda: int(time.time() * 1000)

# Epoch timestamp in millis
T = epoch_time()


async def simulate_prices():
    while True:
        await asyncio.sleep(0.5)
        t = epoch_time()
        for symbol, data in stock_data.items():
            delta = random.gauss(0, data["volatility"])
            data["price"] *= 1 + delta
            data["price"] = round(data["price"], 2)

        # Broadcast update
        message = json.dumps(
            {s: {"price": d["price"], "time": t} for s, d in stock_data.items()}
        )
        for ws in clients.copy():
            try:
                await ws.send(message)
            except:
                clients.remove(ws)


async def handler(ws):
    clients.add(ws)
    try:
        # Send initial snapshot
        t = epoch_time()
        await ws.send(
            json.dumps(
                {s: {"price": d["price"], "time": t} for s, d in stock_data.items()}
            )
        )
        async for _ in ws:  # keep connection open
            pass
    finally:
        clients.remove(ws)


async def main():
    async with websockets.serve(handler, WS_HOST, WS_PORT):
        await simulate_prices()


if __name__ == "__main__":
    print("INFO: Stock market started at {T} ms from EPOCH.")
    asyncio.run(main())
