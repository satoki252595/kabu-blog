# 銘柄コードや銘柄名、業種を取得する。

import urllib.request
import re
import pandas as pd

# セキュリティ的にだめ！！（一時凌ぎ）
# https://qiita.com/shutokawabata0723/items/9733a7e640a175c23f39
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def getStockCodes():

    #### wgetコマンドをpythonで実装########################################

    URL = 'https://www.jpx.co.jp/markets/statistics-equities/misc/01.html'

    response = urllib.request.urlopen(URL).read().decode("utf-8")
    string_html = re.findall('<a href=\".+?\.xls\"', response)
    url_list = []
    for i in string_html:
        j = i.lstrip('<a href=\"')
        k = j.rstrip('\"')
        url_list.append('https://www.jpx.co.jp'+k)
    url = url_list[0]

    # 国内株式のみ抽出

    df = pd.read_excel(url)
    df = df[(df.iloc[:, 3] == 'プライム（内国株式）') | (df.iloc[:, 3] ==
                                               'スタンダード（内国株式）') | (df.iloc[:, 3] == 'グロース（内国株式）')]

    # csvファイルに銘柄コード一覧を出力

    # df_code = df['コード']
    # df_code.to_csv('./stockCode.csv',index = False,header = False)

    return df
