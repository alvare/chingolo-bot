import re
import requests
import random
import shelve

import config


def help():
    msg = """
*Command list*

`/js <library>` - checks if library is cool or not
`/vape <text>` - A E S T H E T I C S
`/sadness` - cry
`/puppy` - good doggo
`/remember <keyword> <text>` - have memories
`/urban <word>` - cool dict
`/help` - return this
    """
    return 'message', {'text': msg, 'parse_mode': 'Markdown'}


def js(string):
    def messages(desc, pop):
        n = pop*100
        tmpl = '{}: {}.\nScore: {:.1f} out of 100, {}'
        if n > 90:
            m = 'cool as fuck'
        elif n > 80:
            m = 'pretty ok'
        elif n > 70:
            m = 'meh'
        elif n > 60:
            m = 'old'
        elif n > 50:
            m = 'deprecated'
        elif n > 40:
            m = 'lol seriously?'
        elif n > 30:
            m = 'lol seriously?'
        elif n > 20:
            m = 'please die'
        elif n > 20:
            m = '...'
        elif n > 10:
            m = 'burn your computer'
        else:
            m = 'Exception("<commits suicide>")'

        return tmpl.format(string, desc, n, m)

    if not string:
        return None, None
    else:
        r = requests.get('https://api.npms.io/v2/search?q={}'.format(string))
        if r.ok:
            data = r.json()
            if data['results']:
                pop = data['results'][0]['score']['detail']['popularity']
                desc = data['results'][0]['package']['description']
                return 'message', {'text': messages(desc, pop)}
            else:
                return 'message', {'text': 'No.'}
        else:
            return None, None


def sadness():
    sub = random.choice(['vaporwaveaesthetics',
                         'vaporwaveart',
                         'vaporwave'])

    url = 'https://imgur.com/r/{}/hot.json'.format(sub)

    r = requests.get(url)
    if r.ok:
        data = r.json()
        img = random.choice(data['data'])
        text = img['title']
        url = 'https://imgur.com/{}{}'.format(img['hash'], img['ext'])
        return 'photo', {'photo': url, 'caption': text}
    else:
        return None, None


def remember(string):
    """ Splits on spaces and takes first
        word as `keyword` rest as `body`.
        If body is not empty store that in memory,
        else return it.
    """
    if not string:
        return None, None

    with shelve.open('db', 'c') as db:
        keyword, *body = string.split()
        if body:
            db[keyword] = ' '.join(body)
            txt = 'I\'ll remember that'
        else:
            result = db.get(keyword, None)
            if result:
                txt = '{} = {}'.format(keyword, result)
            else:
                txt = 'No idea about {}'.format(keyword)
    return 'message', {'text': txt}

def puppy():
    sub = 'doggos' if random.random() > 0.1 else 'boats'
    url = 'https://imgur.com/r/{}/hot.json'.format(sub)
    r = requests.get(url)
    if r.ok:
        data = r.json()
        img = random.choice(data['data'])
        text = img['title']
        url = 'https://imgur.com/{}{}'.format(img['hash'], img['ext'])
        return 'photo', {'photo': url, 'caption': text}
    else:
        return None, None

def urban(string):
    url = 'https://mashape-community-urban-dictionary.p.mashape.com/define?term={}.'.format(string)
    r = requests.get(url, headers={'X-Mashape-Key':'GNy1l9QrcUmshewiEylj8w3VdCpVp1tbthojsnpeTXm87VYeaY'})
    if r.ok:
        data = r.json()
        if data['result_type'] == 'exact':
            info = random.choice(data['list'])
            definition = "*Definition:* " + info['definition']
            example = "*Example:* " + info['example']
            return 'message-markdown', {'text': definition + "\n" + example}
        else:
            return 'message', {'text': 'Nope'}
    else:
        return None, None

def vape(text):
    def trans(c):
        i = ord(c)
        if ord('!') <= i <= ord('}'):
            return chr(0xFF01 + i - ord('!'))
        else:
            return c
    if text:
        return 'message', {'text': ''.join(trans(c) for c in text)}
    else:
        return 'message', {'text': 'ｎｅｖｅｒｍｉｎｄ'}
