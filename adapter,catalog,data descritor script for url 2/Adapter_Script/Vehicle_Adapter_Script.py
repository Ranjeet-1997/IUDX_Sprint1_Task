import requests
import json
import time
import dateutil.parser
time_formatter = "%Y-%m-%dT%H:%M:%S+05:30"
response=requests.get("http://220.227.12.155/vsclapi/SWMService.svc/GetTrailDetailsByVehicleNo/UP65HT3952/15-Oct-2019%2023:55:28/16-Oct-2019%2023:55:28")
new_data=response.json()
new_l = new_data['trailDetails']
# Filter the Duplicate data
seen=set()
data=[]
for d in new_l:
    t=tuple(d.items())
    if t not in seen:
        seen.add(t)
        data.append(d)
length=len(data)
listOfData=[]
for i in range(length):
    rs_data = {}
    try:
        rs_data["id"] = "resource-server-name/resource-group-name/resource-item-name"
        rs_data["resourceGroup"] = "varanasi-swm-vehicles"
        rs_data["observationDateTime"] = dateutil.parser.parse(data[i]["dateTime"]).strftime(time_formatter)
        rs_data["location"] = {}
        rs_data["location"]["coordinates"] = []
        rs_data["location"]["coordinates"].append(data[i]["longitude"])
        rs_data["location"]["coordinates"].append(data[i]["latitude"])
        rs_data["vehicleSpeed"] =data[i]['speed']
        rs_data["vehicleLicenscePlate"] =data[i]['vehicleNo']
        listOfData.append(rs_data)
    except Exception as e:
        print("error in process_response")
        print(e)
print(json.dumps(listOfData, indent=4))

