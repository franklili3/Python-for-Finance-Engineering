import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import OrderedDict

# Simple order book

buy_orders = {} # key is price, value is size
sell_orders = {}
trades = []

def dummy_book():
    buy_orders.clear()
    sell_orders.clear()
    # add some buys and sells
    buy_orders[99.50] = 1000
    buy_orders[99.00] = 900
    sell_orders[100.02] = 2500
    sell_orders[100.50] = 1900
    sell_orders[101.01] = 200

def show_book():
    buy_qty = []
    buy_price = []
    sell_price = []
    sell_qty = []
    for key in sorted( buy_orders, reverse = True ):
        buy_price.append(key)
        buy_qty.append(int(buy_orders[key]))
    for key in sorted(sell_orders):
        sell_price.append(key)
        sell_qty.append(sell_orders[key])
    
    d = OrderedDict(BUY_QTY = buy_qty, BUY_PX = buy_price, SELL_PX = sell_price, SELL_QTY = sell_qty)
    display_book = pd.DataFrame(OrderedDict([(k, pd.Series(v)) for k, v in d.items()]))
    display(display_book)
      
# return best bid and offer
def get_BBO():
    return (max(buy_orders.items()), 
            min(sell_orders.items()))

# add a new order to the book 
def new_order(side, price, qty):
    # side = s | b, fail on anything else
    if not (side in ["s", "b"]):
        print("Side '" + side + "' not supported.")
        return
    # price: float
    # qty: integer
    remaining_order_qty = qty
    
    # it's a sell order
    if (side == 's'):
        # loop thru buy orders
        for key in sorted(buy_orders, reverse = True):
            buy_price = key
            buy_qty = buy_orders[key]
            
            # check for price at this level
            if price <= buy_price: # we have at least one match
                trade_qty = min (buy_qty, remaining_order_qty)
                trade_price = buy_price
                
                # update order book
                # remove or reduce order 
                if buy_qty >= remaining_order_qty:
                    # we have exhausted our order quantity, update the resting quantity
                    if (buy_qty == remaining_order_qty):
                        # nothing left at this level, remove it
                        del buy_orders[buy_price]
                    else:
                        # update residual order book quantity
                        buy_orders[buy_price] -= remaining_order_qty
                    trades.append((trade_price, trade_qty))
                    break # we're done
                    
                else: # we have more order left, remove this price level in the book and continue
                    # remove buy order 
                    del buy_orders[key]
                    # decrement sell qty
                    remaining_order_qty -= trade_qty

                    # record trade
                    trades.append((trade_price, trade_qty))
                    continue
                    
            else: # prices didn’t match, so add it to the sell side
                if price in sell_orders:
                    sell_orders[price] += remaining_order_qty
                else:
                    sell_orders[price] = remaining_order_qty
                break 

    # it's a buy  
    else:
        # loop thru sell orders
        for key in sorted(sell_orders):
            sell_price = key
            sell_qty = sell_orders[key]
            # check for price at this level
            if price >= sell_price: # we have at least one match
                trade_qty = min (sell_qty, remaining_order_qty)
                trade_price = sell_price
                
                # update order book
                # remove or reduce order 
                if sell_qty >= remaining_order_qty:
                    # we have exhausted our order quantity, update the resting quantity
                    if (sell_qty == remaining_order_qty):
                        # nothing left at this level, remove it
                        del sell_orders[sell_price]
                    else:
                        # update residual order book quantity
                        sell_orders[sell_price] -= remaining_order_qty
                    trades.append((trade_price, trade_qty))
                    break # we're done
                    
                else: # we have more order left, remove this price level in the book and continue
                    # remove buy order 
                    del sell_orders[key]
                    # decrement sell qty
                    remaining_order_qty -= trade_qty

                    # record trade
                    trades.append((trade_price, trade_qty))
                    continue
                    
            else: # prices didn’t match, so add it to the sell side
                if price in buy_orders:
                    buy_orders[price] += remaining_order_qty
                else:
                    buy_orders[price] = remaining_order_qty
                break 
    
