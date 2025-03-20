# WizTrader SDK

A Python SDK for connecting to the Wizzer trading platform.

## Installation

You can install the package directly from PyPI:

```bash
pip install wiz_trader
```

## Features

- Real-time market data through WebSocket connection
- REST API for accessing market data and indices
- Automatic WebSocket reconnection with exponential backoff
- Subscribe/unsubscribe to instruments
- Customizable logging levels

## Quick Start - Quotes Client

```python
import asyncio
from wiz_trader import QuotesClient

# Callback function to process market data
def process_tick(data):
  print(f"Received tick: {data}")

async def main():
  # Initialize client with direct parameters
  client = QuotesClient(
    base_url="wss://websocket-url/quotes",
    token="your-jwt-token",
    log_level="info"  # Options: "error", "info", "debug"
  )
  
  # Set callback
  client.on_tick = process_tick
  
  # Connect in the background
  connection_task = asyncio.create_task(client.connect())
  
  # Subscribe to instruments
  await client.subscribe(["NSE:SBIN:3045"])
  
  # Keep the connection running
  try:
    await asyncio.sleep(3600)  # Run for 1 hour
  except KeyboardInterrupt:
    # Unsubscribe and close
    await client.unsubscribe(["NSE:SBIN:3045"])
    await client.close()
      
  await connection_task

if __name__ == "__main__":
  asyncio.run(main())
```

## Quick Start - DataHub Client

```python
from wiz_trader import WizzerClient

# Initialize client
client = WizzerClient(
  base_url="https://api-url.in",
  token="your-jwt-token",
  log_level="info"  # Options: "error", "info", "debug"
)

# Get list of indices
indices = client.get_indices(exchange="NSE")
print(indices)

# Get index components
components = client.get_index_components(
  trading_symbol="NIFTY 50", 
  exchange="NSE"
)
print(components)

# Get historical OHLCV data
historical_data = client.get_historical_ohlcv(
  instruments=["NSE:SBIN:3045"],
  start_date="2024-01-01",
  end_date="2024-01-31",
  ohlcv=["open", "high", "low", "close", "volume"]
)
print(historical_data)
```

## Configuration

You can configure the clients in two ways:

1. **Direct parameter passing** (recommended):
  ```python
  quotes_client = QuotesClient(
    base_url="wss://websocket-url/quotes",
    token="your-jwt-token",
    log_level="info"
  )
   
  wizzer_client = WizzerClient(
    base_url="https://api-url.in",
    token="your-jwt-token",
    log_level="info"
  )
  ```

2. **System environment variables**:
  - `WZ__QUOTES_BASE_URL`: WebSocket URL for the quotes server
  - `WZ__API_BASE_URL`: Base URL for the Wizzer's REST API
  - `WZ__TOKEN`: JWT token for authentication

  ```python
  # The clients will automatically use the environment variables if parameters are not provided
  quotes_client = QuotesClient(log_level="info")
  wizzer_client = WizzerClient(log_level="info")
  ```

## Advanced Usage

Check the `examples/` directory for more detailed examples:

- `example_manual.py`: Demonstrates direct configuration with parameters
- `example_wizzer.py`: Demonstrates usage of the Wizzer client

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.