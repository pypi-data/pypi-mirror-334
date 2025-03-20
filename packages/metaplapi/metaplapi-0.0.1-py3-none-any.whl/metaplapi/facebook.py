import os
import re
import json
import uuid
import random
import datetime
import requests

from .useragent import UserAgent
from .generator import Generator
from .headers import FacebookHeaders

def cookie_required(function):
    def wrapper(self, *args, **kwargs):
        if not self.cookies:
            raise Exception('require facebook cookie to access this features')
        return function(self, *args, **kwargs)
    return wrapper

class Facebook:
    
    web = 'https://web.facebook.com'
    api = 'https://graph.facebook.com'
    
    def __init__(self, cookie: str = None):
        self.cookies = cookie
        self.windows = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        self.headers = {'get': FacebookHeaders.web('get', cookie=self.cookies, user_agent=self.windows), 'post': FacebookHeaders.web('post', cookie=self.cookies, user_agent=self.windows)}
        self.session = requests.Session()
        self.session.headers.update(self.headers.get('get'))
        self.session.cookies.update({'cookie': self.cookies} if self.cookies else {})
        self.user_id = re.search(r'c_user=(\d+)', self.cookies).group(1) if self.cookies and 'c_user' in cookie else None

    @staticmethod
    def parser(pattern: str, content: str, default: any = '') -> str:
        match = re.search(pattern, content)
        return match.group(1) if match else default

    def get_id(self, link_or_username: str) -> str | None:
        link = link_or_username.replace('m.facebook','web.facebook').replace('www.facebook','web.facebook') if link_or_username.startswith('https') else os.path.join(self.web, link_or_username)
        response = self.session.get(link, allow_redirects=True)
        response.raise_for_status()
        html = response.text.replace('\\','')
        for pattern in [r'"userID"\s*:\s*"(.*?)"', r'"actor_id"\s*:\s*"(.*?)"']:
            if fbid := self.parser(pattern, html, None):
                return fbid
        raise Exception(f'failed to get user id from {link_or_username}')

    def get_link(self, user: str, path: str = '') -> str:
        fbid = self.get_id(user) if user.startswith('https') else user
        return f'{self.web}/{fbid}{"/" + path if path else ""}'
    
    @staticmethod
    def get_data(response: str) -> dict:
        try:
            return {
                'av':(av := Facebook.parser(r'"actorID":"(.*?)"', response)),
                '__user':av,
                '__a':str(random.randrange(1, 6)),
                '__hs':Facebook.parser(r'"haste_session":"(.*?)"', response),
                'dpr':'1.5',
                '__ccg':Facebook.parser(r'"connectionClass":"(.*?)"', response),
                '__rev':(__rev := Facebook.parser(r'"__spin_r":(.*?),', response)),
                '__spin_r':__rev,
                '__spin_b':Facebook.parser(r'"__spin_b":"(.*?)"', response),
                '__spin_t':Facebook.parser(r'"__spin_t":(.*?),', response),
                '__hsi':Facebook.parser(r'"hsi":"(.*?)"', response),
                '__comet_req':'15',
                'fb_dtsg':Facebook.parser(r'"DTSGInitialData",\[\],{"token":"(.*?)"}', response),
                'jazoest':Facebook.parser(r'jazoest=(.*?)"', response),
                'lsd':Facebook.parser(r'"LSD",\[\],{"token":"(.*?)"}', response),
            }
        except Exception:
            return {}
    
    @cookie_required
    def friends(self, user: str) -> dict:
        response = self.session.get(self.get_link(user))
        response.raise_for_status()
        html = response.text.replace('\\', '')
        tab_key = self.parser(r'{"tab_key":"friends_all","id":"(.*?)"}', html)
        if not tab_key:
            return {}
        data = self.get_data(html)
        end_cursor = None
        has_next_page = True
        while has_next_page:
            try:
                data.update({
                    'fb_api_caller_class':'RelayModern',
                    'fb_api_req_friendly_name':'ProfileCometAppCollectionListRendererPaginationQuery',
                    'variables':json.dumps({
                        "count":8,
                        "cursor":end_cursor,
                        "scale":3,
                        "search":None,
                        "id":tab_key
                    }),
                    'server_timestamps':True,
                    'doc_id':'9394039170688660'
                })
                post = self.session.post(f'{self.web}/api/graphql', headers=self.headers.get('post'), data=data).json()
                page_info = post['data']['node']['pageItems']['page_info']
                has_next_page = page_info.get('has_next_page', False)
                for edge in post['data']['node']['pageItems']['edges']:
                    yield {
                        'id':edge['node']['node']['id'],
                        'username':edge['node']['node']['url'].split('/')[-1] if not 'profile.php?id=' in edge['node']['node']['url'] else '',
                        'fullname':edge['node']['title']['text'],
                    }
                if has_next_page:
                    end_cursor = page_info.get('end_cursor')
            except IOError:
                break
    
    @cookie_required
    def account(self) -> dict:
        response = self.session.get('https://accountscenter.facebook.com/personal_info')
        response.raise_for_status()
        html = response.text.replace('\\','')
        info = {}
        info['id'] = self.parser(r'"USER_ID":"(.*?)"', html)
        find = self.parser(r'"navigation_row_subtitle":"(.*?)","node_id":"CONTACT_POINT",', html)
        if find:
            emails = [item.replace('u0040','@') for item in find.split(',') if '.com' in item]
            phones = [item.strip() for item in find.split(',') if '+' in item]
            info['email'] = emails[0] if emails else ''
            info['phone'] = phones[0] if phones else ''
        find = self.parser(r'"navigation_row_subtitle":"(.*?)"\s*,\s*"node_id":"BIRTHDAY"', html)
        if find:
            info['birthday'] = find.split('"')[-1]
        info['fullname'] = self.parser(r'"NAME":"(.*?)"', html)
        info['username'] = self.parser(r'"username":"(.*?)"', html)
        info['pictures'] = self.parser(r'"profilePicLarge":{"uri":"(.*?)"}', self.session.get(self.get_link(info['id'])).text.replace('\\',''))
        return info if info['id'] and info['id'] != '0' else {}
    
    @cookie_required
    def followers(self, user: str) -> dict:
        response = self.session.get(self.get_link(user))
        response.raise_for_status()
        html = response.text.replace('\\', '')
        tab_key = self.parser(r'{"tab_key":"followers","id":"(.*?)"}', html)
        if not tab_key:
            return {}
        data = self.get_data(html)
        end_cursor = None
        has_next_page = True
        while has_next_page:
            try:
                data.update({
                    'fb_api_caller_class':'RelayModern',
                    'fb_api_req_friendly_name':'ProfileCometAppCollectionListRendererPaginationQuery',
                    'variables':json.dumps({
                        "count":8,
                        "cursor":end_cursor,
                        "scale":3,
                        "search":None,
                        "id":tab_key
                    }),
                    'server_timestamps':True,
                    'doc_id':'9394039170688660'
                })
                post = self.session.post(f'{self.web}/api/graphql', headers=self.headers.get('post'), data=data).json()
                page_info = post['data']['node']['pageItems']['page_info']
                has_next_page = page_info.get('has_next_page', False)
                for edge in post['data']['node']['pageItems']['edges']:
                    yield {
                        'id':edge['node']['node']['id'],
                        'username':edge['node']['node']['url'].split('/')[-1] if not 'profile.php?id=' in edge['node']['node']['url'] else '',
                        'fullname':edge['node']['title']['text'],
                    }
                if has_next_page:
                    end_cursor = page_info.get('end_cursor')
            except Exception:
                break
    
    @cookie_required
    def following(self, user: str) -> dict:
        response = self.session.get(self.get_link(user))
        response.raise_for_status()
        html = response.text.replace('\\', '')
        tab_key = self.parser(r'{"tab_key":"following","id":"(.*?)"}', html)
        print(tab_key)
        if not tab_key:
            return {}
        data = self.get_data(html)
        end_cursor = None
        has_next_page = True
        while has_next_page:
            try:
                data.update({
                    'fb_api_caller_class':'RelayModern',
                    'fb_api_req_friendly_name':'ProfileCometAppCollectionListRendererPaginationQuery',
                    'variables':json.dumps({
                        "count":8,
                        "cursor":end_cursor,
                        "scale":3,
                        "search":None,
                        "id":tab_key
                    }),
                    'server_timestamps':True,
                    'doc_id':'9394039170688660'
                })
                post = self.session.post(f'{self.web}/api/graphql', headers=self.headers.get('post'), data=data).json()
                page_info = post['data']['node']['pageItems']['page_info']
                has_next_page = page_info.get('has_next_page', False)
                for edge in post['data']['node']['pageItems']['edges']:
                    yield {
                        'id':edge['node']['node']['id'],
                        'username':edge['node']['node']['url'].split('/')[-1] if not 'profile.php?id=' in edge['node']['node']['url'] else '',
                        'fullname':edge['node']['title']['text'],
                    }
                if has_next_page:
                    end_cursor = page_info.get('end_cursor')
            except Exception:
                break
    
    @cookie_required
    def application(self) -> list:
        response = self.session.post(f'{self.web}/setting')
        response.raise_for_status()
        html = response.text.replace('\\', '')
        data = self.get_data(html)
        apps = []
        apps_list_data = [
            {'node': 'activeApps', 'query': 'ApplicationAndWebsitePaginatedSettingAppGridListActiveQuery', 'doc_id': '28619574884357662'},
            {'node': 'expiredApps', 'query': 'ApplicationAndWebsitePaginatedSettingAppGridListExpiredQuery', 'doc_id': '28698012099813736'}
        ]
        for web in apps_list_data:
            node = web['node']
            body = data.copy()
            body.update({'fb_api_req_friendly_name': web['query'], 'doc_id': web['doc_id']})
            end_cursor = None
            has_next_page = True
            while has_next_page:
                try:
                    body['variables'] = json.dumps({'after': end_cursor, 'first': 6, 'id': body['__user']})
                    response = self.session.post(f'{self.web}/api/graphql', headers=self.headers.get('post'), data=body).json()
                    page_info = response['data']['node'][node]['page_info']
                    has_next_page = page_info.get('has_next_page', False)
                    for edge in response['data']['node'][node]['edges']:
                        item = edge['node']['apps_and_websites_view']['detailView']
                        app_info = {
                            'id': item['app_id'],
                            'name': item['app_name'],
                            'since': datetime.datetime.fromtimestamp(int(item['install_timestamp'])).strftime('%Y-%m-%d %H:%M:%S'),
                            'status': item['app_status'].lower(),
                            'picture': item['logo_url']
                        }
                        apps.append(app_info)
                    end_cursor = page_info.get('end_cursor')
                except Exception:
                    break
        return apps