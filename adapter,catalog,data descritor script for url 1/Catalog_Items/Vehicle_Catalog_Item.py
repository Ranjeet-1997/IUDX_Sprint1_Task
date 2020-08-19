import json
import requests
from collections import OrderedDict
response=requests.get("http://220.227.12.155/vsclapi/SWMService.svc/GetVehicleDetails")
new_data=response.json()
new_l = new_data['vehicleDetails']
# Filter the Duplicate data 
seen=set()
data=[]
for d in new_l:
    t=tuple(d.items())
    if t not in seen:
        seen.add(t)
        data.append(d)
l=len(data)
a=[]
for i in range(l):
    item = {}
    item["@context"] = "https://voc.iudx.org.in/"
    item["type"] = ["iudx:Resource", "iudx:WmgmtVehicle"]
    item["id"] = "abc"
    item["name"] = data[i]['vehicleNo']
    item["description"] = "List of DataModels belonging to the UrbanMobility domain in Varanasi city."
    item["tags"] = ["vehicleNo", "speed", "longitude", "latitude", "dateTime", "VehicleStatus", "altitude", "angle",
                    "batteryStatus", "ignition", "location", "simNo"]
    item["itemStatus"] = "ACTIVE"
    item["resourceGroup"] = "provider.org/SHA/rs-varanasi.iudx.org.in/varanasi-UrbanMobility"
    item["itemCreatedAt"] = "2020-08-16T10:03:26+0000"
    item["location"] = {
        "type": "Place",
        "geometry": {
            "type": "Point",
            "coordinates": [
                data[i]['longitude'],
                data[i]['latitude']
            ]
        }
    }
    item["provider"] = "provider.org/SHA"
    item["itemModifiedAt"] = "2020-07-01T10:03:26+0000"
    a.append(item)
with open("catalog_item.jsonld", "w+") as outs:
    json.dump(a, outs, indent=4)

