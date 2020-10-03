import requests
import random

models = ["SAMSUNG", "LG", "MI", "SONY", "MOTOROLA", "XIOMI", "APPLE", "SONATA", "LENOVO", "DELL", "HP", "IFB"]

types = ["Television", "MOBILE", "WASHING MACHINE", "SMART TV", "WATCH", "HEAD SET", "POD", "SMART BULB", "DRONE", "CAMERA"]

BASE = "http://127.0.0.1:5000/api/"

def create_data():
    for i in range(1000):
        res = requests.put(BASE+str(i), {'model': random.choice(models), "mac_address": "0000A"+str(i), "type":random.choices(types)})
        print(res)
    print("Successfully create Database entries...")

# create_data()

# response = requests.put(BASE+'5', {'model': 'Samsung', "mac_address":"100.11.22.33", "type":"TV"})

# # 'type': 'Television', 'mac_address': '11.11.111.3'})
# print(response.text)

# input()
x = input("Enter the product id you wanna search??")
res = requests.get(BASE+x)
print(res.text)

# print("To delete this item id:{5}, press enter...")
# input()

# res = requests.delete(BASE + '5')

# print(res.text)