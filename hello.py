print("hello")

a = 1
b = 2

print(a + b)

def say_hello(name):
    print(f"Hello, {name}!")


import greet

greet.say_hello("Alice")

import math

print(math.sqrt(16))  # หาค่ารากที่สองของ 16
print(math.pi)  # แสดงค่าพาย



import os

print(os.getcwd())  # แสดงที่อยู่ของ directory ปัจจุบัน
os.system('mkdir my_new_directory')  # สร้าง directory ใหม่ (ทำงานบนระบบ Unix/Linux)




import json

# แปลง dictionary เป็น JSON
data = {
    "name": "John",
    "age": 30,
    "city": "New York"
}
json_data = json.dumps(data)
print(json_data)

# แปลง JSON เป็น dictionary
json_data = '{"name": "John", "age": 30, "city": "New York"}'
data = json.loads(json_data)
print(data)


import requests

response = requests.get('https://www.example.com')
print(response.status_code)
print(response.text)

import requests

response = requests.get('https://www.cmuccdc.org/api/ccdc/stations')
print(response.status_code)
print(response.text)
