# Binance Futures Testnet Trading Bot

![](asset/gif.gif)

![Web UI](asset/UI%20.png)
![Sell UI](asset/sell%20ui.png)
![Testnet](asset/testnet%20image.png)

A simple Python CLI application to place Market and Limit orders on the Binance Futures Testnet (USDT-M).

## Features

- **Modern Web Interface (New!)**: A beautiful, glassmorphism UI served via a local Flask backend (`app.py`).
- **CLI Support**: Fully functional command-line interface for terminal users (`cli.py`).
- Place **MARKET** and **LIMIT** orders on the Binance Futures Testnet (USDT-M).
- Supports **BUY** and **SELL** sides.
- Validates user input both in the frontend UI and via CLI parameters.
- Structured code organization (`bot/`, `app.py`, `cli.py`).
- Logs API requests, responses, and errors to `trading_bot.log`.
- Designed specifically for the Binance Futures Testnet, using `requests` and custom HMAC-SHA256 signing for maximum control.

## Prerequisites

- Python 3.x
- A Binance Futures Testnet Account (Get API keys from [testnet.binancefuture.com](https://testnet.binancefuture.com/))

## Setup Steps

1. **Clone or navigate to the project directory:**
   ```bash
   cd new2
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables:**
   Create a `.env` file in the root directory and add your Testnet API keys:
   ```env
   BINANCE_API_KEY=your_testnet_api_key_here
   BINANCE_API_SECRET=your_testnet_api_secret_here
   ```
   *Alternatively, you can export these directly in your terminal bash session.*

## How to Run Examples

You communicate with the bot using the `cli.py` script.

### 1. Place a MARKET Order
Places an order to buy 0.01 BTC at the current market price.
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

### 2. Place a LIMIT Order
Places an order to sell 0.01 BTC at a specific limit price (e.g., 60000.00).
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 60000.00
```

## Running the Web UI

To launch the beautiful graphical interface instead of using the terminal, simply run the Flask application:

```bash
python app.py
```

Then, open your web browser and navigate to:
**[http://127.0.0.1:5001](http://127.0.0.1:5001)**

*(Note: The server runs on port 5001 to avoid a known conflict with Apple's AirPlay Receiver on macOS).*

The UI allows you to visually toggle between Market/Limit orders, input specific quantities, and seamlessly tracks execution results. All logic directly utilizes the core `bot` package.

## Logs

Detailed logs of all API interactions, including request parameters, URLs, and server responses, are written to `trading_bot.log`. Check this file if an order fails or to see the exact payload sent to Binance.

## Assumptions

- **Tick Size & Step Size:** The app assumes the user inputs matching tick size and step size rules for the queried asset (e.g., BTCUSDT quantity minimums and decimal places). It performs basic type/value validation but doesn't hardcode exchange information logic (like fetching bounds from `/fapi/v1/exchangeInfo`).
- **GTC Time-In-Force:** All LIMIT orders currently default to `GTC` (Good Till Canceled), standard for standard LIMIT placements.
