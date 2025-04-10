import asyncio
import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import matplotlib
import websockets
import threading
import os

matplotlib.use("TkAgg")

# Setup
symbols = ["ACME", "GLOBEX", "INITECH", "Hooli"]
HISTORY_LENGTH = 100
price_history = {symbol: deque([100.0], maxlen=HISTORY_LENGTH) for symbol in symbols}

# Plot setup
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
axes = axes.flatten()
lines = {}

# Environment variables
WS_HOST = os.environ.get("SM_HOST", "localhost")
WS_PORT = os.environ.get("SM_PORT", "8765")

for i, symbol in enumerate(symbols):
    ax = axes[i]
    ax.set_title(symbol)
    ax.set_xticks([])
    ax.set_yticks([])
    (line,) = ax.plot([], [], lw=2)
    lines[symbol] = line


def update(_):
    for symbol, line in lines.items():
        y = list(price_history[symbol])
        x = list(range(len(y)))
        line.set_data(x, y)
        ax = axes[symbols.index(symbol)]
        ax.set_xlim(0, HISTORY_LENGTH)
        ax.set_ylim(min(y), max(y) if max(y) != min(y) else min(y) + 1)


async def listen():
    uri = f"ws://{WS_HOST}:{WS_PORT}"
    try:
        async with websockets.connect(uri) as websocket:
            async for message in websocket:
                data = json.loads(message)
                for symbol in symbols:
                    price = data.get(symbol)["price"]
                    if price is not None:
                        price_history[symbol].append(price)
    except Exception as e:
        print(f"WebSocket error: {e}")


def start_async_loop():
    asyncio.run(listen())


# Start the asyncio event loop in a separate thread
threading.Thread(target=start_async_loop, daemon=True).start()

# Start the plot animation
ani = animation.FuncAnimation(fig, update, interval=500, blit=False)

plt.tight_layout()
plt.show()
