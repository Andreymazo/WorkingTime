import os

from django.core.management import BaseCommand

# from catalog.models import Student
import requests
from requests.auth import HTTPDigestAuth


# def _send_request(self, search_word, page):
    # # url = f'{self.__url}/vacancies/?page={page}&keyword={search_word}'
    # headers = {
    #     'X-Api-App-Id': self.__secret,
    #     'Content-Type': 'application / x - www - form - urlencoded'
    # }
    # response = requests.get(url=f'{self.__url}/vacancies?keyword={search_word}&page={page}', headers=headers)
    # if response.status_code == 200:
    #     print(f'Try to get page {page}')
    #     print(response.json())
    #     return response.json()
def _send_request():#(login=, password=):
    __secret = ''
    login = os.getenv('SMS_login')
    password = os.getenv('SMS_password')
    api_id = os.getenv('api_id')
    recepient = '79313155752'

    # url = 'https://lk.megafon.ru/api/'
    # url = 'https://{domain}/crmapi/v1/{endpoint} '
    ########################################## Нижние 4 рабочие урлы Megafon #######################################
    # url = f'https://sms.ru/auth/check?api_id={api_id}&json=1'
    # url = f'https://sms.ru/auth/check?login={login}&password={password}&json=1'
    url = f'https://sms.ru/sms/send?api_id={api_id}&to={recepient}&msg=hello+world&json=1'
    # url = f'https://sms.ru/sms/cost?api_id={api_id}&to[79219507391]=hello+world&to[74993221627]=hello+world&json=1'
    ##########################################################################################################
    # url = 'https://m2m.megafon.ru:3333/openapi/v1/tokens-stub/get?'
    # url = 'https://a2p-api.megalabs.ru/'
    # https: // infostart.ru / public / 676587 /?ysclid = lid0v9cma9905169632
    # https: // github.com / megafonapi / examples

    # url = 'https://lk.megafon.ru/api/lk/options/remaindersMini'
    # url = 'https://sm.megafon.ru/sm/client/routing?login=79219507391'#&password=XyXZXY

    # headers = {
    #     # 'User - Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0',
    #     # 'User - Agent': 'apps.PosutochkaConfig.name/1.0 (my-app-feedback@example.com)',
    #     # "User-Agent": "python-requests/2.28.2",
    #     'X-Api-App-Id': '__secret',
    #     'Content-Type': 'application / x - www - form - urlencoded',
    #
    # }
################################################################################
    # https: // iot - m2m.megafon.ru / assets / documents / MF_IOT_CMP_MEGAFON_GF - DOC_API - RU_v351.pdf?ysclid = lifuzeihg6569993396
##############################################################
 # Berem token:
    # https: // m2m.megafon.ru: 3333 / openapi / v1 / tokens - stub / get?


    # "User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
    pag = requests.get(url)#, headers=headers)#, headers=headers)#, auth=HTTPDigestAuth(login, password), headers=headers, timeout=5)
    # client.get(url)
    # csrftoken = client.cookies
    # print(csrftoken)
    # print(pag.status_code, pag.json(), pag.content, pag.text)
    if pag.status_code == 200:
        print(pag.json())
    print(pag.status_code, pag.content, pag.text)


class Command(BaseCommand):
    # __url = 'https://api.superjob.ru/2.0'
    # __secret = 'v3.r.137222938.adcc1bf5602cc5a2c697d63eb9c580dd5029f96f.049aae965267ebe71bbc7c587187da62cdbc560e'
    # __per_page = 20

    def handle(self, *args, **options):
        _send_request()
