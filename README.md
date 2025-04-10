> Simulates multiple stock prices in real time and streams them via **WebSocket** to connected clients.

---

## Getting Started

```bash
# Install required dependencies
pip install -r requirements.txt

# Run the stock market server (runs on ws://localhost:8765 by default)
python stock-market.py &

# Run the sample client to view the live plot (2x2 grid for all stocks)
python sample-client.py
```

## WebSocket API

The server streams stock price updates to all connected WebSocket clients in real time (roughly every 0.5 seconds).

### Message Format

Each message sent over the WebSocket connection is a JSON object with the current prices of all available stocks and timestamps (from EPOCH) at the time of sensing the stock values.

### Example Payload:

```json
{
  "ACME": { "price": 98.72, "time": 1744276931469 },
  "GLOBEX": { "price": 102.35, "time": 1744276931469 },
  "INITECH": { "price": 100.21, "time": 1744276931469 },
  "Hooli": { "price": 101.12, "time": 1744276931469 }
}
```

- Clients must connect to `ws://<host>:<port>` (default: `ws://localhost:8765`) and listen for messages.
- No special events or namespaces; just raw WebSocket text messages.

## Client Visualization

The included sample client (`sample-client.py`) connects to the WebSocket server and visualizes all stocks in a **2x2 grid using `matplotlib`**.

- **X/Y axes**: Simplified for readability (ticks removed).
- **Subplots**: One per stock, with a live updating line.
- **Animation**: Driven by `matplotlib.animation.FuncAnimation`.
