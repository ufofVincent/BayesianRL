from itertools import islice
import collections
import numpy as np
import pandas as pd

class LimitOrderBook:
    def __init__(self):
        self.buy_orders = dict()
        self.sell_orders = dict()
        
    def read_lob_csv_file(self, lob_file, row):
        
        file = pd.read_csv(lob_file)
        
        bid_or_ask = False # ask is False, bid is True
        agent_count = 1
        
        for column in range(0, file.shape[1] // 2):
            if not bid_or_ask:
                self.add_sell(file.iloc[row][column * 2], file.iloc[row][column * 2 + 1], agent_count)
                bid_or_ask = True
                agent_count += 1
            else:
                self.add_buy(file.iloc[row][column * 2], file.iloc[row][column * 2 + 1], agent_count)
                bid_or_ask = False
                agent_count += 1
                
                
        
    def add_buy(self, price, amount, agent_id):
        if price not in list(self.buy_orders.keys()):
            self.buy_orders.update({price : [(amount, agent_id)]})
        else:
            self.buy_orders[price].append((amount, agent_id))
            
    def add_sell(self, price, amount, agent_id):
        if price not in list(self.sell_orders.keys()):
            self.sell_orders.update({price : [(amount, agent_id)]})
        else:
            self.sell_orders[price].append((amount, agent_id))
            
    def top_5_buy(self):
        def take(n, iterable):
            """Return the first n items of the iterable as a list."""
            return list(islice(iterable, n))
        return take(5, self.buy_orders)
    
    def re_order_buys(self):
        self.buy_orders = collections.OrderedDict(sorted(self.buy_orders.items(), reverse=True))
        
    def re_order_sells(self):
        self.sell_orders = collections.OrderedDict(sorted(self.sell_orders.items()))
        
    def mid_point(self):
        self.re_order_buys()
        self.re_order_sells()
        
        if len(self.sell_orders) == 0 and len(self.buy_orders) == 0:
            return 0
        elif len(self.sell_orders) == 0 and not len(self.buy_orders) == 0:
            return list(self.buy_orders.keys())[0]
        elif not len(self.sell_orders) == 0 and len(self.buy_orders) == 0:
            return list(self.sell_orders.keys())[0]
        
        return (list(self.sell_orders.keys())[0] + list(self.buy_orders.keys())[0]) / 2
   
    def top_5_sell(self):
        def take(n, iterable):
            """Return the first n items of the iterable as a list."""
            return list(islice(iterable, n))
        return take(5, self.sell_orders)
    
    def fill_buy_order(self, price, shares, agent_id):
        
        if price < 0:
            return None, None
        
        
        
        prices = np.array(sorted(list(self.sell_orders.keys())))
        rel_prices = prices[prices <= price]
        # relevant_prices = prices[:prices.index(price)]
        prices_to_remove = []
        order_shares = shares
        totalAmount = 0
        for i in range(0, len(rel_prices)):
            if shares == 0:
                break
            num_indices_to_rem = 0
            for j in range(0, len(self.sell_orders[rel_prices[i]])):
                amount, id = self.sell_orders[rel_prices[i]][j]
                if amount > shares:
                    self.sell_orders[rel_prices[i]][j] = (amount - shares, agent_id)
                    shares = 0
                    totalAmount += shares * rel_prices[i]
                else:
                    shares -= amount
                    num_indices_to_rem += 1
                    totalAmount += amount * rel_prices[i]
                    
            for k in range(0, num_indices_to_rem):
                del self.sell_orders[rel_prices[i]][0]
            if len(self.sell_orders[rel_prices[i]]) == 0:
                prices_to_remove.append(rel_prices[i])
        if shares != 0:
            self.add_buy(price, shares, agent_id)
        for price in prices_to_remove:
            del self.sell_orders[price]
            
        weighted_average = 0
        
        if not (order_shares - shares) == 0:
            weighted_average = totalAmount / (order_shares - shares)
        else:
            weighted_average = 0
            
        self.re_order_buys()
            
        return weighted_average, shares  # money that this buy costed


    def fill_sell_order(self, price, shares, agent_id):
        
        if price < 0:
            return None, None
        
        prices = np.array(sorted(list(self.buy_orders.keys()), reverse=True))
        rel_prices = prices[prices >= price]
        # relevant_prices = prices[:prices.index(price)]
        prices_to_remove = []
        order_shares = shares
        totalAmount = 0
        
        for i in range(0, len(rel_prices)):
            if shares == 0:
                break
            num_indices_to_rem = 0
            for j in range(0, len(self.buy_orders[rel_prices[i]])):
                amount, id = self.buy_orders[rel_prices[i]][j]
                if amount > shares:
                    self.buy_orders[rel_prices[i]][j] = (amount - shares, agent_id)
                    shares = 0
                    totalAmount += shares * rel_prices[i]
                    
                else:
                    totalAmount += amount * rel_prices[i]
                    shares -= amount
                    num_indices_to_rem += 1
                    
                    
            for k in range(0, num_indices_to_rem):
                del self.buy_orders[rel_prices[i]][0]
            if len(self.buy_orders[rel_prices[i]]) == 0:
                prices_to_remove.append(rel_prices[i])
        if shares != 0:
            self.add_sell(price, shares, agent_id)
        for price in prices_to_remove:
            del self.buy_orders[price]
        
        weighted_average = 0
        
        if not (order_shares - shares) == 0:
            weighted_average = totalAmount / (order_shares - shares)
        else:
            weighted_average = 0
            
        self.re_order_buys()
        
        return weighted_average, shares # money made in selling


lob = LimitOrderBook()
lob.read_lob_csv_file("AAPL_2024-03-01_34200000_57600000_orderbook_10.csv", 0)

print(list(lob.buy_orders))
print(list(lob.sell_orders))









        
        





