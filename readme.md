# FastAPI Crypto Tracker

A simple FastAPI application for tracking cryptocurrency holdings and monitoring portfolio performance using live Binance price data.

## Features

- Add cryptocurrency holdings with:
  - coin symbol
  - amount
  - buy price
- Fetch live prices from the Binance API
- View current value and profit/loss for each holding
- View total portfolio value and overall returns
- Store holdings in PostgreSQL
- Built with FastAPI and async Python

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- asyncpg
- httpx
- Pydantic

## Project Structure

- `main.py` — API routes and portfolio logic
- `database.py` — PostgreSQL database setup and queries
- `models.py` — request/response models
- `services.py` — Binance API integration

## Installation

1. Clone the repository
2. Create a virtual environment
3. Install dependencies

```bash
pip install fastapi uvicorn httpx asyncpg python-dotenv

## ⚙️ Installation & Running

### 1. Clone the repository
```bash
git clone https://github.com/your-username/fastapi-crypto-tracker.git
cd fastapi-crypto-tracker
```

### 2. Create and activate a virtual environment
```bash
# For Linux/macOS
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install fastapi uvicorn httpx asyncpg python-dotenv pydantic
```

### 4. Configure environment variables
Create a `.env` file in the project root directory and add your PostgreSQL connection string:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/crypto_tracker
```
> **Note:** Ensure that the `crypto_tracker` database is created in PostgreSQL beforehand. The `holdings` table will be created automatically upon the first application startup.

### 5. Run the application
```bash
uvicorn main:app --reload
```
Once running, the application will be available at:
- **Base URL:** http://127.0.0.1:8000
- **Interactive API Docs (Swagger UI):** http://127.0.0.1:8000/docs
- **Alternative Docs (ReDoc):** http://127.0.0.1:8000/redoc

## API Endpoints

### 1. Create a holding
- **Method:** `POST /holdings`
- **Description:** Adds a new cryptocurrency purchase record.
- **Request Body:**
  ```json
  {
    "coin": "BTC",
    "amount": 1.5,
    "buy_price": 62000.0
  }
  ```
- **Response (201 Created):**
  ```json
  {
    "id": 1,
    "coin": "BTC",
    "amount": 1.5,
    "buy_price": 62000.0,
    "current_price": 63450.25,
    "profit_loss": 2175.375,
    "created_at": "2023-10-25T12:00:00Z"
  }
  ```

### 2. Get all holdings
- **Method:** `GET /holdings`
- **Description:** Returns a list of all saved holdings with current pricing data and individual PnL calculations.

### 3. Get a single holding
- **Method:** `GET /holdings/{holding_id}`
- **Description:** Returns detailed information about a specific holding by its ID. Returns `404 Not Found` if the holding does not exist.

### 4. Delete a holding
- **Method:** `DELETE /holdings/{holding_id}`
- **Description:** Removes the holding record from the database. Returns `204 No Content` on successful deletion.

### 5. Get portfolio summary
- **Method:** `GET /portfolio`
- **Description:** Aggregates data across all assets to display overall portfolio statistics.
- **Response Example:**
  ```json
  {
    "total_value": 95000.0,
    "total_invested": 90000.0,
    "profit_loss": 5000.0,
    "profit_percentage": 5.56,
    "holdings_count": 2,
    "holdings": []
  }
  ```

---

## Database Schema

The application automatically creates the `holdings` table on startup if it does not already exist.

```sql
CREATE TABLE IF NOT EXISTS holdings (
    id SERIAL PRIMARY KEY,
    coin VARCHAR(10) NOT NULL,
    amount DECIMAL(20, 8) NOT NULL,
    buy_price DECIMAL(20, 8) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Field Descriptions:**
- `id`: Unique record identifier (auto-generated).
- `coin`: Cryptocurrency symbol (e.g., `BTC`, `ETH`, `SOL`).
- `amount`: Number of coins held (precision up to 8 decimal places for crypto compatibility).
- `buy_price`: Purchase price per coin in USDT.
- `created_at`: Timestamp of record creation.

---

## Implementation Notes

1. **Ticker Adaptation:** Coin symbols are automatically converted to the format required by the Binance API internally (e.g., `BTC` becomes `BTCUSDT`), ensuring seamless price fetching.
2. **No API Keys Required:** The app uses Binance's public market endpoint (`/api/v3/ticker/price`), which does not require authentication, simplifying deployment and testing.
3. **Type Safety:** Extensive use of type hints and Pydantic models guarantees data integrity at the application boundaries.

---
