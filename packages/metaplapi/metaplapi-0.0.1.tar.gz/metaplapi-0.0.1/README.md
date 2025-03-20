# MetaPlapi
**Python Library for Interacting with Meta Platforms Api: Threads, Facebook, and Instagram**  

MetaPlapi is a powerful and flexible Python library designed to interact with Meta's social media platforms api, including Threads, Facebook, and Instagram. It provides tools for automating tasks, managing accounts, scraping data, and customizing device configurations to avoid suspicious activity. Built with developers in mind, metaplapi offers full control over account management, media post scraping, and more.

## Requirements
| Library       | Installation                  | 
|---------------|-------------------------------|
| Requests      | `pip install requests`        |
| Pycryptodomex | `pip install pycryptodomex`   |

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Customize](#customize)
- [Advance](#advance)
- [Authors](#authors)

## Installation
install with pip
```bash
pip install metaplapi
```  
install with clone repository
```bash
git clone https://github.com/iqbalmh18/metaplapi
cd metaplapi
pip install .
```

## Quick Start
example usage of `metaplapi` for threads
```python
from metaplapi import Threads

# set new threads session
tr = Threads(cookie='YOUR THREADS COOKIE')

# get account info
print(tr.account())

# get username info
print(tr.username('username')

# get followers from target username
foll = tr.followers('username')
for user in foll:
    print(user)

# get following from target username
foll = tr.following('username')
for user in foll:
    print(user)
```

example usage of `metaplapi` for facebook
```python
from metaplapi import Facebook

# set new facebook session
fb = Facebook(cookie='YOUR THREADS COOKIE')

# get account info
print(fb.account())

# get friends from target id
frnd = fb.friends('facebook_id')
for user in frnd:
    print(user)

# get followers from target id
foll = fb.followers('facebook_id')
for user in foll:
    print(user)

# get following from target id
foll = fb.following('facebook_id')
for user in foll:
    print(user)
```

example usage of `metaplapi` for instagram
```python
from metaplapi import Instagram

# set new instagram session
ig = Instagram(cookie='YOUR INSTAGRAM COOKIE')

# get account info
print(ig.account())

# get username info
print(ig.username('username')

# get location info from username
print(ig.location('username')

# get followers from target username
foll = ig.followers('username')
for user in foll:
    print(user)

# get following from target username
foll = ig.following('username')
for user in foll:
    print(user)

# get mediapost from target username
media = ig.mediapost('username')
for post in media:
    print(post)

# get media info from media id or url
url = 'https://www.instagram.com/p/XXXX'
print(ig.media_info(url))
```

## Customize
Check Available Device
```python
from metaplapi import DEVICE, DEVICE_LIST

print(DEVICE)
print(DEVICE_LIST)
```
Check Available Country
```python
from metaplapi import COUNTRY, COUNTRY_LIST

print(COUNTRY)
print(COUNTRY_LIST)
```
Device Customization  
```python  
from metaplapi import Device  

device = Device(device_brand='Samsung', device_model='SM-A125F', device_country='ID')  
info = device.info()  
print(info)  
```  
User Agent Customization
```python
from metaplapi import Device, UserAgent

device = Device(device_brand='Samsung', device_model='SM-A125F', device_country='ID')  
useragent = UserAgent(device)

print(useragent.dalvik())
print(useragent.threads())
print(useragent.facebook())
print(useragent.instagram())
```

## Advance
example usage of `metaplapi` for advance users
```python  
from metaplapi import (
    Device,
    UserAgent,
    Generator,
    Instagram
)

cookies = 'YOUR INSTAGRAM COOKIE'  
proxies = {'http': 'protocol:ip:port', 'https': 'protocol:ip:port'}
devices = Device('Samsung').info()

useragent = UserAgent(devices)
generator = Generator()
device_id = generator.device_id()

ig = Instagram(cookie=cookies, device=devices, device_id=device_id, proxies=proxies)

info = ig.account()
if info:
    print(info)
    print(ig.session.headers)
else:
    print('cookie is not valid or have been expired')
```

example usage to generate `identifier` for advance users
```python  
from metaplapi import Identifier  

identify = Identifier(firstname='john', last_name='doe', domain=['gmail.com','yahoo.com'], result=10)  

emails = identify.email()  
for email in emails:  
    print(email)  
    
usernames = identify.username()
for username in usernames:
    print(username)

fullname = identify.fullname()
print(fullname)

wordlist = identify.wordlist()
print(wordlist)
```  

## Authors
<p align="center">
  <img src="https://2.gravatar.com/avatar/883c7ebdf4f802eeeaafad5c229372afdb625e67de197c88272fa2fcf12256fb?size=512" width="150" style="border-radius: 50%;">
  <br>
  <b>Iqbalmh18</b>
  <br>
  <a href="https://instagram.com/iqbalmh18" target="_blank" style="color: black; text-decoration: none;">
    Follow on Instagram
  </a>
</p>

[*back to top*](#metaplapi)