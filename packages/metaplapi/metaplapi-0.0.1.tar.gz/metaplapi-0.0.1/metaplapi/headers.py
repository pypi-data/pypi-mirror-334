import re
import string
import random
import datetime

from .generator import Generator
from .useragent import UserAgent

def set_chrome_useragent(user_agent):
    version = find.group(1) if (find := re.search(r'(?:Chrome|CriOS)/(\d+\.\d+\.\d+\.\d+)', user_agent)) else (UserAgent().chrome_version())
    pattern = {
        'iPhone': ('2.75', '"iOS"', '?1'),
        'Macintosh': ('1', '"macOS"', '?0'),
        'Windows': ('1', '"Windows"', '?0'),
        'X11': ('1', '"Linux"', '?0'),
        'Android': ('2.75', '"Android"', '?1')
    }
    dpr, platform, mobile = next((value for key, value in pattern.items() if key in user_agent), ('1', '"Unknown"', '?0'))
    return {
        'dpr': dpr,
        'sec-ch-prefers-color-scheme': random.choice(['dark', 'light']),
        'sec-ch-ua': f'"Not/A)Brand";v="8", "Chromium";v="{version.split(".")[0]}", "Google Chrome";v="{version.split(".")[0]}"',
        'sec-ch-ua-full-version-list': f'"Chromium";v="{version}", "Google Chrome";v="{version}", "Not/A)Brand";v="8"',
        'sec-ch-ua-mobile': mobile,
        'sec-ch-ua-platform': platform,
        'user-agent': user_agent,
    }

class ThreadsHeaders:
    
    @staticmethod
    def web(method: str = 'get', **kwargs):
        kwargs = {key.replace('_','-'): value for key, value in kwargs.items() if kwargs}
        agents = kwargs.pop('user-agent', UserAgent().chrome())
        return {
            'authority': 'www.threads.net',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US;q=0.8,en;q=0.7',
            'accept-encoding': 'gzip, deflate',
            'cache-control': 'max-age=0',
            'pragma': 'no-cache',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            **kwargs,
            **set_chrome_useragent(agents),
        } if method.lower() == 'get' else {
            'authority': 'www.threads.net',
            'accept': '*/*',
            'accept-language': 'en-US;q=0.8,en;q=0.7',
            'accept-encoding': 'gzip, deflate',
            'content-type': 'application/x-www-form-urlencoded',
            'content-length': str(random.randint(1000,1800)),
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'origin': f'https://www.threads.net',
            'referer': f'https://www.threads.net/login?hl=en',
            **kwargs,
            **set_chrome_useragent(agents),
            'x-asbd-id': '359341',
            'x-ig-app-id': '1412234116260832' if 'iPhone' in agents or 'Android' in agents else '238260118697367',
            'x-csrftoken': Generator.csrftoken(22),
            'x-instagram-ajax': '0',
            'x-bloks-version-id': '057c41cc15ea08e8f8a4a55ff49ae274dff45f744ad7d173aa98c6668f53e53f',
        }
    
    @staticmethod
    def api(method: str = 'get', **kwargs):
        kwargs = {key.replace('_','-'): value for key, value in kwargs.items() if kwargs}
        return {
            'host': 'i.instagram.com',
            'accept': '*/*',
            'connection': 'Keep-Alive',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'id-ID, en-US',
            'x-ig-app-id': '3419628305025917',
            'x-ig-device-id': kwargs.pop('x-ig-device-id', Generator.device_id()),
            'x-ig-android-id': kwargs.pop('x-ig-android-id', Generator.android_id()),
            'x-ig-family-device-id': kwargs.pop('x-ig-family-device-id', Generator.family_device_id()),
            'x-ig-connection-type': kwargs.pop('x-ig-connection-type', 'MOBILE(LTE)'),
            'x-fb-connection-type': kwargs.pop('x-fb-connection-type', 'MOBILE.LTE'),
            'user-agent': kwargs.pop('user-agent', UserAgent().threads()),
            'x-mid': kwargs.pop('x-mid', Generator.machine_id()),
            **kwargs,
        } if method.lower() == 'get' else {
            'host': 'i.instagram.com',
            'accept': '*/*',
            'connection': 'Keep-Alive',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'id-ID, en-US',
            'content-length': str(random.randint(2345,3456)),
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'priority': 'u=3',
            'ig-intended-user-id': '0',
            'x-ig-www-claim': '0',
            'x-ig-app-id': '3419628305025917',
            'x-ig-app-locale': 'in_ID',
            'x-ig-device-locale': 'in_ID',
            'x-ig-mapped-locale': 'id_ID',
            'x-ig-device-id': kwargs.pop('x-ig-device-id', Generator.device_id()),
            'x-ig-android-id': kwargs.pop('x-ig-android-id', Generator.android_id()),
            'x-ig-family-device-id': kwargs.pop('x-ig-family-device-id', Generator.family_device_id()),
            'x-ig-capabilities': kwargs.pop('x-ig-capabilities', '3brTv10='),
            'x-ig-connection-type': kwargs.pop('x-ig-connection-type', 'MOBILE(LTE)'),
            'x-ig-bandwidth-speed-kbps': '{}.000'.format(str(random.randint(1200,1418))),
            'x-ig-bandwidth-totalbytes-b': str(random.randint(1320000,1323526)),
            'x-ig-bandwidth-totaltime-ms': str(random.randint(888,999)),
            'x-ig-timezone-offset': str(datetime.datetime.now().astimezone().utcoffset().seconds),
            'x-pigeon-session-id': kwargs.pop('x-pigeon-session-id', Generator.pigeon_session_id()),
            'x-pigeon-rawclienttime': kwargs.pop('x-pigeon-rawclienttime', Generator.pigeon_raw_client_time()),
            'x-bloks-version-id': kwargs.pop('x-bloks-version-id', '5f56efad68e1edec7801f630b5c122704ec5378adbee6609a448f105f34a9c73'),
            'x-bloks-is-prism-enabled': 'false',
            'x-bloks-is-layout-rtl': 'false',
            'x-tigon-is-retry': 'True, True',
            'x-fb-connection-type': kwargs.pop('x-ig-connection-type', 'MOBILE(LTE)'),
            'x-fb-http-engine': 'Liger',
            'x-fb-client-ip': 'True',
            'x-fb-server-cluster': 'True',
            'x-mid': kwargs.pop('x-mid', Generator.machine_id()),
            'user-agent': kwargs.pop('user-agent', UserAgent().threads()),
            **kwargs,
        }

class FacebookHeaders:
    
    @staticmethod
    def web(method: str = 'get', **kwargs):
        kwargs = {key.replace('_','-'): value for key, value in kwargs.items() if kwargs}
        agents = kwargs.pop('user-agent', UserAgent().chrome())
        return {
            'authority': 'm.facebook.com' if 'iPhone' in agents or 'Android' in agents else 'web.facebook.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US;q=0.8,en;q=0.7',
            'accept-encoding': 'gzip, deflate',
            'cache-control': 'max-age=0',
            'pragma': 'no-cache',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            **kwargs,
            **set_chrome_useragent(agents),
        } if method.lower() == 'get' else {
            'authority': 'm.facebook.com' if 'iPhone' in agents or 'Android' in agents else 'web.facebook.com',
            'accept': '*/*',
            'accept-language': 'en-US;q=0.8,en;q=0.7',
            'accept-encoding': 'gzip, deflate',
            'content-type': 'application/x-www-form-urlencoded',
            'content-length': str(random.randint(1000,1800)),
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'origin': 'https://m.facebook.com' if 'iPhone' in agents or 'Android' in agents else 'https://web.facebook.com',
            'referer': 'https://m.facebook.com/' if 'iPhone' in agents or 'Android' in agents else 'https://web.facebook.com/',
            **kwargs,
            **set_chrome_useragent(agents),
        }

class InstagramHeaders:
    
    @staticmethod
    def web(method: str = 'get', **kwargs):
        kwargs = {key.replace('_','-'): value for key, value in kwargs.items() if kwargs}
        agents = kwargs.pop('user-agent', UserAgent().chrome())
        return {
            'authority': 'www.instagram.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US;q=0.8,en;q=0.7',
            'accept-encoding': 'gzip, deflate',
            'cache-control': 'max-age=0',
            'pragma': 'no-cache',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            **kwargs,
            **set_chrome_useragent(agents)
        } if method.lower() == 'get' else {
            'authority': 'www.instagram.net',
            'accept': '*/*',
            'accept-language': 'en-US;q=0.8,en;q=0.7',
            'accept-encoding': 'gzip, deflate',
            'content-type': 'application/x-www-form-urlencoded',
            'content-length': str(random.randint(1000,1800)),
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'origin': f'https://www.instagram.com',
            'referer': f'https://www.instagram.com/accounts/login/',
            **kwargs,
            **set_chrome_useragent(agents),
            'x-asbd-id': '359341',
            'x-ig-app-id': '1217981644879628' if 'iPhone' in agents or 'Android' in agents else '936619743392459',
            'x-ig-www-claim': '0',
            'x-instagram-ajax': '1020718735',
            'x-requested-with': 'XMLHttpRequest',
            'x-web-session-id': f'{Generator.string(6)}:{Generator.string(6)}:{Generator.string(6)}',
            'x-csrftoken': Generator.csrftoken(),
        }
    
    @staticmethod
    def api(method: str = 'get', **kwargs):
        kwargs = {key.replace('_','-'): value for key, value in kwargs.items() if kwargs}
        return {
            'host': 'i.instagram.com',
            'accept': '*/*',
            'connection': 'Keep-Alive',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'id-ID, en-US',
            'x-ig-app-id': '567067343352427',
            'x-ig-device-id': kwargs.pop('x-ig-device-id', Generator.device_id()),
            'x-ig-android-id': kwargs.pop('x-ig-android-id', Generator.android_id()),
            'x-ig-family-device-id': kwargs.pop('x-ig-family-device-id', Generator.family_device_id()),
            'x-ig-connection-type': kwargs.pop('x-ig-connection-type', 'MOBILE(LTE)'),
            'x-fb-connection-type': kwargs.pop('x-fb-connection-type', 'MOBILE.LTE'),
            'user-agent': kwargs.pop('user-agent', UserAgent().instagram()),
            'x-mid': kwargs.pop('x-mid', Generator.machine_id()),
            **kwargs,
        } if method.lower() == 'get' else {
            'host': 'i.instagram.com',
            'accept': '*/*',
            'connection': 'Keep-Alive',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'id-ID, en-US',
            'content-length': str(random.randint(2345,3456)),
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'priority': 'u=3',
            'ig-intended-user-id': '0',
            'x-ig-www-claim': '0',
            'x-ig-app-id': '567067343352427',
            'x-ig-app-locale': 'in_ID',
            'x-ig-device-locale': 'in_ID',
            'x-ig-mapped-locale': 'id_ID',
            'x-ig-device-id': kwargs.pop('x-ig-device-id', Generator.device_id()),
            'x-ig-android-id': kwargs.pop('x-ig-android-id', Generator.android_id()),
            'x-ig-family-device-id': kwargs.pop('x-ig-family-device-id', Generator.family_device_id()),
            'x-ig-capabilities': kwargs.pop('x-ig-capabilities', '3brTv10='),
            'x-ig-connection-type': kwargs.pop('x-ig-connection-type', 'MOBILE(LTE)'),
            'x-ig-bandwidth-speed-kbps': '{}.000'.format(str(random.randint(1200,1418))),
            'x-ig-bandwidth-totalbytes-b': str(random.randint(1320000,1323526)),
            'x-ig-bandwidth-totaltime-ms': str(random.randint(888,999)),
            'x-ig-timezone-offset': str(datetime.datetime.now().astimezone().utcoffset().seconds),
            'x-pigeon-session-id': kwargs.pop('x-pigeon-session-id', Generator.pigeon_session_id()),
            'x-pigeon-rawclienttime': kwargs.pop('x-pigeon-rawclienttime', Generator.pigeon_raw_client_time()),
            'x-bloks-version-id': kwargs.pop('x-bloks-version-id', '16e9197b928710eafdf1e803935ed8c450a1a2e3eb696bff1184df088b900bcf'),
            'x-bloks-is-prism-enabled': 'false',
            'x-bloks-is-layout-rtl': 'false',
            'x-fb-connection-type': kwargs.pop('x-ig-connection-type', 'MOBILE(LTE)'),
            'x-fb-http-engine': 'Liger',
            'x-fb-client-ip': 'True',
            'x-fb-server-cluster': 'True',
            'x-mid': kwargs.pop('x-mid', Generator.machine_id()),
            'user-agent': kwargs.pop('user-agent', UserAgent().instagram()),
            **kwargs,
        }