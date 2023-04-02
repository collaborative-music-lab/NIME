# https://realpython.com/python-json/
# https://www.w3schools.com/python/python_json.asp
import json

mapName = "thisMapping.json"

def loadMap(filename):
	'''load a josn file with mapping data'''
	with open(filename) as f:
		mapDict = json.load(f)

		print (json.dumps(mapDict, indent=4))
		return mapDict
# with open(mapName,"w") as write_file:
# 	json.dump(data, write_file, indent=4)

