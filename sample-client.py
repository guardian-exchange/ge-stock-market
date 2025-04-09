from collections import deque
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import requests
import matplotlib
matplotlib.use("TkAgg")

# Stock symbols to monitor
symbols = ["ACME", "GLOBEX", "INITECH", "Hooli"]

# History length for each stock
HISTORY_LENGTH = 100

# Store price history for each symbol
price_history = {symbol: deque([100.0], maxlen=HISTORY_LENGTH)
                 for symbol in symbols}

# Setup 2x2 subplots
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
axes = axes.flatten()

# Lines for each subplot
lines = {}

for i, symbol in enumerate(symbols):
    ax = axes[i]
    ax.set_title(symbol)
    ax.set_xticks([])  # remove x-axis ticks
    ax.set_yticks([])  # remove y-axis ticks

    # Initialize a blank line
    line, = ax.plot([], [], lw=2)
    lines[symbol] = line


def update(frame):
    try:
        # Fetch all stock prices at once
        response = requests.get("http://localhost:5000/price")
        prices = response.json()

        for symbol in symbols:
            price = prices.get(symbol)
            if price is not None:
                price_history[symbol].append(price)
                y = list(price_history[symbol])
                x = list(range(len(y)))

                line = lines[symbol]
                line.set_data(x, y)
                axes[symbols.index(symbol)].set_xlim(0, len(y))
                axes[symbols.index(symbol)].set_ylim(min(y), max(y))

    except Exception as e:
        print("Error fetching data:", e)


ani = animation.FuncAnimation(
    fig, update, interval=500, blit=False, cache_frame_data=False
)

plt.tight_layout()
plt.show()
