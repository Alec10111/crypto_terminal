def maxProfit(prices):
    buy = 0
    sell = 1
    max_profit = 0
    for i in range(1, len(prices)):

        # Checking for lower buy value
        if prices[buy]['high'] > prices[i]['high']:
            buy = i

        # Checking for higher profit
        elif prices[i]['high'] - prices[buy]['high'] > max_profit:
            sell = i
            max_profit = prices[i]['high'] - prices[buy]['high']
    return prices[buy], prices[sell]
