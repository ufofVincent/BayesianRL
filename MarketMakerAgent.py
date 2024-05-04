from LimitOrderBook import LimitOrderBook

class MarketMakerAgent:
    
    def take_action(self, limit_order_book):
        
        buy_prices = limit_order_book.top_5_buy()
        
        for price in buy_prices:
            limit_order_book.add_buy(price, 1000, 0)
            
        sell_prices = limit_order_book.top_5_sell()
        
        for price in sell_prices:
            limit_order_book.add_sell(price, 1000, 0)