import datetime
import sys

class Logger:
  def __init__(self, date_format='%Y-%m-%d %H:%M:%S', debug_color='grey', log_color='white'):
    self.date_format = date_format
    self.debug_color = debug_color
    self.log_color = log_color

  def log(self, text):
    timestamp = datetime.datetime.now().strftime(self.date_format)
    self.print_color(f'[{timestamp}] {text}', self.log_color)

  def debug(self, text):
    timestamp = datetime.datetime.now().strftime(self.date_format)
    self.print_color(f'[{timestamp}] {text}', self.debug_color, sys.stderr)

  def print_color(self, text, color, output=sys.stdout):
    colors = {
      'default': '\033[0m',
      'red': '\033[31m',
      'green': '\033[32m',
      'yellow': '\033[33m',
      'cyan': '\033[36m',
      'blue': '\033[34m',
      'magenta': '\033[35m',
      'white': '\033[37m',
      'grey': '\033[90m',
      'dark_grey': '\033[30m'
    }
    if color not in colors:
      raise ValueError(f"Invalid color. Expected one of: {', '.join(colors.keys())}")
    print(colors[color] + text + colors['default'], file=output)
