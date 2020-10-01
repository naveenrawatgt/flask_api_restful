import requests
BASE = "http://127.0.0.1:5000/api/"
response = requests.patch(BASE+'5', {'model': 'Samsung'})

# 'type': 'Television', 'mac_address': '11.11.111.3'})
print(response)


input()

res = requests.get(BASE+'5')
print(res)
