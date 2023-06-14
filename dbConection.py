import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from method.getStockInfo import getStockInfo
from method.getStocCodes import getStockCodes


# Use a service account.
cred = credentials.Certificate(
    '/Users/satoki252595/work/20230527_kabu_python/kabu-blog-18f635ac9b82.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()


def setStockPrice(code, period):

    code = str(code)

    df_stockPriceInfo = getStockInfo.getStockPriceInfo(code, period)
    for i, l in enumerate(df_stockPriceInfo.index):
        date = str(df_stockPriceInfo.index[i].date())
        priceList = df_stockPriceInfo.loc[l]

        doc_ref = db.collection(code).document(date)
        doc_ref.set({
            u'Open': priceList['Open'],
            u'High': priceList['High'],
            u'Low': priceList['Low'],
            u'Close': priceList['Close'],
            u'Volume': priceList['Volume']
        }, merge=True)


df_stockCodes = getStockCodes()
stockCodesList = [str(l) for l in df_stockCodes['コード']]

for code in stockCodesList:
    setStockPrice(code, period='1d')