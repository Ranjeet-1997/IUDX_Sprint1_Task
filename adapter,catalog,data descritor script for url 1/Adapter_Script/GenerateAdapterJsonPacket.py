import requests
import json
import time
import schedule
import dateutil.parser
time_formatter = "%Y-%m-%dT%H:%M:%S+05:30"
def fetch_data():
    response = requests.get("http://220.227.12.155/vsclapi/SWMService.svc/GetVehicleDetails")
    new_l = response.json()
    new_data = new_l['vehicleDetails']
    # Filter the Duplicate data
    seen = set()
    data = []
    for d in new_data:
        t = tuple(d.items())
        if t not in seen:
            seen.add(t)
            data.append(d)
    length = len(data)
    lostOfData = []
    for i in range(length):
        rs_data = {}
        try:
            rs_data["id"] = "resource-server-name/resource-group-name/resource-item-name"
            rs_data["resourceGroup"] = "varanasi-swm-vehicles"
            rs_data["observationDateTime"] = dateutil.parser.parse(data[i]["dateTime"]).strftime(time_formatter)
            rs_data["vehicleRunningStatus"] = data[i]['VehicleStatus']
            rs_data["vehicleAltitude"] = data[i]['altitude']
            rs_data["vehicleBearing"] = data[i]['angle']
            rs_data["deviceBatteryStatus"] = data[i]['batteryStatus']
            rs_data["ignitionStatus"] = data[i]['ignition']
            rs_data["location"] = {}
            rs_data["location"]["coordinates"] = []
            rs_data["location"]["coordinates"].append(data[i]["longitude"])
            rs_data["location"]["coordinates"].append(data[i]["latitude"])
            rs_data["deviceSimNumber"] = data[i]['simNo']
            rs_data["vehicleSpeed"] = data[i]['speed']
            rs_data["vehicleType"] = data[i]['vehicleType']
            rs_data["vehicleLicenscePlate"] = data[i]['vehicleNo']
            rs_data["wardID"] = data[i]['wardNo']
            lostOfData.append(rs_data)
        except Exception as e:
            print("error in process_response")
            print(e)
    print(json.dumps(lostOfData, indent=4))
schedule.every(10).minutes.do(fetch_data)
while True:
    schedule.run_pending()
    time.sleep(1)









