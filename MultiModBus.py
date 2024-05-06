import os
import json

################# End of Main Imports #####################

# Gets the current script directory
current_directory = os.path.dirname(__file__)

# Build the path to the JSON file
path_JSON = os.path.join(current_directory, 'Devices_infos.json')

# Open JSON file
with open(path_JSON) as f:
    data = json.load(f)

IPs = data['IPs']
print("IP list:", IPs)

readCoil = data['read_coil']
print("list of coils to read:", readCoil)

readHR = data['read_holding']
print("list of registers to be read:", readHR)

import ReadModBusAsync as Mod1

for item in IPs:
    print("Now reading the device:", item)
    
    Mod1.asyncio.run(
        Mod1.async_aplication_multi(item, "502", readCoil, readHR)
        )