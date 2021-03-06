# coding=utf-8

# GOAT Summer Entry Bot by @edzart/@573supreme
from random import randrange

import requests
from time import sleep, time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Goat:
    def __init__(self):
        self.start = time()
        self.s = requests.Session()
        self.s.verify = False
        self.headers = {
            'Host': 'www.goat.com',
            'Accept-Encoding': 'gzip,deflate',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Accept-Language': 'en-US;q=1',
            'User-Agent': 'GOAT/1.13.1 (iPhone; iOS 10.3.3; Scale/2.00)',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        proxy = raw_input('Enter proxy (Press enter for none) > ')
        if proxy not in {'', None, ' '}:
            print 'Updating proxy {}'.format(proxy)
            self.s.proxies.update({
                'http': 'http://{}'.format(proxy),
                'https': 'https://{}'.format(proxy)
            })
        self.auth_token = ''
        self.products = []
        self.skip = 0
        print '='*50
        print '\n #GOATSUMMER ENTRY JIG \n BY @EDZART/@573SUPREME \n http://github.com/alxgmpr/goatsummer \n'
        print '='*50

    def login(self):
        username = raw_input('Enter email > ')
        password = raw_input('Enter password > ')
        skip = raw_input('Enter skip (if you ran this before and got an error, use this to skip to the index you died on)\n'
                         'Press enter to continue otherwise > ')
        if skip not in {'0', None, ''}:
            self.skip = int(skip)
        url = 'https://www.goat.com/api/v1/users/sign_in'
        data = {
            'user[login]': username,
            'user[password]': password
        }
        try:
            print 'logging in w/ {}:{}'.format(username, password)
            r = self.s.post(
                url,
                data=data,
                headers=self.headers,
                timeout=5
            )
            if r.status_code == 200:
                print 'getting user token'
                try:
                    r = r.json()
                    self.auth_token = r['authToken']
                    print 'using auth token {}'.format(self.auth_token)
                    self.headers['Authorization'] = 'Token token="{}"'.format(self.auth_token)
                except KeyError:
                    print 'couldnt find auth token'
                    return False
            else:
                print 'got bad status code {} from login'.format(r.status_code)
                print '\n{}\n'.format(r.text)
                return False
        except requests.exceptions.Timeout:
            print 'timeout from login request'
            return False

        print 'getting /me'
        r = self.s.get(
            'https://www.goat.com/api/v1/users/me',
            headers=self.headers
        )
        r.raise_for_status()
        print 'getting /allstrings'
        r = self.s.get(
            'https://www.goat.com/api/v1/allstrings',
            headers=self.headers
        )
        r.raise_for_status()
        return True

    def get_products(self, page):
        url = 'https://www.goat.com/api/v1/contests/3?page={}'.format(page)
        try:
            print 'scraping up product template ids (page {})'.format(page)
            r = self.s.get(
                url,
                headers=self.headers,
                timeout=5
            )
            if r.status_code == 200:
                try:
                    r = r.json()
                    for prod in r['productTemplates']:
                        self.products.append(prod['id'])
                        print '{} \t|| {}'.format(prod['id'], prod['name'].encode('utf-8'))
                    print 'scraped {} ids'.format(len(self.products))
                    return True
                except KeyError:
                    print 'couldnt find product ids'
                    return False
            else:
                print 'got bad status code {} from pid scrape'.format(r.status_code)
                exit(-1)
        except requests.exceptions.Timeout:
            print 'timeout from product scrape'
            return False

    def share_product(self, pid, network):
        url = 'https://www.goat.com/api/v1/contests/3/shared'
        data = {
            'productTemplateId': pid,
            'socialMediaType': network
        }
        try:
            print 'submitting share for prod {}'.format(pid)
            r = self.s.post(
                url,
                headers=self.headers,
                data=data,
                timeout=5
            )
            if r.status_code == 200:
                print 'successfully submitted {}'.format(pid)
                return True
            else:
                print 'got bad status code {} from share'.format(r.status_code)
                return False
        except requests.exceptions.Timeout:
            print 'timeout from product share {}'.format(pid)
            return False
g = Goat()
if g.login():
    print '='*50
    for i in range(1, 16):
        g.get_products(i)
        print '='*50
        print g.products
        print '='*50
    # for p in g.products:
    #     print '\'{}\','.format(p)
    # exit(0)
    for i in range(0, len(g.products)):
        if i >= g.skip:
            if not g.share_product(g.products[i], 'twitter'):
                print 'DIED ON INDEX: {}'.format(i)
                exit(-1)
            else:
                sleep(randrange(3, 5))
                if not g.share_product(g.products[i], 'facebook'):
                    print 'DIED ON INDEX: {}'.format(i)
                    exit(-1)
                else:
                    sleep(randrange(3, 5))
                    if not g.share_product(g.products[i], 'instagram'):
                        print 'DIED ON INDEX: {}'.format(i)
                        exit(-1)
                    else:
                        sleep(randrange(3, 5))
print '='*50
print 'time to run: {} sec'.format(abs(g.start-time()))