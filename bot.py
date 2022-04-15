import alpaca_trade_api as tradeapi

# Connect to API:
#alpaca_endpoint = 'https://paper-api.alpaca.markets'

#api = tradeapi.REST('PKTKIT2O85UBGRAZEJ2X','OaOkEa2UkD2WI9AamvhuS2ZNnWW5DoTMQIX1swoi', alpaca_endpoint)

# Check if connection is successful:
#	account = api.get_account()
# print(account.status)


class Martingale(object):
  def __init__(self):
    self.key = 'PKTKIT2O85UBGRAZEJ2X'
    self.secret = 'OaOkEa2UkD2WI9AamvhuS2ZNnWW5DoTMQIX1swoi'
    self.alpaca_endpoint = 'https://paper-api.alpaca.markets'
    self.api = tradeapi.REST(self.key, self.secret, self.alpaca_endpoint)
    self.symbol = 'IVV'  # Can be changed to 'SPY'or 'VOO'
    self.current_order = None  # Variable to know when we have an open order
    self.last_price = 1  # last closing price of the previous agragate

    #Position: IVV
    # Positions come in 2 types: Short, and Long
    #Short: Borrowed and sold
    # Long: Held before being sold
    # For now, we do not want more than one postion open:

    # Try block to handle exceptions:
    # If the except gets triggered, then no position will exist:
    try:
      self.position = int(self.api.get_position(self.symbol).qty)
    except:
      self.position = 0

  # Create Strategy:
  # Function takes 2 parameters:
  # self and target quantity
  def submit_order(self, target):
    if self.current_order is not None:  # Check to see if there's an open order already
    # If there's already an order, cancel it
      self.api_cancel_order(self.current_order.id)
# Delta: Ratio that copares the change of price of an asset with the corresponding change of price of an option or derrivative ..

    # Our delta is:
    # target quantity - position:
    delta = target - self.position
    if delta == 0:  # If delta = 0, retun
      return
    print(f'Processing the order for {target} shares')

    if delta > 0:  # If delta is bigger than 0, we want to buy:
      buy_quantity = delta
      # If the position is less than 0, we want buy the current quantity of shares:
      if self.position < 0:
        # absolute value around the position
        buy_quantity = min(abs(self.position), buy_quantity)
      print(f'Buying {buy_quantity} shares')
        # Send request to Alpaca with api submit order method and will execute the transaction.
      self.current_order = self.api.submit_order(self.symbol, buy_quantity, 'buy', 'limit', 'day', self.last_price)
    elif delta < 0:  # Else if delta is less than 0
      sell_quantity = abs(delta)  # We want to sell
      if self.position > 0:  # If the position is greater than 0, sell:
        sell_quantity = min(abs(self.position), sell_quantity)
      print(f'Selling {sell_quantity} shares')
      self.current_order = self.api.submit_order(self.symbol, sell_quantity, 'sell', 'limit', 'day', self.last_price)


# Main Function:
if __name__ == '__main__':
  t = Martingale()  # Creating an object of the Martingale class
  # Calling the submit order function and passing in the number of shares we want to trade:
  t.submit_order(3)
