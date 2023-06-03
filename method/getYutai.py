import requests
from bs4 import BeautifulSoup
import re
import time

import ssl
ssl._create_default_https_context = ssl._create_unverified_context


URL1 = 'https://www.kabuyutai.com/yutai/'
URL2 = '_sp'
URL3 = '.html'

monthList = ['january', 'february', 'march', 'april', 'may', 'june',
             'july', 'august', 'september', 'october', 'november', 'december']
# monthList = ['august',]
numList = [str(i) for i in range(2, 100, 1)]
numList.insert(0, '')


def conMonth(month):

    if month == 'january':
        return '1月'
    if month == 'february':
        return '2月'
    if month == 'march':
        return '3月'
    if month == 'april':
        return '4月'
    if month == 'may':
        return '5月'
    if month == 'june':
        return '6月'
    if month == 'july':
        return '7月'
    if month == 'august':
        return '8月'
    if month == 'september':
        return '9月'
    if month == 'october':
        return '10月'
    if month == 'november':
        return '11月'
    if month == 'december':
        return '12月'


def getYuutaiCodeInformation(month):

    parent_dict = {}

    for num in numList:

        url = URL1 + str(month) + URL2 + str(num) + URL3

        # HTMl取得
        time.sleep(0.5)
        response = requests.get(url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        if 'ページが見つかりませんでした' in soup.text:
            break

        tr_s = soup.find_all(class_="table_tr_info")

        for tr in tr_s:

            children_dict = {}
            p = tr.find_all('p')
            code = p[0].text[-5:-1]
            p_name = p[0].text[:-6]
            p_yuutai = p[1].text
            p_tyouki = p[2].text[6:]
            p_yuutaiGetMoney = p[4].text[8:][:-1]
            p_yuutaiYeild = p[5].text[7:][:-1]
            # 何故かうまくできない時がある。8929の青山財産で"
            try:
                p_dividentYeild = p[6].text[7:][:-1]
            except:
                p_dividentYeild = '?'

            children_dict['企業名'] = p_name
            children_dict['優待内容'] = p_yuutai[6:]
            children_dict['長期保有有無'] = p_tyouki
            children_dict['最低投資金額'] = p_yuutaiGetMoney
            children_dict['優待利回り'] = p_yuutaiYeild
            children_dict['配当利回り'] = p_dividentYeild
            children_dict['権利月'] = conMonth(month)

            parent_dict[code] = children_dict

    return parent_dict


if __name__ == '__main__':

    d = {}

    for month in monthList:
        s = getYuutaiCodeInformation(month)
        d |= s
