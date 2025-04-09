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
Each message sent over the WebSocket connection is a JSON object with the current prices of all available stocks.

### Example Payload:
```json
{
  "ACME": 98.72,
  "GLOBEX": 102.35,
  "INITECH": 100.21,
  "Hooli": 101.12
}
```

- Clients must connect to `ws://<host>:<port>` (default: `ws://localhost:8765`) and listen for messages.
- No special events or namespaces; just raw WebSocket text messages.

## Client Visualization
The included sample client (`sample-client.py`) connects to the WebSocket server and visualizes all stocks in a **2x2 grid using `matplotlib`**.

- **X/Y axes**: Simplified for readability (ticks removed).
- **Subplots**: One per stock, with a live updating line.
- **Animation**: Driven by `matplotlib.animation.FuncAnimation`.

## TODOs
- [ ] **Restrict Access to Server Internally:** Use a firewall or reverse proxy (e.g., NGINX) to expose the WebSocket server only to internal frontend/backend services.

- [ ] **Randomize Simulation in Production:** Currently uses `random.seed(42)` for deterministic price generation. Replace this with a random or time-based seed for real deployments.
