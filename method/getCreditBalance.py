import re
import pandas as pd
import csv

# javaをinstallすれば、tabula(PDF読み込み)が利用できる。
import tabula

import urllib.request as req
import urllib

# セキュリティ的にだめ！！（一時凌ぎ）
# https://qiita.com/shutokawabata0723/items/9733a7e640a175c23f39
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

pdfCreditBalanceFile = 'file/creditBalance.pdf'

# 対象のURLより、信用残高一覧ファイルのURLを取得する。
URL = 'https://www.jpx.co.jp/markets/statistics-equities/margin/05.html'


# DATEAGOは1-5
def getCreditBalance(DATEAGO=1):

    response = urllib.request.urlopen(URL).read().decode("utf-8")
    string_html = re.findall('<a href=\".+?\.pdf\"', response)
    url_list = []
    for i in string_html:
        j = i.lstrip('<a href=\"')
        k = j.rstrip('\"')
        url_list.append('https://www.jpx.co.jp'+k)

    url_list.sort()
    url = url_list[-DATEAGO]
    # -1の要素が直近版である！

    # ファイル名に日付を付与する。
    csvCreditBalanceFile = 'file/creditBalance_'+url[-14:-6]+'.csv'

    urllib.request.urlretrieve(url, pdfCreditBalanceFile)

    # pages='all'で全てのpageを読み込む。'1'は1ページ目の表を取得する。
    dfs_list = tabula.read_pdf(pdfCreditBalanceFile, lattice=True, pages='all')

    with open(csvCreditBalanceFile, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')

        # ◯ページ目がPDFデータがlist構造で格納されている。
        for index_dfs_list, dfs in enumerate(dfs_list):

            for index_df, df in dfs.iterrows():

                list = []

                try:

                    stockCode = df[0][-5:-1]
                    if str.isnumeric(stockCode):
                        list.append(stockCode)

                        buyBalance = int(re.sub(',', '', df[2]))
                        list.append(buyBalance)
                        sellBalance = int(re.sub(',', '', df[4]))
                        list.append(sellBalance)

                        writer.writerow(list)

                except:
                    continue

    df = pd.read_csv(csvCreditBalanceFile, header=None, names=[
        'Code', 'sellBalance', 'buyBalance'])
    df = df.set_index('Code')
    df = df.sort_index()

    # 重複indexの最初のkeepする
    df = df[~df.index.duplicated(keep='first')]

    date = url[-14:-6]
    date = date[0:4] + '-' + date[4:6] + '-' + date[6:]

    return df, date


if __name__ == '__main__':

    import firebase_admin
    from firebase_admin import credentials
    from firebase_admin import firestore

    # Use a service account.
    cred = credentials.Certificate(
        '/Users/satoki252595/work/20230527_kabu_python/kabu-blog-18f635ac9b82.json')

    app = firebase_admin.initialize_app(cred)

    db = firestore.client()

    df, date = getCreditBalance(DATEAGO=5)

    for i, code in enumerate(df.index):

        creditBalance = df.loc[code]

        doc_ref = db.collection(str(code)).document(date)
        doc_ref.set({
            u'sellBalance': int(creditBalance['sellBalance']),
            u'buyBalance': int(creditBalance['buyBalance']),
        }, merge=True)
