import os
import math
import asyncio
import xml.etree.ElementTree as ET
from configparser import ConfigParser
import pytak
import getfmi as fmi

COT_URL = os.getenv("COT_URL")
TAK_PROTO = os.getenv("TAK_PROTO","0")
PYTAK_TLS_CLIENT_CERT = os.getenv("PYTAK_TLS_CLIENT_CERT")
PYTAK_TLS_CLIENT_KEY = os.getenv("PYTAK_TLS_CLIENT_KEY")
PYTAK_TLS_DONT_VERIFY = os.getenv("PYTAK_TLS_DONT_VERIFY","1")

def weather2cot(sensor):
    uid = f"fmisensor.{sensor["id"]}"
    root = ET.Element("event")
    root.set("version", "2.0")
    root.set("type", "b-w-A-t")
    root.set("uid", uid)
    root.set("how", "m-c")
    root.set("time", pytak.cot_time())
    root.set("start", pytak.cot_time())
    root.set("stale", pytak.cot_time(120))

    pt_attr = {
        "lat": f'{sensor["lat"]}',
        "lon": f'{sensor["lon"]}',
        "hae": "0",
        "ce": "10",
        "le": "10",
    }
    
    ET.SubElement(root, "point", attrib=pt_attr)

    callsign = f"{sensor["name"]}"
    contact = ET.Element("contact")
    contact.set("callsign", callsign)

    remarks = ET.Element("remarks")
    remarks.text = f"Temperature: {sensor["temp"]}°C"
    if not math.isnan(sensor["ws"]):
        remarks.text += f"\nWind speed: {sensor["ws"]}m/s"
    if not math.isnan(sensor["wd"]):
        remarks.text += f"\nWind direction: {sensor["wd"]}°"
    remarks.text += "\n#weather"

    detail = ET.Element("detail")
    detail.append(contact)
    detail.append(remarks)

    root.append(detail)

    return ET.tostring(root)
        

class sendWeather(pytak.QueueWorker):

    async def handle_data(self, data):
        """Handle pre-CoT data, serialize to CoT Event, then puts on queue."""
        event = data
        await self.put_queue(event)

    async def run(self):
        """Run the loop for processing or generating pre-CoT data."""
        while 1:
            data = bytes()
            sensors = fmi.getweather()
            for sensor in sensors:
                data += weather2cot(sensor)
#            self._logger.info("Sent:\n%s\n", data.decode())
            await self.handle_data(data)
            await asyncio.sleep(60)


async def main():
    config = ConfigParser()
    config["mycottool"] = {
        "COT_URL": COT_URL,
        "TAK_PROTO": TAK_PROTO,
        "PYTAK_TLS_CLIENT_CERT": PYTAK_TLS_CLIENT_CERT,
        "PYTAK_TLS_CLIENT_KEY": PYTAK_TLS_CLIENT_KEY,
        "PYTAK_TLS_DONT_VERIFY": PYTAK_TLS_DONT_VERIFY
    }
    config = config["mycottool"]

    clitool = pytak.CLITool(config)
    await clitool.setup()

    clitool.add_tasks(set([
        sendWeather(clitool.tx_queue, config),
    ]))

    await clitool.run()


if __name__ == "__main__":
    asyncio.run(main())

