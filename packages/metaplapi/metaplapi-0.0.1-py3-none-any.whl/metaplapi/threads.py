import os
import re
import json
import time
import uuid
import random
import string
import datetime
import requests

from .device import Device
from .useragent import UserAgent
from .generator import Generator
from .headers import ThreadsHeaders

def cookie_required(function):
    def wrapper(self, *args, **kwargs):
        if not self.cookie:
            raise Exception('require threads cookie to access this features')
        return function(self, *args, **kwargs)
    return wrapper

class Threads:
    
    web = 'https://www.threads.net'
    api = 'https://i.instagram.com/api/v1'
    
    def __init__(
            self,
            cookie      : str               = None,
            bearer      : str               = None,
            device      : dict              = None,
            user_id     : str               = None,
            csrftoken   : str               = None,
            device_id   : str               = None,
            machine_id  : str               = None,
            user_agent  : str               = None,
            proxies     : dict              = None,
            session     : requests.Session  = None,
            **kwargs
        ):
        
        self.cookie     = cookie
        self.generator  = Generator
        
        if cookie and cookie is not None:
            
            bearer = bearer or self.generator.encrypt_bearer(cookie)
            try: user_id = str(re.search(r'ds_user_id=(.*?);', cookie).group(1))
            except: raise Exception('cookie is not valid cannot find ds_user_id in this cookie')
            if not csrftoken: csrftoken = (re.search(r'csrftoken=(.*?);', cookie).group(1) if 'csrftoken' in cookie else self.generator.string(32))
            if not device_id: device_id = (str(uuid.UUID(re.search(r'ig_did=(.*?);', cookie).group(1))) if 'ig_did' in cookie else self.generator.device_id())
            if not machine_id: machine_id = (re.search(r'mid=(.*?);', cookie).group(1) if 'mid' in cookie else self.generator.machine_id())

        self.bearer     = bearer
        self.device     = device or Device(device_country='ID').info()
        self.user_id    = user_id
        self.csrftoken  = csrftoken
        self.device_id  = device_id or self.generator.device_id()
        self.machine_id = machine_id or self.generator.machine_id()
        self.android_id = self.generator.android_id(self.device_id)
        self.user_agent = user_agent or UserAgent(self.device).threads()
        self.proxies    = proxies
        self.private    = session or requests.Session()
        self.private.headers.update(ThreadsHeaders.api(
            x_ig_device_id  = self.device_id,
            x_ig_android_id = self.android_id,
            user_agent      = self.user_agent,
            x_mid           = self.machine_id,
        ))
        self.session    = session or requests.Session()
        self.session.headers.update(ThreadsHeaders.web(
            x_csrftoken     = self.csrftoken,
            user_agent      = self.user_agent,
            x_mid           = self.machine_id,
        ))
        
        if self.cookie and isinstance(self.cookie, str):
            self.private.cookies.update({'cookie': self.cookie})
            self.session.cookies.update({'cookie': self.cookie})
        if self.bearer and isinstance(self.bearer, str):
            self.private.headers.update({'authorization': self.bearer})
        if self.proxies and isinstance(self.proxies, dict):
            self.private.proxies.update(self.proxies)
    
    @staticmethod
    def parser(pattern: str, content: str, default: any = '') -> str:
        match = re.search(pattern, content)
        return match.group(1) if match else default
    
    @staticmethod
    def get_data(response: str) -> dict:
        try:
            return {
                'av':(av := Threads.parser(r'"actorID":"(.*?)"', response)),
                '__user':'0',
                '__a':str(random.randrange(1, 6)),
                '__req':'78',
                '__hs':Threads.parser(r'"haste_session":"(.*?)"', response),
                'dpr':'1.5',
                '__ccg':Threads.parser(r'"connectionClass":"(.*?)"', response),
                '__rev':(__rev := Threads.parser(r'"__spin_r":(.*?),', response)),
                '__s':'4x',
                '__dyn':'',
                '__csr':'',
                '__hsi':Threads.parser(r'"hsi":"(.*?)"', response),
                '__hsdp':'',
                '__hblp':'',
                '__comet_req':'29',
                'fb_dtsg':Threads.parser(r'"DTSGInitialData",\[\],{"token":"(.*?)"}', response),
                'jazoest':Threads.parser(r'jazoest=(.*?)"', response),
                'lsd':Threads.parser(r'"LSD",\[\],{"token":"(.*?)"}', response),
                '__spin_r':__rev,
                '__spin_b':Threads.parser(r'"__spin_b":"(.*?)"', response),
                '__spin_t':Threads.parser(r'"__spin_t":(.*?),', response),
            }
        except Exception:
            return {}
    
    @cookie_required
    def account(self):
        try:
            user = self.private.get(self.api + f'/users/{self.user_id}/info/').json()['user']
            info = {
                'id': user['pk_id'],
                'private': user['is_private'],
                'verified': user['is_verified'],
                'username': user['username'],
                'fullname': user['full_name'],
                'followers': str(user['follower_count']),
                'following': str(user['following_count']),
                'mediapost': str(user['media_count']),
                'biography': user['biography'],
                'pictures': user['hd_profile_pic_url_info']['url']
            }
            return info
        except Exception:
            return False
    
    @cookie_required
    def username(self, username: str = None):
        try:
            user = self.private.get(self.api + f'/users/{username}/usernameinfo/').json()['user']
            info = {
                'id': user['pk_id'],
                'private': user['is_private'],
                'verified': user['is_verified'],
                'username': user['username'],
                'fullname': user['full_name'],
                'followers': str(user['follower_count']),
                'following': str(user['following_count']),
                'mediapost': str(user['media_count']),
                'biography': user['biography'],
                'pictures': user['hd_profile_pic_url_info']['url']}
            return info
        except Exception:
            return False
    
    @cookie_required
    def followers(self, username: str = None):
        user = self.username_info(username)['id']
        html = self.session.get(f'{self.web}/@{username}').text
        data = self.get_data(html)
        end_cursor = None
        has_next_page = True
        while has_next_page:
            try:
                data.update({
                    'fb_api_caller_class':'RelayModern',
                    'fb_api_req_friendly_name':'BarcelonaFriendshipsFollowersTabRefetchableQuery',
                    'variables':json.dumps({
                        "after":end_cursor,
                        "first":10,
                        "id":user,
                        "__relay_internal__pv__BarcelonaIsLoggedInrelayprovider":True,
                        "__relay_internal__pv__BarcelonaIsCrawlerrelayprovider":False,
                        "__relay_internal__pv__BarcelonaHasDisplayNamesrelayprovider":False
                    }),
                    'server_timestamps':True,
                    'doc_id':'9226067564176291',
                })
                post = self.session.post(f'{self.web}/graphql/query', data=data).json()
                page_info = post['data']['fetch__XDTUserDict']['followers']['page_info']
                has_next_page = page_info.get('has_next_page', False)
                for edge in post['data']['fetch__XDTUserDict']['followers']['edges']:
                    yield {
                        'id':edge['node']['id'],
                        'username':edge['node']['username'],
                        'fullname':edge['node']['full_name'],
                    }
                if has_next_page:
                    end_cursor = page_info.get('end_cursor')
            except Exception:
                break
    
    @cookie_required
    def following(self, username: str = None):
        user = self.username_info(username)['id']
        html = self.session.get(f'{self.web}/@{username}').text
        data = self.get_data(html)
        end_cursor = None
        has_next_page = True
        while has_next_page:
            try:
                data.update({
                    'fb_api_caller_class':'RelayModern',
                    'fb_api_req_friendly_name':'BarcelonaFriendshipsFollowingTabRefetchableQuery',
                    'variables':json.dumps({
                        "after":end_cursor,
                        "first":10,
                        "id":user,
                        "__relay_internal__pv__BarcelonaIsLoggedInrelayprovider":True,
                        "__relay_internal__pv__BarcelonaIsCrawlerrelayprovider":False,
                        "__relay_internal__pv__BarcelonaHasDisplayNamesrelayprovider":False
                    }),
                    'server_timestamps':True,
                    'doc_id':'8914031855370781',
                })
                post = self.session.post(f'{self.web}/graphql/query', data=data).json()
                page_info = post['data']['fetch__XDTUserDict']['following']['page_info']
                has_next_page = page_info.get('has_next_page', False)
                for edge in post['data']['fetch__XDTUserDict']['following']['edges']:
                    yield {
                        'id':edge['node']['id'],
                        'username':edge['node']['username'],
                        'fullname':edge['node']['full_name'],
                    }
                if has_next_page:
                    end_cursor = page_info.get('end_cursor')
            except Exception:
                break