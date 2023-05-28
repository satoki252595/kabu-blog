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
# stockCodesList = [str(l) for l in df_stockCodes['コード']]

# 無料枠を利用するため。銘柄コードが1のものを中心に取得する。
# stockCodesList = [str(l) for l in df_stockCodes['コード']
#                   if str(l).startswith('1')]

stockCodesList = ['1871', '1873', '1878', '1879', '1882', '1884', '1885', '1887', '1888', '1890', '1893', '1897', '1898', '1899', '1904', '1905', '1909', '1911', '1914', '1921', '1925', '1926', '1928', '1929', '1930', '1934', '1938', '1939', '1941',
                  '1942', '1944', '1945', '1946', '1948', '1949', '1950', '1951', '1952', '1954', '1959', '1960', '1961', '1963', '1964', '1965', '1966', '1967', '1968', '1969', '1971', '1972', '1973', '1975', '1976', '1979', '1980', '1981', '1982', '1992', '1994', '1997']

for code in stockCodesList:
    setStockPrice(code, period='10y')
