"""
## format data to send through MQTT
{
    "parking_type":"checkin",
    "timestamp":"2022-07-29 01:00:00",
    "user_id":1,
    "vehicle_id":1,
    "parking_location_id":1,
    "code":"98375e52-221d-4732-b662-eb9b696e668a"
}

{
    "parking_type":"checkout",
    "timestamp":"2022-07-29 02:59:00",
    "user_id":1,
    "code":"c245e483-18b9-41dc-bf18-01d6d5ddb151"
}

## format data from QRCode
{
    "user_id":1,
    "code":"550bb52e-df73-4658-8f9b-a546621621c9",
    "parking_type":"checkin"
}

{
    "user_id":1,
    "code":"a7f9c0dd-5198-45c3-88ef-0f6166dbdbe4",
    "expired":"2022-07-28 22:17:45",
    "parking_type":"checkout"
}
"""

from datetime import datetime, tzinfo, timedelta
from time import time
from pytz import timezone
import json

DATETIME_FMT = '%Y-%m-%d %H:%M:%S'
TZJAKARTA = timezone("Asia/Jakarta")

class Helper:
    @staticmethod
    def parse_json_qrcode(json_data):
        """ Validate and parse json data to python dict """
        if not json_data:
            return False

        json_obj = json.loads(json_data)
        
        return {
            "code": json_obj.get('code', False),
            "expired": json_obj.get('expired', False),
            "parking_type": json_obj.get('parking_type', False),
            "user_id": json_obj.get('user_id', False),
        }

    @staticmethod
    def format_json_mqtt(data):
        """ Format data to json format """
        if isinstance(data['timestamp'], int):
            
            data['timestamp'] = datetime.fromtimestamp(data['timestamp']/1000, tz=TZJAKARTA).strftime(DATETIME_FMT)
            data["vehicle_id"] = 1
            data["parking_location_id"] = 1
            
        return json.dumps(data)

    @staticmethod
    def parse_to_timestamp(date=datetime_fmt):
        """ will throw datetime.now() when parameter not filled """
        if not datetime_fmt:
            datetime_fmt = datetime.fromtimestamp(time())
        
        if isinstance(datetime_fmt, str):
            datetime_fmt = Helper.parse_datetime(datetime_fmt)

        datetime_fmt = datetime_fmt + timedelta(hours=7)

        return datetime_fmt.timestamp()

    @staticmethod
    def parse_datetime(datetime_str):
        """ parse datetime string with approved  format to datetime object """
        if not datetime_str:
            return False

        return datetime.strptime(datetime_str, DATETIME_FMT)