import yfinance as yfin


class getStockInfo():

    def __init__(self, code, period):
        self.code = code
        self.period = period

    def getStockPriceInfo(code, period):
        '''銘柄コードを引数に指定すれば、株価の情報が取得できる。'''
        df = yfin.download(code + ".T", period=period)

        return df
