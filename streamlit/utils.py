def get_symbol(cList, coin):
    filtered = [record for record in cList if record['name'] == coin]
    return filtered[0]['symbol']


def flatten(xss):
    return [x for xs in xss for x in xs]
