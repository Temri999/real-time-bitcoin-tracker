import requests
import time

# Function to get current Bitcoin price from CoinGecko API
def get_btc_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    try:
        response = requests.get(url)
        if response.status_code == 429:
            wait_time = int(response.headers.get('Retry-After', 60))  # Default to 1 minute
            print(f"Rate limit hit. Retrying in {wait_time} seconds.")
            time.sleep(wait_time)
            return get_btc_price()
        response.raise_for_status()
        data = response.json()
        return data.get('bitcoin', {}).get('usd', None)
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

# Main loop to fetch and display the Bitcoin price every minute
def main():
    print("Starting real-time Bitcoin price fetcher. Press Ctrl+C to stop.")
    try:
        while True:
            btc_price = get_btc_price()
            if btc_price is not None:
                print(f"Bitcoin Price: ${btc_price}")
            else:
                print("Failed to fetch Bitcoin price. Retrying in 1 minute.")
            time.sleep(60)  # Wait for 1 minute before fetching again
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")

if __name__ == "__main__":
    main()
