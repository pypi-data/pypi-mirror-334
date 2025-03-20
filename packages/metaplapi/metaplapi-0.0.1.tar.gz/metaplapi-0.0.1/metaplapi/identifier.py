import random
import itertools

from typing import Union

class Identifier:
    
    def __init__(self,
            firstname: str,
            last_name: str = '',
            domain: Union[str, list] = None,
            result: Union[int, None] = None
        ):
        
        if domain and domain is not None:
            domain = domain if isinstance(domain, list) else [domain]
        if result and isinstance(result, int):
            result = result if result <= 5000 else 1000
        
        self.firstname = firstname
        self.last_name = last_name
        self.domain = domain or ['gmail.com','yahoo.com','outlook.com']
        self.result = result or 1000
    
    def fullname(self):
        fullname = f'{self.firstname} {self.last_name}'
        return [fullname] * self.result
    
    def wordlist(self, capitalize: bool = False):
        years = [str(y) for y in range(1995, 2026)]
        month = [f'{m:02d}' for m in range(1, 13)]
        dates = [f'{d:02d}' for d in range(1, 32)]
        digit = [str(d) for d in range(1, 10000)]
        firstname = [self.firstname]
        last_name = [self.last_name]
        patterns = [
            (lambda f, d: f + d, (firstname, digit)),
            (lambda f, day: f + day, (firstname, dates)),
            (lambda f, m: f + m, (firstname, month)),
            (lambda f, y: f + y[-2:], (firstname, years)),
            (lambda f, y: f + y, (firstname, years)),
            (lambda f, day, m, y: f + day + m + y[:2], (firstname, dates, month, years)),
            (lambda f, d: f + d, (last_name, digit)),
            (lambda f, day: f + day, (last_name, dates)),
            (lambda f, m: f + m, (last_name, month)),
            (lambda f, y: f + y[-2:], (last_name, years)),
            (lambda f, y: f + y, (last_name, years)),
            (lambda f, day, m, y: f + day + m + y[:2], (last_name, dates, month, years)),
            (lambda f, l, d: f + l + d, (firstname, last_name, digit)),
            (lambda f, l, day: f + l + day, (firstname, last_name, dates)),
            (lambda f, l, m: f + l + m, (firstname, last_name, month)),
            (lambda f, l, y: f + l + y, (firstname, last_name, years)),
            (lambda f, l, day, m, y: f + l + day + m + y[:2], (firstname, last_name, dates, month, years)),
        ]
        wordlist = set()
        for func, lists in patterns:
            args = [random.choice(lst) for lst in lists]
            wordlist.add(func(*args))
        while len(wordlist) < self.result:
            func, lists = random.choice(patterns)
            args = [random.choice(lst) for lst in lists]
            wordlist.add(func(*args))
        wordlist = list(wordlist)
        if capitalize: wordlist = [word.capitalize() for word in wordlist]
        else: wordlist = [word.lower() for word in wordlist]
        random.shuffle(wordlist)
        return wordlist

    def username(self):
        username = set()
        fullname = self.fullname()
        numerics = range(1,10000)
        patterns = [
            '{fn}{ln}',
            '{fn}.{ln}',
            '{fn}{ln}_',
            '{fn}_{ln}',
            '{fn}{ln}{nm}',
            '{fn}{ln}.{nm}',
            '{fn}.{ln}.{nm}',
            '{fn}{ln}_{nm}',
            '{fn}{ln}{nm}_',
        ]
        for nm, pt in itertools.product(numerics, patterns):
            nu = pt.format(fn=self.firstname, ln=self.last_name, nm=nm).strip('_')
            if nu not in username: username.add(nu)
            if len(username) >= self.result: break
        return [{'identify': identify.lower(),'fullname': fullname[0]} for identify in username]

    def email(self):
        email = set()
        username = self.username()
        for users in username:
            email.add(f'{users["identify"]}@{random.choice(self.domain)}')
            if len(email) >= self.result: break
        return [{'identify': identify.lower(),'fullname': users['fullname']} for identify in email]