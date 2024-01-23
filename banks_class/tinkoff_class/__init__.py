import requests
from rapidfuzz import fuzz

class Tinkoff:

    offers = dict()

    def __init__(self, number):
        self.session = requests.session()
        self.sessionId = ''
        self.number = number
        pass
        

    def connect(self):
        
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }

        self.session.headers.update(headers)

        response = self.session.get('https://www.tinkoff.ru/auth/login/', headers=headers)


        params = {
            'prompt': 'none',
            'origin': 'web,ib5,platform',
        }

        response = self.session.get('https://www.tinkoff.ru/api/common/v1/session/authorize', params=params, allow_redirects=False)
        response = self.session.get(response.headers['Location'], allow_redirects=False)
        response = self.session.get(response.headers['Location'], allow_redirects=False)


        params = {
            'theme': 'default',
            'display': 'page',
            'origin': 'web,ib5,platform',
            'complete_uri': 'https://www.tinkoff.ru/auth/',
            'warmup': '{"origin":"web,ib5,platform"}',
        }

        response = self.session.get('https://www.tinkoff.ru/api/common/v1/session/authorize/', params=params, allow_redirects=False)
        response = self.session.get(response.headers['Location'], allow_redirects=False)
        self.cid = response.headers['Location']
        response = self.session.get('https://id.tinkoff.ru/auth/' + self.cid, allow_redirects=False)

        headers = {
            'authority': 'id.tinkoff.ru',
            'accept': 'application/form-variables+json',
            'origin': 'https://id.tinkoff.ru',
            'referer': 'https://id.tinkoff.ru/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
        data = {
            'phone': self.number,
            # 'phone': '+79104280726',
            'step': 'phone',
        }

        response = self.session.post('https://id.tinkoff.ru/auth/' + self.cid, data=data, headers=headers)
        self.token = response.json()['token']

    def code(self, code):
        
        headers = {
            'authority': 'id.tinkoff.ru',
            'accept': 'application/form-variables+json',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://id.tinkoff.ru',
            'referer': 'https://id.tinkoff.ru/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }


        data = {
            'otp': code,
            'consent': '',
            'step': 'otp',
            'token': self.token,
        }

        response = self.session.post('https://id.tinkoff.ru/auth/' + self.cid, headers=headers, data=data)


        headers = {
            'authority': 'id.tinkoff.ru',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'referer': 'https://id.tinkoff.ru/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }


        response = self.session.get('https://id.tinkoff.ru/auth/' + self.cid, headers=headers)


        headers = {
            'authority': 'id.tinkoff.ru',
            'accept': 'application/form-variables+json',
            'origin': 'https://id.tinkoff.ru',
            'referer': 'https://id.tinkoff.ru/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }

        data = {
            'step': 'fingerprint',
        }

        response = self.session.post('https://id.tinkoff.ru/auth/' + self.cid, headers=headers, data=data)

        data = {
            'step': 'complete',
        }

        response = self.session.post('https://id.tinkoff.ru/auth/' + self.cid, headers=headers, data=data)



        data = {
            'step': 'set-pin',
            'skipped': 'true',
        }

        response = self.session.post('https://id.tinkoff.ru/auth/' + self.cid, headers=headers, data=data)


        headers = {
            'authority': 'www.tinkoff.ru',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'referer': 'https://id.tinkoff.ru/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
        redirect_to = response.json()['redirectTo']
        par = redirect_to[redirect_to.find('?')+1:]
        response = self.session.get(response.json()['redirectTo'], headers=headers)
        response = self.session.get(f'https://www.tinkoff.ru/api/common/v1/session/check_auth?notInFrame=true&{par}')


        self.sessionId = response.json()['sessionId']
        return True


    def response_offers(self):
        self.offers = dict()

        try:

            headers = {
                'authority': 'ms-gateway.tinkoff.ru',
                'content-type': 'application/json',
                'origin': 'https://www.tinkoff.ru',
                'referer': 'https://www.tinkoff.ru/',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            }

            params = {
                'origin': 'web,ib5,platform',
                'sessionId': self.sessionId,
            }

            response = self.session.get(
                'https://ms-gateway.tinkoff.ru/loyalty_api/api/internetBank/clientOffers',
                params=params,
                headers=headers,
            )
            for offer in response.json()['payload']:
                self.offers[offer['merchant']['merchantName']] = f"{offer['cashbackInfo']['cashbackPercent']}%"

            params = {
                'origin': 'web,ib5,platform',
                'appName': 'supreme',
                'appVersion': '0.0.1',
                'sessionid': self.sessionId,
            }
            response = self.session.get(
                'https://www.tinkoff.ru/api/common/v1/client_offer_essences',
                params=params,
            )
            for offer in response.json()['payload'][0]['essences']:
                self.offers[offer['name']] = f"{offer['percent']}%"
        except:
            raise('Failed parsing tinkoff categories')
        
        

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

        headers = {
            'authority': 'ms-gateway.tinkoff.ru',
            'content-type': 'application/json',
            'origin': 'https://www.tinkoff.ru',
            'referer': 'https://www.tinkoff.ru/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }

        params = {
            'origin': 'web,ib5,platform',
            'sessionId': self.sessionId,
        }

        response = self.session.get(
            'https://ms-gateway.tinkoff.ru/loyalty_api/api/internetBank/clientOffers',
            params=params,
            headers=headers,
        )
        return not ('Нет доступа' in response.text)
    
