import json

def string2json(str_o):
    json_o = json.loads(str_o)
    return json_o

def toString(json_o):
    return json_o.__str__()

