import requests
import json
import re
from datetime import datetime
import time
from rapidfuzz import fuzz

class Alfa:
    pattern_id_1 = r'id=[+-]?\d+&'
    pattern_id_2 = r'[+-]?\d+'

    pattern_main_cat = r'^\d+%\xa0'


    offers = dict()

    def __init__(self, username, password):
        self.session = requests.session()
        self.username = username
        self.password = password
        pass
        

    def connect(self):
        self.session = requests.session()

        headers = {
            'Referer': 'https://private.auth.alfabank.ru/passport/cerberus-mini-blue/dashboard-blue/username?response_type=code&client_id=newclick-web&scope=openid%20newclick-web&acr_values=username&non_authorized_user=true',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }

        json_data = {
            'username': self.username,
            'password': self.password,
            # 'username': 'anton15456',
            # 'password': 'Fynjy15456!',
            'queryRedirectParams': {
                'response_type': 'code',
                'client_id': 'newclick-web',
                'scope': 'openid newclick-web',
                'acr_values': 'username',
                'non_authorized_user': 'true',
            },
            'currentRoute': '/username',
        }

        response = self.session.post(
            'https://private.auth.alfabank.ru/passport/cerberus-mini-green/dashboard-green/api/oid/authorize',
            headers=headers,
            json=json_data,
        )

        t = json.loads(response.text)
        self.mfa_token = t['params']['mfa_token']
        self.username = t['params']['username']
                
        headers = {
            'Referer': 'https://private.auth.alfabank.ru/passport/cerberus-mini-green/dashboard-green/sms?response_type=code&client_id=newclick-web&scope=openid%20newclick-web&acr_values=username&non_authorized_user=true',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }

        json_data = {
            'queryRedirectParams': {
                'response_type': 'code',
                'client_id': 'newclick-web',
                'scope': 'openid newclick-web',
                'acr_values': 'username',
                'non_authorized_user': 'true',
            },
            'previousMultiFactorResponseParams': {
                'redirect_uri': 'https://web.alfabank.ru/openid/authorize/newclick-web',
                'mfa_token': self.mfa_token,
                'acr_values': 'username:sms',
                'client_id': 'newclick-web',
                'scope': 'openid newclick-web',
                'role': 'client',
                'username': self.username,
            },
            'is_push': True,
            'type': 'CARD',
        }

        response = self.session.post(
            'https://private.auth.alfabank.ru/passport/cerberus-mini-green/dashboard-green/api/oid/reference',
            headers=headers,
            json=json_data,
        )

        t = json.loads(response.text)
        self.reference = t['reference']['reference']
        self.masked_phone = t['reference']['masked_phone']

        # print(mfa_token, username, reference, masked_phone)
    def code(self, code):
        headers = {
            'Referer': f'https://private.auth.alfabank.ru/passport/cerberus-mini-blue/dashboard-blue/sms?redirect_uri=https%3A%2F%2Fweb.alfabank.ru%2Fopenid%2Fauthorize%2Fnewclick-web&mfa_token={self.mfa_token}&acr_values=username:sms&client_id=newclick-web&scope=openid&non_authorized_user=true',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }

        json_data = {
            'credentials': {
                'queryRedirectParams': {
                    'redirect_uri': 'https://web.alfabank.ru/openid/authorize/newclick-web',
                    'mfa_token': self.mfa_token,
                    'acr_values': 'username:sms',
                    'client_id': 'newclick-web',
                    'scope': 'openid',
                    'non_authorized_user': 'true',
                },
                'previousMultiFactorResponseParams': {
                    'reference': self.reference,
                    'masked_phone': self.masked_phone,
                },
                'is_push': False,
                'type': 'CARD',
                # 'fingerprint': {
                #     'canvas_fingerprint_v1': '5f8227ebc98fdfa4c18e7f3272d2dae922d67637',
                #     'webgl_fingerprint_v1': 'a7dd6355b50c54074e15d924ca2da2091c42a9f1',
                # },
                'code': code,
            },
        }

        response = self.session.post(
            'https://private.auth.alfabank.ru/passport/cerberus-mini-green/dashboard-green/api/oid/finishCustomerRegistration',
            headers=headers,
            json=json_data,
        )

        t = json.loads(response.text)
        self.code_shifr = t['params']['code']
        self.expires_in = t['params']['expires_in']

        response = self.session.get(
            f'https://web.alfabank.ru/openid/authorize/newclick-web?redirect_uri=https%3A%2F%2Fweb.alfabank.ru%2Fopenid%2Fauthorize%2Fnewclick-web&mfa_token={self.mfa_token}&acr_values=username%3Asms&client_id=newclick-web&scope=openid+newclick-web&role=client&username={self.username}&reference={self.reference}&masked_phone={self.masked_phone}&code={self.code_shifr}&expires_in={self.expires_in}&auth_type=CARD',
        )
        return True


    def response_offers(self):
        self.offers = dict()

        try:
            response = self.session.get(
                'https://web.alfabank.ru/api/v1/loyalty-partners/categories?withoutSuggestions=true',
            )
            categories = response.json()

            for cat in categories['categories']:
                cat_id = re.search(self.pattern_id_1, cat['deeplink'])
                cat_id = re.search(self.pattern_id_2, cat['deeplink'][cat_id.start() : cat_id.end()])
                cat_id = cat_id.group(0)

                time.sleep(0.2)
                response = self.session.get(
                    f'https://web.alfabank.ru/api/v1/loyalty-partners/bonus-offers?category={cat_id}',
                )
                offers = response.json()['bonusOffers']
                for offer in offers:
                    self.offers[offer['title']] = offer['condition']
            

            response = self.session.get(
                f'https://web.alfabank.ru/api/v1/loyalty-promoted-cashback/summary/categorical-cashback?offerDate={datetime.today().replace(day=1).strftime("%Y-%m-%d")}',
            )
            categories = response.json()
            categories['categoriesSection']['categories']
            for _, offer in enumerate(categories['categoriesSection']['categories']):
                title = offer['title']
                srch = re.search(self.pattern_main_cat, title)
                self.offers[title[srch.end():]] = srch.group(0).replace('\xa0', '')

            response = self.session.get(
                f'https://web.alfabank.ru/api/v1/loyalty-promoted-cashback/wheel-of-fortune/winner?offerDate={datetime.today().replace(day=1).strftime("%Y-%m-%d")}',
            )
            categories = response.json()
            categories = categories['winnerOffer']
            self.offers[categories['partner']] = categories['discount']
        except:
            raise('Failed parsing alfa categories')
        
        

    def get_offers(self):
        print(self.offers)
        return self.offers
    
    def get_near_offers(self, find_str):
        Max = 0
        Key = ''
        for key, _ in self.offers.items():
            val = fuzz.ratio(find_str.lower(), key.lower())
            if val > Max:
                Max = val
                Key = key

        return Key, self.offers[Key]

    def is_connect(self):
        response = self.session.get(
                f'https://web.alfabank.ru/api/v1/loyalty-promoted-cashback/wheel-of-fortune/winner?offerDate={datetime.today().replace(day=1).strftime("%Y-%m-%d")}',
            )
        return not ('пользователь не авторизован' in response.text)