# Real-Time Bitcoin Price Fetcher

## Description
This Python script continuously fetches the real-time price of Bitcoin (in USD) from the CoinGecko API every minute. The script is designed to run indefinitely until manually stopped and provides an easy way to monitor Bitcoin's current price in the terminal.

## Features
- Fetches the latest Bitcoin price every minute.
- Handles API rate-limiting by waiting for the retry period if the limit is exceeded.
- Gracefully handles errors and retries.
- Can be terminated manually with `Ctrl+C`.

## Requirements
- Python 3.6 or higher
- `requests` library

## Installation
1. Clone the repository or download the script.
2. Ensure Python is installed on your system.
3. Install the required library by running:
   ```bash
   pip install requests
   ```

## Usage
1. Run the script:
   ```bash
   python bitcoin_price_fetcher.py
   ```
2. The script will display the Bitcoin price in USD every minute.
3. To stop the program, press `Ctrl+C`.

## Code Explanation

### 1. **Importing Required Libraries**
The script uses:
- `requests`: For making HTTP requests to the CoinGecko API.
- `time`: For adding delays between API requests and handling rate limits.

```python
import requests
import time
```

### 2. **Fetching Bitcoin Price**
The `get_btc_price` function retrieves the current Bitcoin price in USD using the CoinGecko API:

- **API Endpoint**: The script queries the `https://api.coingecko.com/api/v3/simple/price` endpoint with parameters for Bitcoin (`ids=bitcoin`) and currency (`vs_currencies=usd`).
- **Rate Limiting**: If the API responds with a `429 Too Many Requests` status, the script reads the `Retry-After` header and waits for the specified duration before retrying.
- **Error Handling**: Handles both request errors and JSON parsing issues gracefully.

```python
def get_btc_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    try:
        response = requests.get(url)
        if response.status_code == 429:
            wait_time = int(response.headers.get('Retry-After', 60))
            print(f"Rate limit hit. Retrying in {wait_time} seconds.")
            time.sleep(wait_time)
            return get_btc_price()
        response.raise_for_status()
        data = response.json()
        return data.get('bitcoin', {}).get('usd', None)
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
```

### 3. **Main Loop**
The main function continuously fetches the Bitcoin price every minute:

- **Infinite Loop**: Uses a `while True` loop to repeatedly call the `get_btc_price` function.
- **Graceful Termination**: Captures `KeyboardInterrupt` (e.g., `Ctrl+C`) to allow a clean exit.
- **Error Messages**: Displays an error message if the price cannot be fetched.
- **Delay Between Requests**: Uses `time.sleep(60)` to wait 1 minute between successive API calls.

```python
def main():
    print("Starting real-time Bitcoin price fetcher. Press Ctrl+C to stop.")
    try:
        while True:
            btc_price = get_btc_price()
            if btc_price is not None:
                print(f"Bitcoin Price: ${btc_price}")
            else:
                print("Failed to fetch Bitcoin price. Retrying in 1 minute.")
            time.sleep(60)
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")

if __name__ == "__main__":
    main()
```

### 4. **Entry Point**
The `if __name__ == "__main__":` block ensures the `main` function runs only when the script is executed directly.

## Example Output
```plaintext
Starting real-time Bitcoin price fetcher. Press Ctrl+C to stop.
Bitcoin Price: $43120.45
Bitcoin Price: $43090.21
Bitcoin Price: $43115.78
...
Program terminated by user.
```

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributions
Contributions, issues, and feature requests are welcome. Feel free to fork the repository and submit a pull request!

