from utils.leagues_loader import load_config
import json

data = load_config()

print(data)

for i in data:
    print(type(i["id"]))
    # print(i)