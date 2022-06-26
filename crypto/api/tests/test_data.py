from api.models import Coin, CoinHistory

test_coins = [
    {
        'name': 'Bitcoin',
        'symbol': 'BTC'
    },
    {
        'name': 'Cardano',
        'symbol': 'ADA'
    },
    {
        'name': 'Ethereum',
        'symbol': 'ETH'
    }
]

test_records = [
    {
        "symbol": "BTC",
        "date": "2018-11-13",
        "high": 6423.25,
        "low": 6350.17,
        "open": 6413.63,
        "close": 6411.27,
        "volume": 3939060000.0,
        "marketcap": 111373453740.24
    },
    {
        "symbol": "ADA",
        "date": "2018-11-13",
        "high": 6423.25,
        "low": 6350.17,
        "open": 6413.63,
        "close": 6411.27,
        "volume": 3939060000.0,
        "marketcap": 111373453740.24
    },
    {
        "symbol": "ETH",
        "date": "2018-11-13",
        "high": 6423.25,
        "low": 6350.17,
        "open": 6413.63,
        "close": 6411.27,
        "volume": 3939060000.0,
        "marketcap": 111373453740.24
    },
    {
        "symbol": "BTC",
        "date": "2018-11-14",
        "high": 6423.25,
        "low": 6350.17,
        "open": 6413.63,
        "close": 6411.27,
        "volume": 3939060000.0,
        "marketcap": 111373453740.24
    },
    {
        "symbol": "ADA",
        "date": "2018-11-14",
        "high": 6423.25,
        "low": 6350.17,
        "open": 6413.63,
        "close": 6411.27,
        "volume": 3939060000.0,
        "marketcap": 111373453740.24
    },
    {
        "symbol": "ETH",
        "date": "2018-11-14",
        "high": 6423.25,
        "low": 6350.17,
        "open": 6413.63,
        "close": 6411.27,
        "volume": 3939060000.0,
        "marketcap": 111373453740.24
    }
]


def base_data(cls):
    cls.coins = Coin.objects.bulk_create([Coin(**data) for data in test_coins])
    cls.records = CoinHistory.objects.bulk_create([CoinHistory(**data) for data in test_records])
