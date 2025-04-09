> Simulates multiple stock prices in real time and serves them over a simple Flask API.
---

## Getting Started
```bash
# Install required dependencies
pip install -r requirements.txt

# Run the stock market server on port :5000
python stock-market.py &

# Run the sample client to view the live plot (2x2 grid for all stocks)
python sample-client.py
```

## API Reference
### `GET /price`
Returns the current stock prices for all available stocks.

#### Optional Query Parameter:
- `symbol` (string): If provided, returns data for the specified stock only.

#### Example: Get all stocks:
```bash
curl http://localhost:5000/price
```

**Response:**
```json
{
  "ACME": 98.72,
  "GLOBEX": 102.35,
  "INITECH": 100.21,
  "Hooli": 101.12
}
```

#### Example: Get single stock
```bash
curl http://localhost:5000/price?symbol=ACME
```

**Response:**
```json
{
  "ACME": 98.72
}
```

## TODOs

- [ ] **Add a firewall**
  Restrict access to the `/price` endpoint such that only internal services (like the django-backend or sample-client) can query the server.

- [ ] **Randomize the initialization seed in production**
  Currently, a fixed seed (`random.seed(42)`) is used to ensure reproducibility. Replace it with a random seed (or time-based one) in production to make price simulation unpredictable.
