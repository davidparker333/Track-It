import os

class Track_Config():
    key = os.environ.get('SHIPENGINE_API')
    base = 'https://api.shipengine.com/v1/tracking?'
    headers = {"Host": "api.shipengine.com", "API-Key": key}
    carrier_codes = {
        "FedEx": "fedex",
        "USPS": "usps",
        "UPS": "ups"
    }