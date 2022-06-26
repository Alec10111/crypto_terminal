def getSymbol(cList, coin):
    filtered = list(filter(lambda x: x['name'] == coin, cList))
    dicte = filtered[0]
    return dicte['symbol']


def flatten(xss):
    return [x for xs in xss for x in xs]
