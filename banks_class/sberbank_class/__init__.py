import requests

class Sberbank:

    offers = dict()

    def __init__(self):
        self.session = requests.session()
        pass
        

    def connect(self):
        
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Referer': 'https://web3-new.online.sberbank.ru/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }

        response = self.session.get('https://online.sberbank.ru/CSAFront/index.do', headers=headers)




        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://online.sberbank.ru',
            'Referer': 'https://online.sberbank.ru/CSAFront/index.do',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }

        data = {
            # 'deviceprint': 'version=1.7.3&pm_br=Chrome&pm_brmjv=120&iframed=0&intip=&pm_expt=&pm_fpacn=Mozilla&pm_fpan=Netscape&pm_fpasw=internal-pdf-viewer|internal-pdf-viewer|internal-pdf-viewer|internal-pdf-viewer|internal-pdf-viewer&pm_fpco=1&pm_fpjv=0&pm_fpln=lang=ru-RU|syslang=|userlang=&pm_fpol=true&pm_fposp=&pm_fpsaw=1920&pm_fpsbd=&pm_fpsc=24|1920|1080|1032&pm_fpsdx=&pm_fpsdy=&pm_fpslx=&pm_fpsly=&pm_fpspd=24&pm_fpsui=&pm_fpsw=&pm_fptz=3&pm_fpua=mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/120.0.0.0 safari/537.36|5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36|Win32&pm_fpup=&pm_inpt=&pm_os=Windows&adsblock=0=true|1=true|2=false|3=false|4=false&audio=baseLatency=0.01|outputLatency=0|sampleRate=48000|state=suspended|maxChannelCount=2|numberOfInputs=1|numberOfOutputs=1|channelCount=2|channelCountMode=max|channelInterpretation=speakers|fftSize=2048|frequencyBinCount=1024|minDecibels=-100|maxDecibels=-30|smoothingTimeConstant=0.8&pm_fpsfse=true&webgl=ver=webgl2|vendor=Google Inc. (Intel)|render=ANGLE (Intel, Intel(R) UHD Graphics 630 (0x00003E9B) Direct3D11 vs_5_0 ps_5_0, D3D11)',
            'jsEvents': '',
            'domElements': '',
            'operation': 'button.begin',
            'login': 'anton15456',
            'pageInputType': 'INDEX',
            'password': 'Fynjy15456!',
            'loginInputType': 'BY_LOGIN',
            'storeLogin': 'true',
            'publicKeyCredentialAvailable': 'false',
        }

        response = self.session.post('https://online.sberbank.ru/CSAFront/authMainJson.do', headers=headers, data=data)
        self.token = response.json()['token']



    def code(self, code):
        
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://online.sberbank.ru',
            'Referer': 'https://online.sberbank.ru/CSAFront/index.do',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }

        data = {
            # 'deviceprint': 'version=1.7.3&pm_br=Chrome&pm_brmjv=120&iframed=0&intip=&pm_expt=&pm_fpacn=Mozilla&pm_fpan=Netscape&pm_fpasw=internal-pdf-viewer|internal-pdf-viewer|internal-pdf-viewer|internal-pdf-viewer|internal-pdf-viewer&pm_fpco=1&pm_fpjv=0&pm_fpln=lang=ru-RU|syslang=|userlang=&pm_fpol=true&pm_fposp=&pm_fpsaw=1920&pm_fpsbd=&pm_fpsc=24|1920|1080|1032&pm_fpsdx=&pm_fpsdy=&pm_fpslx=&pm_fpsly=&pm_fpspd=24&pm_fpsui=&pm_fpsw=&pm_fptz=3&pm_fpua=mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/120.0.0.0 safari/537.36|5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36|Win32&pm_fpup=&pm_inpt=&pm_os=Windows&adsblock=0=true|1=true|2=false|3=false|4=false&audio=baseLatency=0.01|outputLatency=0|sampleRate=48000|state=suspended|maxChannelCount=2|numberOfInputs=1|numberOfOutputs=1|channelCount=2|channelCountMode=max|channelInterpretation=speakers|fftSize=2048|frequencyBinCount=1024|minDecibels=-100|maxDecibels=-30|smoothingTimeConstant=0.8&pm_fpsfse=true&webgl=ver=webgl2|vendor=Google Inc. (Intel)|render=ANGLE (Intel, Intel(R) UHD Graphics 630 (0x00003E9B) Direct3D11 vs_5_0 ps_5_0, D3D11)',
            'jsEvents': '',
            'domElements': '',
            'org.apache.struts.taglib.html.TOKEN': self.token,
            'operation': 'button.next',
            'confirmPassword': code,
            'pageInputType': 'INDEX',
            'token': self.token,
        }

        response = self.session.post('https://online.sberbank.ru/CSAFront/authMainJson.do', headers=headers, data=data)


        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            # 'Cookie': '_sa=SA1.12d26d8e-0365-445a-8db6-40f2bcd4c411.1704470973; sb-sid=3a4d6ae7-9c9b-4d48-b2aa-31882d39753a; sb-id=gYHOLuOiqLxFhLOaZO7JTH1xAAABjNpjCdPA7mE5zCEpOktID7YZp8y1tMWRCRb8p_EVp6lxKYeR6TNhNGQ2YWU3LTljOWItNGQ0OC1iMmFhLTMxODgyZDM5NzUzYQ; sb-pid=gYHzmLcBCvNH3KX_EGm2r1zVAAABifMnjYFMxiO9OoFZN3WM7GhtyROxxXjnTOd2eCOParWxiqGaUQ; sbrf.pers_sign=1; g_uid=4/n6GBJLpyX/g1oUC9QCeX6eDLo12RQRCQnPaiSzikhC7r//UxaVY4orPcoeCQtRsVEVVONVIXix0EOZPOJuPA/FDnz2yIR8nqFv4w==; TS019a42f2=0156c5c860df866a4e45088b233b35c29259003bf3c0f9dbedee77f74c04c848c7104d45702bb1fa8aa600b2e0937f3957ba3946a3a082c7aa158465d15ded2c88acb7088c19bfa80e25df2d97c7650c77d451134634d64ba5771e475754a749802f3201248a989950b624d7f0f91214926998cc8cb6fd850f8786ee9f35f34d5c1aaf44994873af5ef7fd66f72a1f487baf27ea45',
            'Pragma': 'no-cache',
            'Referer': 'https://online.sberbank.ru/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }


        response = self.session.get(response.json()['redirect'], headers=headers, allow_redirects=False)
        response = self.session.get(response.headers['Location'], headers=headers, allow_redirects=False)
        response = self.session.get(response.headers['Location'], headers=headers, allow_redirects=False)
        return True


    # def response_offers(self):
    #     self.offers = dict()

    #     try:

    #         headers = {
    #             'authority': 'ms-gateway.tinkoff.ru',
    #             'content-type': 'application/json',
    #             'origin': 'https://www.tinkoff.ru',
    #             'referer': 'https://www.tinkoff.ru/',
    #             'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    #         }

    #         params = {
    #             'origin': 'web,ib5,platform',
    #             'sessionId': self.sessionId,
    #         }

    #         response = self.session.get(
    #             'https://ms-gateway.tinkoff.ru/loyalty_api/api/internetBank/clientOffers',
    #             params=params,
    #             headers=headers,
    #         )
    #         for offer in response.json()['payload']:
    #             self.offers[offer['merchant']['merchantName']] = f"{offer['cashbackInfo']['cashbackPercent']}%"

    #         params = {
    #             'origin': 'web,ib5,platform',
    #             'appName': 'supreme',
    #             'appVersion': '0.0.1',
    #             'sessionid': 'mhQejhokuTKXC8neMqztddcTcKHQ2bxC.ds-prod-api-102',
    #         }
    #         response = self.session.get(
    #             'https://www.tinkoff.ru/api/common/v1/client_offer_essences',
    #             params=params,
    #         )
    #         for offer in response.json()['payload'][0]['essences']:
    #             self.offers[offer['name']] = f"{offer['percent']}%"
    #     except:
    #         raise('Failed parsing tinkoff categories')
        
        

    # def get_offers(self):
    #     print(self.offers)
    #     return self.offers
    
    # def get_near_offers(self, find_str):
    #     Max = 0
    #     Key = ''
    #     for key, _ in self.offers.items():
    #         val = fuzz.ratio(find_str.lower(), key.lower())
    #         if val > Max:
    #             Max = val
    #             Key = key

    #     return Key, self.offers[Key]

    def is_connect(self):

        from datetime import datetime, timedelta

        From = datetime.now().strftime('%d.%m.%Y')
        To = (datetime.now() - timedelta(days=365.24)).strftime('%d.%m.%Y')

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json;charset=UTF-8',
            'Origin': 'https://web3-new.online.sberbank.ru',
            'Referer': 'https://web3-new.online.sberbank.ru/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }

        json_data = {
            'paginationOffset': 0,
            'paginationSize': 11,
            'from': f'{To}T00:00:00',
            'to': f'{From}T23:59:59',
        }

        response = self.session.post(
            'https://web-node3.online.sberbank.ru/uoh-bh/v1/operations/list',
            headers=headers,
            json=json_data,
        )

        return not ('errorText_variable' in response.text)
    

    def get_balance(self):

        from datetime import datetime, timedelta

        From = datetime.now().strftime('%d.%m.%Y')
        To = (datetime.now() - timedelta(days=365.24)).strftime('%d.%m.%Y')

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json;charset=UTF-8',
            'Origin': 'https://web3-new.online.sberbank.ru',
            'Referer': 'https://web3-new.online.sberbank.ru/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }

        json_data = {
            'paginationOffset': 0,
            'paginationSize': 11,
            'from': f'{To}T00:00:00',
            'to': f'{From}T23:59:59',
        }

        response = self.session.post(
            'https://web-node3.online.sberbank.ru/uoh-bh/v1/operations/list',
            headers=headers,
            json=json_data,
        )

        print(response.text)
    

if __name__ == '__main__':
    sberbank = Sberbank()
    print(sberbank.is_connect())
    sberbank.connect()
    sberbank.code(input('code'))
    print(sberbank.is_connect())
    sberbank.get_balance()