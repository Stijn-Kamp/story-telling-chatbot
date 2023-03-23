import os
from dotenv import load_dotenv

load_dotenv()

def get_token(token_name):
  """
  Loads a token from env.
  """
  try:
    os.environ[token_name]
    token = os.environ[token_name]
  except KeyError:
    token = None
  return token