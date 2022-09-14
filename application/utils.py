import requests


def getdata():
    response = requests.get('https://bitpay.com/api/rates')
    data = response.json()
    return data
