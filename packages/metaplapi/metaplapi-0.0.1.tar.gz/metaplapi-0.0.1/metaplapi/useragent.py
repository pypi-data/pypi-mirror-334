import random

from .device import Device
from .constant import (
    THREADS_RELEASE,
    FACEBOOK_RELEASE,
    INSTAGRAM_RELEASE
)

class UserAgent:
    
    def __init__(self, device: dict = None):
        self.device = device if device and 'device_brand' in device else Device().info()

    def chrome_version(self):
        return str(random.randint(80,120)) + '.0.' + str(random.randint(2623,6099)) + '.' + str(random.randint(10,224))
    
    def threads_version(self):
        return random.choice(THREADS_RELEASE)
    
    def facebook_version(self):
        return random.choice(FACEBOOK_RELEASE)
    
    def instagram_version(self):
        return random.choice(INSTAGRAM_RELEASE)
    
    def dalvik(self):
        device = self.device.copy()
        return 'Dalvik/2.1.0 (Linux; U; Android {device_version}; {device_model} Build/{device_build})'.format(**device)
    
    def chrome(self, chrome_version: str = None, chrome_platform: str = None, **kwargs):
        device = self.device.copy()
        device['chrome_version'] = chrome_version if chrome_version is not None else self.chrome_version()
        if chrome_platform == 'ios':
            device['device_brand'] = 'iPhone'
            device['device_model'] = random.choice(['CPU iPhone OS 17_3 like Mac OS X','CPU iPhone OS 16_6 like Mac OS X','CPU iPhone OS 15_5 like Mac OS X'])
            device['mobile_version'] = random.choice(['15E148','15G45','15G77'])
            return 'Mozilla/5.0 ({device_brand}; {device_model}) AppleWebKit/537.36 (KHTML, like Gecko) CriOS/{chrome_version} Mobile/{mobile_version} Safari/537.36'.format(**device)
        elif chrome_platform == 'mac':
            device['device_brand'] = 'Macintosh'
            device['device_model'] = random.choice(['Intel Mac OS X 14_2','Intel Mac OS X 13_5','Intel Mac OS X 12_6','Intel Mac OS X 11_6_5','Intel Mac OS X 10_15_7'])
            return 'Mozilla/5.0 ({device_brand}; {device_model}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version} Safari/537.36'.format(**device)
        elif chrome_platform == 'linux':
            device['device_brand'] = 'X11'
            device['device_model'] = random.choice(['Linux x86_64','Linux i686','Ubuntu; Linux x86_64','Debian; Linux x86_64','Fedora; Linux x86_64','Arch Linux; Linux x86_64','Manjaro; Linux x86_64','Kali; Linux x86_64'])
            return 'Mozilla/5.0 ({device_brand}; {device_model}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version} Safari/537.36'.format(**device)
        elif chrome_platform == 'windows':
            device['device_brand'] = 'Windows'
            device['device_model'] = random.choice(['NT 10.0; Win64; x64','NT 10.0; WOW64','NT 6.3; Win64; x64','NT 6.2; Win64; x64','NT 6.1; Win64; x64'])
            return 'Mozilla/5.0 ({device_brand} {device_model}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version} Safari/537.36'.format(**device)
        else:
            return 'Mozilla/5.0 (Linux; Android {device_version}; {device_model} Build/{device_build}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version} Mobile Safari/537.36'.format(**device)
    
    def threads(self, threads_code: str = None, threads_version: str = None, **kwargs):
        device = self.device.copy()
        threads = self.threads_version()
        device['threads_code'] = threads_code if threads_code is not None else threads['code']
        device['threads_version'] = threads_version if threads_version is not None else threads['version']
        return 'Barcelona {threads_version} Android ({device_sdk}/{device_version}; {device_dpi}; {device_brand}; {device_model}; {device_board}; {device_vendor}; {device_language}; {threads_code})'.format(**device)
    
    def facebook(self, facebook_code: str = None, facebook_version: str = None, facebook_package: str = None, dalvik: bool = False, **kwargs):
        device = self.device.copy()
        facebook = self.facebook_version()
        device['facebook_code'] = facebook_code if facebook_code is not None else facebook['code']
        device['facebook_version'] = facebook_version if facebook_version is not None else facebook['version']
        device['facebook_package'] = facebook_package if facebook_package is not None else 'com.facebook.katana'
        fb_agent = '[FBAN/FB4A;FBAV/{facebook_version};FBBV/{facebook_code};FBDM/{device_density};FBLC/{device_language};FBRV/0;FBCR/{device_operator};FBMF/{device_brand};FBBD/{device_brand};FBPN/{facebook_package};FBDV/{device_model};FBSV/{device_version};FBOP/1;FBCA/{device_armeabi}:;]'.format(**device)
        return self.dalvik() + ' ' + fb_agent if dalvik else fb_agent
    
    def instagram(self, instagram_code: str = None, instagram_version: str = None, **kwargs):
        device = self.device.copy()
        instagram = self.instagram_version()
        device['instagram_code'] = instagram_code if instagram_code is not None else instagram['code']
        device['instagram_version'] = instagram_version if instagram_version is not None else instagram['version']
        return 'Instagram {instagram_version} Android ({device_sdk}/{device_version}; {device_dpi}; {device_brand}; {device_model}; {device_board}; {device_vendor}; {device_language}; {instagram_code})'.format(**device)
