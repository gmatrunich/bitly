import requests
import os
import argparse
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("BITLY_TOKEN")
ENTRY_URL = 'https://api-ssl.bitly.com/v4/bitlinks'

def make_headers(token):
  headers = {
    "Authorization": "Bearer {}".format(token)
  }
  return headers

def make_payload(url):
  payload = {
    "long_url": url
  }
  return payload

def shorten_link(token, url):
  response = requests.post(ENTRY_URL, json=make_payload(url), headers=make_headers(token))
  response.raise_for_status()
  short_link_data = response.json()
  return short_link_data['link']

def count_clicks(token, short_link):
  response = requests.get(ENTRY_URL + '/{}/clicks/summary'.format(short_link), headers=make_headers(token))
  response.raise_for_status()
  clicks_count_data = response.json()
  return clicks_count_data['total_clicks']

def remove_http_symbols(short_link):
  return short_link[short_link.find('bit.ly'):]

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Сокращение ссылок с помощью сервиса bit.ly и вывод статистики по переходам')
  parser.add_argument('url', help='Введите ссылку для сокращения или bitly-ссылку для просмотра количества переходов.')
  args = parser.parse_args()

  try:
    url = args.url
    if url.startswith('http://bit.ly') or url.startswith('https://bit.ly'):
        print('Количество переходов:', count_clicks(TOKEN, remove_http_symbols(url)))
    else:
        print('Битлинк', shorten_link(TOKEN, url))
  except requests.exceptions.HTTPError:
    print('Ошибка: Неверная ссылка.')