# README.md
## About the Program
This program is a proxy designed to fetch data from CoinGecko and cache requests to avoid hitting the rate limiter. It's built with Python and uses Flask for the web server and os for environment variable management.

## Installation
To install and run this program, you will need Python 3 and the Flask library. You can install Flask with pip:
```
git clone https://github.com/usterk/api-cache-proxy.git
cd api-cache-proxy
pip3 install flask flask_cors requests
```
## Running the Program
To run the program, use the following command:
```
python3 main.py
```
The program uses the `HOST` and `PORT` environment variables to determine where to run the server. If these are not set, it will default to `localhost` and `8081` respectively. You can set these variables in your shell before running the program:
```
export HOST='your_host/ip'
export PORT='your_port'
python3 main.py
```
## Running in background
To run the program in background, use the following command:
```
screen -S api-cache-proxy-session
python3 main.py | tee output.log
```
Then press `Ctrl+A`` followed by `D` to detach the session.

To reattach the session, use the following command:
```
screen -d -r api-cache-proxy-session
```

## Making Requests
You can make requests to the CoinGecko API through this proxy using curl, browser or your js app. Here's an example:
```
curl 'http://localhost:8081/coingecko/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc'
```

Replace `localhost:8081` with your host and port if you've set them to something different.

## Using the cache_valid_time Parameter
The `cache_valid_time` parameter is passed as a query parameter in the request URL. It accepts an integer value representing the maximum age of the cache file in seconds. If the cache file is older than this value, the program will fetch fresh data from CoinGecko and update the cache.

Here's an example of how to use it:
```
curl 'http://localhost:8081/coingecko/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&cache_valid_time=3600'
```

In this example, cache_valid_time is set to `3600` seconds, or one hour. This means that if the cache file is more than one hour old, the program will fetch fresh data.

## Program Output
When you start the program, you should see output similar to the following:
```
You can set HOST with environment variables :)
You can set PORT with environment variables :)
 * Serving Flask app 'main'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://localhost:8081
Press CTRL+C to quit
[2024-01-11 15:28:26] Fetching data from https://api.coingecko.com/api/v3/coins/markets
[2024-01-11 15:28:26] Update cache for cache/api.coingecko.com_api_v3_coins_markets/get/cache_valid_time.3600,order.market_cap_desc,vs_currency.usd.cache
127.0.0.1 - - [11/Jan/2024 15:28:26] "GET /coingecko/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&cache_valid_time=3600 HTTP/1.1" 200 -
```

This indicates that the server is running and ready to accept requests.
