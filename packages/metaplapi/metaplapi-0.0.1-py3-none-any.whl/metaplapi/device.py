import random

from typing import Optional
from .constant import (
    DEVICE,
    DEVICE_LIST,
    COUNTRY,
    COUNTRY_LIST
)

class Device:
    
    def __init__(
            self,
            device_brand     : Optional[str] = None,
            device_model     : Optional[str] = None,
            device_country   : Optional[str] = None,
            device_operator  : Optional[str] = None,
            **kwargs
        ):
        self.device_brand    = device_brand
        self.device_model    = device_model
        self.device_country  = device_country
        self.device_operator = device_operator
        self.kwargs          = kwargs

    def get_random_dpi(self) -> str:
        return random.choice([
            '480dpi; 1080x2400','480dpi; 720x1600','480dpi; 720x1560',
            '480dpi; 1080x2376','480dpi; 1080x2404','480dpi; 1080x2408',
            '320dpi; 1080x2340','560dpi; 1440x3040','560dpi; 1440x3088',
            '560dpi; 1080x2400','320dpi; 1600x2560','320dpi; 720x1568',
            '560dpi; 1440x2560','480dpi; 1344x2772',
        ])

    def get_random_build(self) -> str:
        build_prefix = random.choice(['SP1A','QP1A','RP1A','TP1A','RKQ1','SKQ1'])
        build_number = str(random.randint(200999, 220905))
        build_suffix = f".0{random.choice(['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16'])}"
        return f"{build_prefix}.{build_number}{build_suffix}"

    def get_random_armeabi(self) -> str:
        return random.choice([
            'arm64-v8a','armeabi-v8a:armeabi','armeabi-v7a:armeabi',
            'x86_64:x86:x86_64','x86_64:arm64-v8a:x86_64'
        ])

    def get_random_density(self) -> str:
        return random.choice([
            '{density=2.0,width=720,height=1193}','{density=2.1,width=1814,height=1023}',
            '{density=1.8,width=1582,height=558}','{density=3.0,width=1080,height=1920}',
            '{density=3.0,width=1080,height=2068}','{density=3.0,width=1080,height=1920}',
            '{density=2.3,width=2149,height=1117}','{density=1.0,width=2060,height=1078}',
        ])

    def get_device_data(self) -> dict:
        if self.device_brand and self.device_brand.upper() in DEVICE_LIST:
            if self.device_model:
                device_data = next((d for d in DEVICE[self.device_brand.upper()] if d['device_model'] == self.device_model),None)
                if not device_data: device_data = random.choice(DEVICE[self.device_brand.upper()])
            else: device_data = random.choice(DEVICE[self.device_brand.upper()])
        else:
            self.device_brand = random.choice(DEVICE_LIST)
            device_data = random.choice(DEVICE[self.device_brand.upper()])
        return device_data

    def get_country_data(self) -> dict:
        if not self.device_country or self.device_country.upper() not in COUNTRY_LIST: self.device_country = random.choice(COUNTRY_LIST)
        return COUNTRY[self.device_country.upper()]

    def info(self) -> dict:
        device_data  = self.get_device_data()
        country_data = self.get_country_data()
        if not self.device_operator: self.device_operator = random.choice(COUNTRY[self.device_country]['operator'])
        return {
            'device_brand'      : self.device_brand.capitalize() if len(self.device_brand) > 3 else self.device_brand,
            'device_model'      : device_data['device_model'],
            'device_board'      : device_data['device_board'],
            'device_build'      : self.get_random_build(),
            'device_vendor'     : device_data['device_vendor'],
            'device_version'    : device_data['device_version'],
            'device_armeabi'    : self.get_random_armeabi(),
            'device_density'    : self.get_random_density(),
            'device_dpi'        : self.get_random_dpi(),
            'device_sdk'        : str(19 + int(device_data['device_version'])),
            'device_number'     : country_data['number'],
            'device_country'    : self.device_country,
            'device_language'   : country_data['language'],
            'device_operator'   : self.device_operator,
            **self.kwargs
        }