import re
import hmac
import json
import time
import uuid
import base64
import random
import string
import urllib
import hashlib
import datetime
import requests

from typing import Union
from urllib.parse import quote, urlencode

from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES, PKCS1_v1_5
from Cryptodome.Random import get_random_bytes

from .device import Device
from .useragent import UserAgent

class Generator:
    
    @staticmethod
    def uuid(heex: bool = False, seed: Union[str, dict] = None, upper: bool = False):
        if seed is not None:
            hash = hashlib.md5()
            hash.update(seed.encode('utf-8'))
            _uid = uuid.UUID(hash.hexdigest())
        else:
            _uid = uuid.uuid4()
        if heex: return str(_uid.hex).upper() if upper else str(_uid.hex)
        return str(_uid).upper() if upper else str(_uid)
    
    @staticmethod
    def nonce(seed: str = None):
        seed = seed if seed is not None else '12345'
        seed = base64.b64encode(hashlib.sha256(seed.encode('utf-8')).digest())
        return seed.decode('utf-8')
    
    @staticmethod
    def digit(size: int = 12):
        return ''.join(random.choices(string.digits, k=size))
    
    @staticmethod
    def string(size: int = 16, char: bool = False):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=size))
    
    @staticmethod
    def jazoest(seed: str = None):
        seed = seed if seed is not None else Generator.android_id()
        return f'2{sum(ord(line) for line in seed)}'
    
    @staticmethod
    def android_id(device_id: any = None):
        seed = str(device_id if device_id and device_id is not None else Generator.uuid()).replace('-','')
        hash = hashlib.sha256(seed.encode())
        return 'android-' + hash.hexdigest()[:16]
    
    @staticmethod
    def csrftoken(size: int = 32):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=size))
    
    @staticmethod
    def machine_id(size: int = 28):
        return ''.join(random.choices(string.ascii_letters + string.digits + '_-', k=size))
    
    @staticmethod
    def device_id():
        return Generator.uuid(False)
    
    @staticmethod
    def family_device_id(upper: bool = False):
        return Generator.uuid(upper=upper)
    
    @staticmethod
    def pigeon_session_id():
        return 'UFS-' + Generator.uuid(False) + '-' + random.choice(['0', str(random.randint(1,6))])
    
    @staticmethod
    def pigeon_raw_client_time():
        return str(round(time.time(), 3))
    
    @staticmethod
    def timestamp():
        return datetime.datetime.now().timestamp()
    
    @staticmethod
    def timestamp_to_datetime(timestamp: Union[str, int]):
        date = datetime.datetime.fromtimestamp(timestamp)
        return date.strftime('%Y-%m-%d %H:%M:%S')
    
    @staticmethod
    def wordlist(username: str = '', fullname: str = '', combolist: list = [], capitalize: bool = False):
        if combolist and isinstance(combolist, list): combolist = combolist.copy()
        else: combolist = ['123','12345']
        wordlist = []
        digit = ''.join([str(line) for line in username if line.isdigit()])
        users = username.replace(digit,'').replace('.','').replace('_','')
        names = ''.join(line.lower() for line in fullname if line.isalpha() or line.isspace())
        if len(digit) > 0: combolist.append(digit)
        for combo in combolist:
            for name in names.split(' '):
                if len(name) >= 4: wordlist.append(name + combo)
            wordlist.append(users.replace(' ','') + combo)
            wordlist.append(names.replace(' ','') + combo)
        wordlist = [word for word in wordlist if all(ord(line) < 128 for line in word)]
        wordlist = [word.replace(' ','') for word in wordlist if len(word) >= 8]
        if capitalize: wordlist = [line.capitalize() for line in wordlist]
        wordlist = sorted(wordlist, key=len)
        return list(dict.fromkeys(wordlist))
    
    @staticmethod
    def signature(data: dict = None, ig_sig_key: str = 'SIGNATURE', ig_sig_key_version: str = None):
        if ig_sig_key.isdigit():
            return urlencode({
                'signed_body': hmac.new(ig_sig_key.encode('utf-8'), json.dumps(data).encode('utf-8'), hashlib.sha256).hexdigest() + '.' + quote(json.dumps(data)),
                'ig_sig_key_version': ig_sig_key_version
            })
        else:
            if ig_sig_key_version is not None:
                return urlencode({
                    'signed_body': ig_sig_key + '.' + quote(json.dumps(data)),
                    'ig_sig_key_version': ig_sig_key_version
                })
            return urlencode({
                'signed_body': ig_sig_key + '.' + quote(json.dumps(data))
            })
    
    @staticmethod
    def cookie_string(cookie: dict = None, device_id: str = None, machine_id: str = None):
        if not isinstance(cookie, dict):
            return cookie
        if not 'mid' in cookie:
            if machine_id is not None:
                cookie['mid'] = machine_id
            else:
                cookie['mid'] = Generator.machine_id()
        if not 'ig_did' in cookie:
            if device_id is not None:
                cookie['ig_did'] = device_id.upper()
            else:
                cookie['ig_did'] = Generator.device_id(True)
        return '; '.join([key + '=' + value for key, value in cookie.items()]) if cookie is not None else ''
    
    @staticmethod
    def encrypt_bearer(cookie: str = None):
        try: return 'Bearer IGT:2:{}'.format(base64.b64encode(str({'ds_user_id': re.search('ds_user_id=(.*?);', str(cookie)).group(1), 'sessionid': re.search('sessionid=(.*?);', str(cookie) + ';').group(1), 'should_use_header_over_cookies': True}).replace("'",'"').replace('True','true').replace(' ','').encode('ascii')).decode('ascii'))
        except: return None
    
    @staticmethod
    def decrypt_bearer(bearer: str = None):
        cookie = json.loads(base64.urlsafe_b64decode(bearer.split(':')[-1]).decode('utf-8'))
        try: cookie.pop('should_use_header_over_cookies')
        except: pass
        return Generator.cookie_string(cookie)
    
    @staticmethod
    def encrypt_key(session: requests.Session = None):
        devices = Device(device_country='ID').info()
        devices['device_id'] = Generator.device_id()
        devices['machine_id'] = Generator.machine_id()
        devices['android_id'] = Generator.android_id(devices.get('device_id'))
        session = session or requests.Session()
        session.headers.update({
            'Host': 'i.instagram.com',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': '{}, en-US'.format(devices.get('device_language').replace('_','-')),
            'X-Ig-App-Id': '567067343352427',
            'X-Ig-Device-ID': devices.get('device_id'),
            'X-Ig-Android-ID': devices.get('android_id'),
            'X-Ig-Connection-Type': 'MOBILE(LTE)',
            'X-Fb-Connection-Type': 'MOBILE.LTE',
            'X-Fb-Http-Engine': 'Liger',
            'X-MID': devices.get('machine_id'),
            'User-Agent': UserAgent(devices).instagram()
        })
        data = {
            'bool_opt_policy': '0',
            'mobileconfigsessionless': '',
            'api_version': '3',
            'unit_type': '1',
            'use_case': 'STANDARD',
            'query_hash': '6894cdfea7fb5941e14847d18d1cf2d7c6679cec82e4f786a48fb6a7ace73131',
            'ts': str(Generator.timestamp())[:10],
            'device_id': devices.get('device_id'),
            'fetch_mode':'CONFIG_SYNC_ONLY',
            'fetch_type':'ASYNC_FULL',
            'family_device_id': Generator.family_device_id()
        }
        post = session.post('https://i.instagram.com/api/v1/launcher/mobileconfig/', data=data)
        if 'ig-set-password-encryption-key-id' in post.headers:
            return {
                'public_key': post.headers.get('ig-set-password-encryption-pub-key'),
                'public_key_id': post.headers.get('ig-set-password-encryption-key-id')
            }
        return False
    
    @staticmethod
    def encrypt_password(password: str = None, timestamp: str = None, public_key: str = None, public_key_id: int = None):
        iv = get_random_bytes(12)
        session_key = get_random_bytes(32)
        public_key_id = int(public_key_id) if public_key_id else 84
        timestamp = timestamp if timestamp is not None else str(Generator.timestamp())[:10]
        recipient_key = RSA.import_key(base64.b64decode(public_key) if public_key is not None else '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA6YDHRy+STuxk22W1q99e\nORQ1+PblCy8hMftYHGfUROG9wB4irNjcVW9tyvoBv84KNd2OKX0vM7fBvLf5NT1S\nvWLz68kcoQFHkLl1flTcZzfR8rzjlkTjIaa79+SGTMpgME6E2YlhupNShfwOGxa8\nqhucjmdg/wpXWVT0JBoipGY58TtMV+zOVyEuk9cSbqLhKSEQ9WtqTOqpii7J380B\nMYm1BHLJj5WbRkOdRzcZzHYSEB2jqaUo/yb3mfUBOSuvU2GuKHooyUFwLSid75Tv\nYlzwOUvD7Q6ESGl+AnX3jmXKr5RqEBlByIfdWUyaKA7X025BaHXXKzdnlJARsffq\nfQIDAQAB\n-----END PUBLIC KEY-----')
        cipher_rsa = PKCS1_v1_5.new(recipient_key)
        rsa_encrypted = cipher_rsa.encrypt(session_key)
        cipher_aes = AES.new(session_key, AES.MODE_GCM, iv)
        cipher_aes.update(timestamp.encode())
        aes_encrypted, tag = cipher_aes.encrypt_and_digest(password.encode('utf-8'))
        size_buffer = len(rsa_encrypted).to_bytes(2, byteorder='little')
        payload = base64.b64encode(b''.join([b'\x01',public_key_id.to_bytes(1, byteorder='big'),iv,size_buffer,rsa_encrypted,tag,aes_encrypted]))
        return f'#PWD_INSTAGRAM:4:{timestamp}:{payload.decode()}'