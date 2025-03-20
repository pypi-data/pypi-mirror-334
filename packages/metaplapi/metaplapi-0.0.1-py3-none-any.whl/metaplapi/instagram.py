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
from .headers import InstagramHeaders

def cookie_required(function):
    def wrapper(self, *args, **kwargs):
        if not self.cookie:
            raise Exception('require instagram cookie to access this features')
        return function(self, *args, **kwargs)
    return wrapper

class Instagram:
    
    web = 'https://www.instagram.com'
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
        self.generator  = Generator()
        
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
        self.device_id  = device_id or self.generator.device_id()
        self.csrftoken  = csrftoken or self.generator.string(32)
        self.machine_id = machine_id or self.generator.machine_id()
        self.android_id = self.generator.android_id(self.device_id)
        self.user_agent = user_agent or UserAgent(self.device).instagram()
        self.proxies    = proxies
        self.session    = session or requests.Session()
        self.session.headers.update(InstagramHeaders.api(
            x_ig_device_id  = self.device_id,
            x_ig_android_id = self.android_id,
            user_agent      = self.user_agent,
            x_mid           = self.machine_id,
        ))
        
        if self.cookie and isinstance(self.cookie, str):
            self.session.cookies.update({'cookie': self.cookie})
        if self.bearer and isinstance(self.bearer, str):
            self.session.headers.update({'authorization': self.bearer})
        if self.proxies and isinstance(self.proxies, dict):
            self.session.proxies.update(self.proxies)
    
    @cookie_required
    def account(self):
        try:
            user = self.session.get(self.api + f'/users/{self.user_id}/info/').json()['user']
            info = {'id': user['pk_id'], 'email': '', 'phone': '', 'private': user['is_private'], 'verified': user['is_verified'], 'username': user['username'], 'fullname': user['full_name'], 'birthday': '', 'followers': str(user['follower_count']), 'following': str(user['following_count']), 'mediapost': str(user['media_count']), 'biography': user['biography'], 'pictures': user['hd_profile_pic_url_info']['url']}
            user = self.session.get(self.api + '/accounts/current_user/?edit=true').json()['user']
            info['email'] = user['email'] or ''
            info['phone'] = user['phone_number'] or ''
            info['birthday'] = user['birthday'] or ''
            return info
        except Exception:
            return False

    def download(self, url: str, name: str = None, folder: str = None, replace: bool = False):
        folder = folder if folder and os.path.isdir(folder) else os.getcwd()
        os.makedirs(folder, exist_ok=True)
        originals = re.search(r'([^/]+\.(jpg|png|mp4|webp))', url).group(1)
        base_name, extension = os.path.splitext(originals)
        base_name = name or self.generator.string(8)
        existing_files = [f for f in os.listdir(folder) if f.startswith(base_name)]
        if not replace:
            existing_files_with_numbers = [f for f in existing_files if re.match(rf'{re.escape(base_name)}_\d+', f)]
            numbers = [int(re.search(r'_(\d+)', f).group(1)) for f in existing_files_with_numbers]
            numb = max(numbers, default=0) + 1
            file_path = os.path.join(folder, f"{base_name}_{numb}{extension}")
        else:
            file_path = os.path.join(folder, f"{base_name}{extension}")
        try:
            with requests.get(url, stream=True) as session:
                session.raise_for_status()
                with open(file_path, 'wb') as file:
                    for chunk in session.iter_content(chunk_size=8192):
                        file.write(chunk)
            return file_path if os.path.isfile(file_path) else False
        except requests.exceptions.RequestException:
            return False

    @cookie_required
    def username(self, username: str = None):
        try:
            user = self.session.get(self.api + f'/users/{username}/usernameinfo/').json()['user']
            info = {
                'id': user['pk_id'],
                'email': user['public_email'] if 'public_email' in user else '',
                'phone': user['contact_phone_number'] if 'contact_phone_number' in user else '',
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
        except:
            return False
    
    @cookie_required
    def location(self, username: str = None):
        try:
            user = self.session.get(self.api + f'/users/{username}/usernameinfo/').json()['user']
            lttd = user['latitude'] if 'latitude' in user else ''
            lgtd = user['longitude'] if 'longitude' in user else ''
            info = {
                'id': str(user['city_id'] if 'city_id' in user else ''),
                'name': user['city_name'] if 'city_name' in user else '',
                'address': user['address_street'] if 'address_street' in user else '',
                'maps': f'https://www.google.com/maps/search/?api=1&query={lttd},{lgtd}'
            }
            return info if all([lttd, lgtd]) else None
        except:
            return False
    
    @cookie_required
    def followers(self, username: str = None):
        if not username.isdigit(): id = self.username(username=username)['id']
        else: id = username
        end_cursor = None
        has_next_page = True
        while has_next_page:
            try:
                response = self.session.get(self.web + '/graphql/query/', params={'query_hash': 'c76146de99bb02f6415203be841dd25a', 'id': id, 'first': 100, 'after': end_cursor}).json()
                has_next_page = response['data']['user']['edge_followed_by']['page_info']['has_next_page']
                for user in response['data']['user']['edge_followed_by']['edges']:
                    try:
                        data = {'id': user['node']['id'], 'username': user['node']['username'], 'fullname': user['node']['full_name']}
                        yield data
                    except (requests.exceptions.JSONDecodeError, json.decoder.JSONDecodeError): continue
                if has_next_page: end_cursor = response['data']['user']['edge_followed_by']['page_info']['end_cursor']
            except: break
    
    @cookie_required
    def following(self, username: str = None):
        if not username.isdigit(): id = self.username(username=username)['id']
        else: id = username
        end_cursor = None
        has_next_page = True
        while has_next_page:
            try:
                response = self.session.get(self.web + '/graphql/query/', params={'query_hash': 'd04b0a864b4b54837c0d870b0e77e076', 'id': id, 'first': 100, 'after': end_cursor}).json()
                has_next_page = response['data']['user']['edge_follow']['page_info']['has_next_page']
                for user in response['data']['user']['edge_follow']['edges']:
                    try:
                        data = {'id': user['node']['id'], 'username': user['node']['username'], 'fullname': user['node']['full_name']}
                        yield data
                    except (requests.exceptions.JSONDecodeError, json.decoder.JSONDecodeError): continue
                if has_next_page: end_cursor = response['data']['user']['edge_follow']['page_info']['end_cursor']
            except: break
    
    @cookie_required
    def mediapost(self, username: str = None):
        if not username.isdigit(): id = self.username(username=username)['id']
        else: id = username
        next_max_id = ''
        more_available = True
        media_type_number = lambda x: 'image' if x == 1 else ('video' if x == 2 else 'carousel')
        while more_available:
            try:
                response = self.session.get(
                    self.api + f'/feed/user/{id}/',
                    params={
                        'max_id': next_max_id,
                        'count': 0,
                        'min_timestamp': None,
                        'rank_token': f'{id}_{self.generator.uuid()}',
                        'ranked_content': True
                    }).json()
                more_available = response['more_available']
                if more_available: next_max_id = response['next_max_id']
                for media in response['items']:
                    url = []
                    try: caption = media['caption']['text']
                    except: caption = ''
                    try:
                        if media_type_number(media['media_type']) == 'image':
                            url.append(media['image_versions2']['candidates'][0]['url'])
                        elif media_type_number(media['media_type']) == 'video':
                            url.append(media['video_versions'][0]['url'])
                        elif media_type_number(media['media_type']) == 'carousel':
                            for m in media['carousel_media']:
                                if media_type_number(m['media_type']) == 'image':
                                    url.append(m['image_versions2']['candidates'][0]['url'])
                                elif media_type_number(m['media_type']) == 'video': 
                                    url.append(m['video_versions'][0]['url'])
                    except: pass
                    yield {
                        'id': media['id'].split('_')[0],
                        'code': media['code'],
                        'type': media_type_number(media['media_type']),
                        'date': self.generator.timestamp_to_datetime(media['taken_at']),
                        'like': str(media['like_count']),
                        'liked': media['has_liked'],
                        'comment': str(media['comment_count']),
                        'caption': caption,
                        'can_save': media['can_viewer_save'],
                        'can_share': media['can_viewer_reshare'],
                        'can_comment': media.get('has_more_comments', False),
                        'url': url,
                    }
            except: return False

    def media_id(self, url: str = None):
        try:
            media = 0
            base_char = string.ascii_uppercase + string.ascii_lowercase + string.digits + '-_'
            if '/p/' in url: code = re.search(r"/p/([A-Za-z0-9_-]+)/\?", url).group(1)
            elif '/reel/' in url: code = re.search(r"/reel/([A-Za-z0-9_-]+)/\?", url).group(1)
            elif '/story/' in url: code = re.search(r"/story/([A-Za-z0-9_-]+)/\?", url).group(1)
            else: code = ''
            for line in code: media = (media * 64) + base_char.index(line)
            return media
        except:
            return False
    
    @cookie_required
    def media_info(self, url: str = None):
        try:
            if not url.isdigit(): media_id = self.media_id(url)
            else: media_id = url.split('_')[0]
            media = []
            media_type = lambda x: 'image' if x == 1 else ('video' if x == 2 else 'carousel')
            items = self.session.get(self.api + f'/media/{media_id}/info/').json()['items']
            for line in items:
                try: caption = line['caption']['text']
                except: caption = ''
                try: id = line['caption']['user']['id']
                except: id = ''
                try: username = line['caption']['user']['username']
                except: username = ''
                try: fullname = line['caption']['user']['full_name']
                except: fullname = ''
                try:
                    location = {
                        'id': line['location']['facebook_places_id'],
                        'name': line['location']['name'],
                        'address': line['location']['address'],
                        'maps': f'https://www.google.com/maps/search/?api=1&query={line["location"]["lat"]},{line["location"]["lng"]}'
                    }
                except:
                    location = ''
                try: has_more_comments = line['has_more_comments']
                except: has_more_comments = False
                try:
                    if media_type(line['media_type']) == 'image':
                        media.append(line['image_versions2']['candidates'][0]['url'])
                    elif media_type(line['media_type']) == 'video':
                        media.append(line['video_versions'][0]['url'])
                    elif media_type(line['media_type']) == 'carousel':
                        for lines in line['carousel_media']:
                            if media_type(lines['media_type']) == 'image':
                                media.append(lines['image_versions2']['candidates'][0]['url'])
                            elif media_type(lines['media_type']) == 'video': 
                                media.append(lines['video_versions'][0]['url'])
                except: pass
                return {
                    'id': str(line['id']),
                    'code': line['code'],
                    'type': media_type(line['media_type']),
                    'date': self.generator.timestamp_to_datetime(line['taken_at']),
                    'like': str(line['like_count']),
                    'liked': line['has_liked'],
                    'comment': str(line['comment_count']),
                    'caption': caption,
                    'location': location,
                    'can_save': line['can_viewer_save'],
                    'can_share': line['can_viewer_reshare'],
                    'can_comment': has_more_comments,
                    'owner': {
                        'id': id,
                        'username': username,
                        'fullname': fullname
                    },
                    'url': media,
                }
        except:
            return False
    
    @cookie_required
    def upload_id(self, file: str = None, cookie: dict = None, headers: dict = None):
        if not os.path.isfile(file): raise FileNotFoundError(file)
        upload_id = str(int(time.time()) * 1000)
        entity_name = '{}_0_{}'.format(upload_id, random.randint(1000000000, 9999999999))
        params = {'retry_context':'{"num_step_auto_retry": 0, "num_reupload": 0, "num_step_manual_retry": 0}"','media_type':'1','xsharing_user_ids':'[]','upload_id': upload_id,'image_compression':json.dumps({'lib_name':'moz','lib_version':'3.1.m','quality': 80})}
        with open(file,'rb') as f:
            file_data = f.read()
            file_size = str(len(file_data))
        session = requests.Session()
        session.cookies.update(cookie)
        session.headers.update(headers)
        session.headers.update({'Accept-Encoding':'gzip','X-Instagram-Rupload-Params':json.dumps(params),'X_FB_PHOTO_WATERFALL_ID':self.generator.uuid(),'X-Entity-Type':'image/jpeg','Offset':'0','X-Entity-Name':entity_name,'X-Entity-Length':file_size,'Content-Type':'application/octet-stream','Content-Length':file_size})
        upload_id = session.post('https://i.instagram.com/rupload_igphoto/{}'.format(entity_name), data=file_data).json()['upload_id']
        return upload_id
    
    @cookie_required
    def change_biography(self, text: str = None):
        try:
            response = self.session.post(
                self.api + '/accounts/set_biography/',
                data = {
                    'logged_in_uids': self.user_id,
                    'device_id': self.device_id,
                    '__uuid': self.generator.uuid(),
                    'raw_text': text,
                }
            ).json()
            if response['status'] == 'ok': return True
            else: return False
        except:
            return False
    
    @cookie_required
    def change_profile_picture(self, file: str = None):
        try:
            if not os.path.isfile(file): raise FileNotFoundError(file)
            upload_id = self.upload_id(file=file, cookie=self.session.cookies.get_dict().copy(), headers=self.session.headers.copy())
            response = self.session.post(
                self.api + '/accounts/change_profile_picture/',
                data = {
                    '_uuid': self.generator.uuid(),
                    'use_fbuploader': False,
                    'remove_birthday_selfie': False,
                    'upload_id': upload_id
                }
            ).json()
            if response['status'] == 'ok': return True
            else: return False
        except:
            return False
    
    @cookie_required
    def remove_profile_picture(self):
        try:
            response = self.session.post(
                self.api + '/accounts/remove_profile_picture/',
                data = {
                    '_uuid': self.generator.uuid(),
                    'use_fbuploader': False,
                    'remove_birthday_selfie': False,
                    'upload_id': None
                }
            ).json()
            if response['status'] == 'ok': return True
            else: return False
        except:
            return False
    
    @cookie_required
    def change_to_public(self):
        try:
            response = self.session.post(self.api + '/accounts/set_public/').json()
            if response['status'] == 'ok': return True
            else: return False
        except:
            return False
    
    @cookie_required
    def change_to_private(self):
        try:
            response = self.session.post(self.api + '/accounts/set_private/').json()
            if response['status'] == 'ok': return True
            else: return False
        except:
            return False
    
    @cookie_required
    def change_password(self, old_password: str = None, new_password: str = None):
        try:
            enc_old_password = self.encrypt_password(old_password)
            enc_new_password = self.encrypt_password(new_password)
            response = self.session.post(
                self.api + '/accounts/change_password/',
                data = {
                    '_uid': self.user_id,
                    '_uuid': self.device_id,
                    '_csrftoken': self.csrftoken,
                    'enc_old_password': enc_old_password,
                    'enc_new_password1': enc_new_password,
                    'enc_new_password2': enc_new_password
                }
            ).json()
            if response['status'] == 'ok': return True
            else: return False
        except:
            return False
    
    @cookie_required
    def like(self, url: str = None):
        try:
            if not url.isdigit(): media_id = self.media_id(url)
            else: media_id = url
            response = self.session.post(
                self.api + f'/media/{media_id}/like/',
                data = {
                    'media_id': media_id
                }
            ).json()
            if response['status'] == 'ok': return True
            else: return False
        except:
            return False
    
    @cookie_required
    def unlike(self, url: str = None):
        try:
            if not url.isdigit(): media_id = self.media_id(url)
            else: media_id = url
            response = self.session.post(
                self.api + f'/media/{media_id}/unlike/',
                data = {
                    'media_id': media_id
                }
            ).json()
            if response['status'] == 'ok': return True
            else: return False
        except:
            return False
    
    @cookie_required
    def block(self, username: str = None):
        try:
            if not username.isdigit(): id = self.username(username=username)['id']
            else: id = username
            response = self.session.post(
                self.api + f'/friendships/block/{id}/',
                data = {
                    'surface': 'profile',
                    'is_auto_block_enabled': 'true',
                    'user_id':id,
                    '_uid': self.user_id,
                    '__uuid': self.device_id,
                    'container_module': 'profile'
                }
            ).json()
            if response['status'] == 'ok': return True
            else: return False
        except:
            return False
    
    @cookie_required
    def unblock(self, username: str = None):
        try:
            if not username.isdigit(): id = self.username(username=username)['id']
            else: id = username
            response = self.session.post(
                self.api + f'/friendships/unblock/{id}/',
                data = {
                    'user_id': id,
                    '_uid': self.user_id,
                    '__uuid': self.device_id,
                    'container_module': 'search_typeahead'
                }
            ).json()
            if response['status'] == 'ok': return True
            else: return False
        except:
            return False
    
    @cookie_required
    def follow(self, username: str = None):
        try:
            if not username.isdigit(): id = self.username(username=username)['id']
            else: id = username
            response = self.session.post(
                self.api + f'/friendships/create/{id}/',
                data = {
                    'user_id': id
                }
            ).json()
            if response['status'] == 'ok': return True
            else: return False
        except:
            return False
    
    @cookie_required
    def unfollow(self, username: str = None):
        try:
            if not username.isdigit(): id = self.username(username=username)['id']
            else: id = username
            response = self.session.post(
                self.api + f'/friendships/destroy/{id}/',
                data = {
                    'user_id': id
                }
            ).json()
            if response['status'] == 'ok': return True
            else: return False
        except:
            return False
    
    @cookie_required
    def comment(self, url: str = None, text: str = None):
        try:
            if not url.isdigit(): media_id = self.media_id(url)
            else: media_id = url
            text = text if text is not None else random.choice(['Nice post! 👍', 'Good work bro! 💯', 'Alatnya bagus banget, gw suka! 😍', 'Gw kira boongan, ternyata work cuy! 🔥', 'Mantap banget ini alat! 👏', 'Keren banget, auto recommend! 🚀', 'Wih, ini beneran ngebantu banget! 🙌', 'Nice banget, langsung work! 😎', 'Good job! Alatnya oke punya! 💪', 'Ini alat beneran nggak ngecewain! 😁', 'Wah, keren banget! Auto save! 📂', 'Nice, langsung coba dan puas! 😄', 'Alatnya simpel tapi powerful! 💥', 'Gw suka banget sama ini! 👍', 'Ini beneran worth it, cuy! 💸', 'Good work, alatnya beneran ngebantu! 🙏', 'Wih, langsung work tanpa ribet! 🎉', 'Nice post, beneran informatif! 📚', 'Alatnya beneran bagus, gw puas! 😊', 'Keren banget, auto jadi favorit! ⭐', 'Ini beneran nggak boong, work banget! 🔥', 'Good job, alatnya beneran ngebantu! 💯', 'Wah, langsung suka sama ini! 😍', 'Nice, beneran sesuai ekspektasi! 😎', 'Alatnya beneran nggak ngecewain! 👌', 'Ini beneran keren, auto recommend! 🚀', 'Good work, langsung work tanpa error! 🙌', 'Wih, beneran ngebantu banget! 💪', 'Nice post, langsung coba dan puas! 😄', 'Alatnya beneran simpel tapi powerful! 💥', 'Gw suka banget sama ini, beneran worth it! 💸', 'Ini beneran nggak boong, work banget! 🔥', 'Good job, alatnya beneran ngebantu! 🙏', 'Wah, langsung suka sama ini! 😍', 'Nice, beneran sesuai ekspektasi! 😎', 'Alatnya beneran nggak ngecewain! 👌', 'Ini beneran keren, auto recommend! 🚀', 'Good work, langsung work tanpa error! 🙌', 'Wih, beneran ngebantu banget! 💪', 'Nice post, langsung coba dan puas! 😄', 'Alatnya beneran simpel tapi powerful! 💥', 'Gw suka banget sama ini, beneran worth it! 💸', 'Ini beneran nggak boong, work banget! 🔥', 'Good job, alatnya beneran ngebantu! 🙏', 'Wah, langsung suka sama ini! 😍', 'Nice, beneran sesuai ekspektasi! 😎', 'Alatnya beneran nggak ngecewain! 👌', 'Ini beneran keren, auto recommend! 🚀', 'Good work, langsung work tanpa error! 🙌', 'Wih, beneran ngebantu banget! 💪', 'Nice post, langsung coba dan puas! 😄', 'Alatnya beneran simpel tapi powerful! 💥', 'Gw suka banget sama ini, beneran worth it! 💸', 'Ini beneran nggak boong, work banget! 🔥', 'Good job, alatnya beneran ngebantu! 🙏', 'Wah, langsung suka sama ini! 😍', 'Nice, beneran sesuai ekspektasi! 😎', 'Alatnya beneran nggak ngecewain! 👌', 'Ini beneran keren, auto recommend! 🚀', 'Good work, langsung work tanpa error! 🙌', 'Wih, beneran ngebantu banget! 💪', 'Nice post, langsung coba dan puas! 😄', 'Alatnya beneran simpel tapi powerful! 💥', 'Gw suka banget sama ini, beneran worth it! 💸', 'Ini beneran nggak boong, work banget! 🔥', 'Good job, alatnya beneran ngebantu! 🙏', 'Wah, langsung suka sama ini! 😍', 'Nice, beneran sesuai ekspektasi! 😎', 'Alatnya beneran nggak ngecewain! 👌', 'Ini beneran keren, auto recommend! 🚀', 'Good work, langsung work tanpa error! 🙌', 'Wih, beneran ngebantu banget! 💪', 'Nice post, langsung coba dan puas! 😄', 'Alatnya beneran simpel tapi powerful! 💥', 'Gw suka banget sama ini, beneran worth it! 💸', 'Ini beneran nggak boong, work banget! 🔥', 'Good job, alatnya beneran ngebantu! 🙏', 'Wah, langsung suka sama ini! 😍', 'Nice, beneran sesuai ekspektasi! 😎', 'Alatnya beneran nggak ngecewain! 👌', 'Ini beneran keren, auto recommend! 🚀', 'Good work, langsung work tanpa error! 🙌', 'Wih, beneran ngebantu banget! 💪', 'Nice post, langsung coba dan puas! 😄', 'Alatnya beneran simpel tapi powerful! 💥', 'Gw suka banget sama ini, beneran worth it! 💸', 'Ini beneran nggak boong, work banget! 🔥', 'Good job, alatnya beneran ngebantu! 🙏', 'Wah, langsung suka sama ini! 😍', 'Nice, beneran sesuai ekspektasi! 😎', 'Alatnya beneran nggak ngecewain! 👌', 'Ini beneran keren, auto recommend! 🚀', 'Good work, langsung work tanpa error! 🙌', 'Wih, beneran ngebantu banget! 💪', 'Nice post, langsung coba dan puas! 😄', 'Alatnya beneran simpel tapi powerful! 💥', 'Gw suka banget sama ini, beneran worth it! 💸', 'Ini beneran nggak boong, work banget! 🔥', 'Good job, alatnya beneran ngebantu! 🙏', 'Wah, langsung suka sama ini! 😍', 'Nice, beneran sesuai ekspektasi! 😎', 'Alatnya beneran nggak ngecewain! 👌', 'Ini beneran keren, auto recommend! 🚀', 'Good work, langsung work tanpa error! 🙌', 'Wih, beneran ngebantu banget! 💪'])
            response = self.session.post(
                self.api + f'/media/{media_id}/comment/',
                data = {
                    'comment_text': text
                }
            ).json()
            if response['status'] == 'ok': return True
            else: return False
        except:
            return False
    
    @cookie_required
    def direct_message(self, username: str = None, text: str = None):
        try:
            if not username.isdigit(): id = self.username(username=username)['id']
            else: id = username
            text = text if text is not None else 'Hai! pesan ini dikirim menggunakan instahack 👋🏻\n\nhttps://github.com/iqbalmh18/instahack'
            data = {'action':'send_item','client_context':self.generator.uuid(),'recipient_users':'[['+id+']]','__uuid':self.device_id}
            if 'https' in str(text):
                path = 'link'
                data.update({'link_text': text})
            else:
                path = 'text'
                data.update({'text': text})
            response = self.session.post(
                self.api + f'/direct_v2/threads/broadcast/{path}/',
                data=data
            ).json()
            if response['status'] == 'ok': return True
            else: return False
        except:
            return False
    
    @cookie_required
    def direct_message_photo(self, username: str = None, file: str = None):
        try:
            if not os.path.isfile(file): raise FileNotFoundError(file)
            if not username.isdigit(): id = self.username(username=username)['id']
            else: id = username
            upload_id = self.upload_id(file=file, cookie=self.session.cookies.get_dict().copy(), headers=self.session.headers.copy())
            response = self.session.post(
                self.api + f'/direct_v2/threads/broadcast/configure_photo/',
                data = {
                    'action': 'send_item',
                    'send_attribution': 'inbox',
                    'client_context': self.generator.uuid(),
                    '__uuid': self.device_id,
                    'upload_id': upload_id,
                    'recipient_users':'[['+id+']]',
                    'allow_full_aspect_ratio':'true'
                }
            ).json()
            if response['status'] == 'ok': return True
            else: return False
        except:
            return False
    
    @cookie_required
    def upload_photo(self, file: str = None, caption: str = None):
        try:
            if not os.path.isfile(file): raise FileNotFoundError(file)
            upload_id = self.upload_id(file=file, cookie=self.session.cookies.get_dict().copy(), headers=self.session.headers.copy())
            response = self.session.post(
                self.api + '/media/configure/',
                data = {
                    '_uid': self.user_id,
                    '__uuid': self.device_id,
                    'device_id': self.device_id,
                    'custom_accessibility_caption': caption,
                    'caption': caption,
                    'upload_id': upload_id
                }
            ).json()
            if response['status'] == 'ok': return True
            else: return False
        except:
            return False
            
    @cookie_required
    def upload_photo_sidecar(self, file_list: list = None, caption: str = None):
        try:
            upload_id = []
            for file in file_list:
                if not os.path.isfile(file): raise FileNotFoundError(file)
                upid = self.upload_id(file=file, cookie=self.session.cookies.det_dict().copy(), headers=self.session.headers.copy())
                if upid: upload_id.append(upid)
            response = self.session.post(
                self.api + '/media/configure_sidecar/',
                data = {
                    '_uid': self.user_id,
                    '__uuid': self.device_id,
                    'device_id': self.device_id,
                    'client_sidecar_id': str(int(time.time() * 1000)),
                    'source_type': '4',
                    'caption': caption,
                    'children_metadata': [{
                        'upload_id': upid,
                        'source_type': '4',
                        'custom_accessibility_caption': caption
                    } for upid in upload_id]
                }
            ).json()
            if response['status'] == 'ok': return True
            else: return False
        except:
            return False
    
    @cookie_required
    def upload_photo_story(self, file: str = None, caption: str = None, resolution: tuple[int, int] = (1080, 1920)):
        try:
            if not os.path.isfile(file): raise FileNotFoundError(file)
            upload_id = self.upload_id(file=file, cookie=self.session.cookies.get_dict().copy(), headers=self.session.headers.copy())
            date = datetime.datetime.now()
            data = {
                "supported_capabilities_new": "[{\"name\":\"SUPPORTED_SDK_VERSIONS\",\"value\":\"131.0,132.0,133.0,134.0,135.0,136.0,137.0,138.0,139.0,140.0,141.0,142.0,143.0,144.0,145.0,146.0,147.0,148.0,149.0,150.0,151.0,152.0,153.0,154.0,155.0,156.0,157.0,158.0,159.0\"},{\"name\":\"FACE_TRACKER_VERSION\",\"value\":\"14\"},{\"name\":\"COMPRESSION\",\"value\":\"ETC2_COMPRESSION\"},{\"name\":\"gyroscope\",\"value\":\"gyroscope_enabled\"}]",
                "has_original_sound": "1",
                "camera_entry_point": "12",
                "original_media_type": "1",
                "camera_session_id": self.generator.uuid(),
                "date_time_digitalized": f"{date.year}:{date.month:02}:{date.day:02} {date.hour:02}:{date.minute:02}:{date.second:02}",
                "camera_model": self.device["device_model"],
                "scene_capture_type": "",
                "timezone_offset": (datetime.datetime.fromtimestamp(date.timestamp() * 1e-3) - datetime.datetime.utcfromtimestamp(date.timestamp() * 1e-3)).seconds,
                "client_shared_at": int(date.timestamp()),
                "story_sticker_ids": "",
                "configure_mode": "1",
                "source_type": "3",
                "camera_position": "front",
                "_uid": self.user_id,
                "device_id": self.device_id,
                "composition_id": self.generator.uuid(),
                "_uuid": self.generator.uuid(),
                "creation_surface": "camera",
                "can_play_spotify_audio": "1",
                "date_time_original": f"{date.year}:{date.month:02}:{date.day:02} {date.hour:02}:{date.minute:02}:{date.second:02}",
                "capture_type": "normal",
                "upload_id": upload_id,
                "client_timestamp": int(date.timestamp()),
                "private_mention_sharing_enabled": "1",
                "media_transformation_info": f"{{\"width\":\"{resolution[0]}\",\"height\":\"{resolution[1]}\",\"x_transform\":\"0\",\"y_transform\":\"0\",\"zoom\":\"1.0\",\"rotation\":\"0.0\",\"background_coverage\":\"0.0\"}}",
                "camera_make": self.device["device_brand"],
                "device": {
                    "manufacturer": self.device["device_brand"],
                    "model": self.device["device_model"],
                    "android_version": int(self.device["device_sdk"]),
                    "android_release": self.device["device_version"]
                },
                "edits": {
                    "filter_type": 0,
                    "filter_strength": 1.0,
                    "crop_original_size": [
                        float(resolution[0]),
                        float(resolution[1])
                    ]
                },
                "extra": {
                    "source_width": resolution[0],
                    "source_height": resolution[1]
                }
            }
            if caption: data["caption"] = caption
            response = self.session.post(self.api + '/media/configure_to_story/', data={"signed_body": "SIGNATURE." + json.dumps(data)}).json()
            if response['status'] == 'ok': return True
            else: return False
        except:
            return False