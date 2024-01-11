import os
from flask import Flask, request
from flask_cors import CORS
from api_cache import apiCache

app = Flask(__name__)
CORS(app)
api_cache = apiCache(cache_prefix='cache')

@app.route('/coingecko/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
  url = f'https://api.coingecko.com/{path}'
  params = request.args
  cache_valid_time = int(params.get('cache_valid_time', 0))
  data = api_cache.get_data_with_rate_limit(url, cache_valid_time, params)
  return data

if __name__ == '__main__':
  host = os.getenv('HOST', 'localhost')
  port = int(os.getenv('PORT', 8081))
  
  if host == 'localhost':
    print("You can set HOST with environment variables :)")
  if port == 8081:
    print("You can set PORT with environment variables :)")

  app.run(host=host, port=port)
