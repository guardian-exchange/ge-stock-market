import asyncio
import websockets
import json
import random
import os

# Seed for testing (you can make it random in prod)
random.seed(42)

with open("stocks.json", "r") as f:
    stock_data = json.load(f)

clients = set()

# Environment variables
WS_HOST = os.environ.get("SM_HOST", "localhost")
WS_PORT = os.environ.get("SM_PORT", "8765")


async def simulate_prices():
    while True:
        await asyncio.sleep(0.5)
        for symbol, data in stock_data.items():
            delta = random.gauss(0, data["volatility"])
            data["price"] *= (1 + delta)
            data["price"] = round(data["price"], 2)

        # Broadcast update
        message = json.dumps({s: d["price"] for s, d in stock_data.items()})
        for ws in clients.copy():
            try:
                await ws.send(message)
            except:
                clients.remove(ws)


async def handler(ws):
    clients.add(ws)
    try:
        # Send initial snapshot
        await ws.send(json.dumps({s: d["price"] for s, d in stock_data.items()}))
        async for _ in ws:  # keep connection open
            pass
    finally:
        clients.remove(ws)


async def main():
    async with websockets.serve(handler, WS_HOST, WS_PORT):
        await simulate_prices()

if __name__ == "__main__":
    asyncio.run(main())
