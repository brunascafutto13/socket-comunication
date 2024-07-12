import json

print("Str para dict")

obj = '{"name": "Reginaldo"}'

temp = json.loads(obj, )

print(type(obj))
print()
print(obj)
print()
print(type(temp))
print()
print(temp)


print("Dict para str")

obj = {
  "name": "Reginaldo"
}

temp = json.dumps(obj)

print(type(obj))
print()
print(obj)
print()
print(type(temp))
print()
print(temp)
