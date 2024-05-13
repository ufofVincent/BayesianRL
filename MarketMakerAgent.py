from LimitOrderBook import LimitOrderBook
from numpy import random
class MarketMakerAgent:
    def __init__(self, agent_id, lam):
        self.agent_id = 0
        self.lam = lam
        self.timer = 0
    def take_action(self, limit_order_book):
        # buy_prices = limit_order_book.top_5_buy()
        # for price in buy_prices:
        #     limit_order_book.add_buy(price, 1000, 0)
        # sell_prices = limit_order_book.top_5_sell()
        # for price in sell_prices:
        #     limit_order_book.add_sell(price, 1000, 0)
        if self.timer == 0:
            midpoint = limit_order_book.mid_point()
            buy_prices = [midpoint * 0.975, midpoint * 0.98, midpoint * 0.985, midpoint * 0.99, midpoint * 0.995]
            sell_prices = [midpoint * 1.025, midpoint * 1.02, midpoint * 1.015, midpoint * 1.01, midpoint * 1.005]
            # buy_prices = [midpoint * 0.975, midpoint * 0.98,midpoint * 0.99]
            # sell_prices = [midpoint * 1.025, midpoint * 1.02, midpoint * 1.01]
            for price in buy_prices:
                limit_order_book.fill_buy_order(price, 50000, 0)
            for price in sell_prices:
                limit_order_book.fill_sell_order(price, 50000, 0)
            self.timer = random.poisson(self.lam, 1)[0]
            return limit_order_book
        else:
            self.timer -= 1
            return None
