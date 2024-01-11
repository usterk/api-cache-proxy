import os
import pickle
import random
import time
import requests
import datetime
from urllib.parse import urlparse
from logger import Logger

class apiCache:
  def __init__(self, cache_prefix):
    self.cache_prefix = cache_prefix
    self.logs = Logger(debug_color='grey', log_color='white')

  def get_random_user_agent(self):
    user_agents = [
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
      'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
      'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
      'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
      'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
      'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063',
      'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0'
    ]
    return random.choice(user_agents)

  def get_cache_file_name(self, url, params, method="GET", create_directory=False):
    parsed_url = urlparse(url)
    sanitized_path = parsed_url.path.replace('/', '_')
    directory_path = f"{self.cache_prefix}/{parsed_url.netloc}{sanitized_path}/{method}".lower()
    if params:
      sorted_params = ",".join(f"{key}.{value}" for key, value in sorted(params.items()))
    else:
      sorted_params = "no_params"
    full_path = os.path.join(directory_path, sorted_params)
    if create_directory:
      os.makedirs(directory_path, exist_ok=True)
    return full_path + '.cache'

  def get_data_with_rate_limit(self, url, cache_valid_time, params={}):
    cache_file_name = self.get_cache_file_name(url, params, 'GET', False)
    cache_exists = os.path.exists(cache_file_name)
    cache_recent = False

    if cache_exists:
      cache_recent = (
          datetime.datetime.now() - datetime.datetime.fromtimestamp(os.path.getmtime(cache_file_name))).total_seconds() < cache_valid_time
    else:
      self.get_cache_file_name(url, params, 'GET', True)
    if cache_exists and cache_recent:
      self.logs.debug("Loading data from cache " + cache_file_name)
      with open(cache_file_name, "rb") as f:
        data = pickle.load(f)
    else:
      retries = 0
      while retries < 10:
        self.logs.debug(f"Fetching data from {url}")
        headers = {'User-Agent': self.get_random_user_agent()}
        response = requests.get(url, params=params, headers=headers)
        if response.ok:
          self.logs.debug("Update cache for " + cache_file_name)
          data = response.json()
          with open(cache_file_name, "wb") as f:
            pickle.dump(data, f)
          break
        elif response.status_code == 429:  # If we hit the rate limit, wait and retry without increasing the retry counter
          rand_wait = random.randint(1, 10)
          self.logs.debug(f"Rate limit exceeded. Waiting {rand_wait} seconds...")
          time.sleep(rand_wait)
        else:
          retries += 1
          time.sleep(5)  # Wait for 5 seconds before retrying
      else:  # If after X attempts the request still fails, load the data from the cache
        if os.path.exists(cache_file_name):
          self.logs.debug("Failed fetching from api: Loading data from cache " + cache_file_name)
          with open(cache_file_name, "rb") as f:
            data = pickle.load(f)
        else:
          data = None
    return data
