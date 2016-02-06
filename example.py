# Built on Python 3.4.3 64 bits

import cfApi
import uuid

apiPath = "https://www.cryptofacilities.com/derivatives"
apiPublicKey = "..."
apiPrivateKey = "..."
        

##### public methods #####

cfPublic = cfApi.cfApiMethods( apiPath )

# get contracts    
result = cfPublic.get_contracts()

# get ticker    
result = cfPublic.get_ticker( "F-XBT:USD-Sep16", "USD" )

# get order book    
result = cfPublic.get_orderBook( "F-XBT:USD-Sep16", "USD" )

# get CF-BPI    
result = cfPublic.get_cfbpi()

# get volatility  
result = cfPublic.get_volatility()


##### private methods #####

cfPrivate = cfApi.cfApiMethods( apiPath, apiPublicKey = apiPublicKey, apiPrivateKey = apiPrivateKey )

# get balances  
result = cfPrivate.get_balance()

# get open orders  
result = cfPrivate.get_openOrders()

# get trades  
result = cfPrivate.get_trades( 10 )

# place order
tradeType = "LMT"
tradeable = "F-XBT:USD-Sep16"
unit = "USD"
tradeDir = "Buy"
qty = 1
price = 10
result = cfPrivate.place_order( tradeType, tradeable, unit, tradeDir, qty, price )

# cancel order
orderID = "8d89b8ca-d502-423b-b39d-33b7b3894432"
tradeable = "F-XBT:USD-Sep16"
unit = "USD"
result = cfPrivate.cancel_order( orderID, tradeable, unit )

# batch order
uid = str( uuid.uuid4() )
orders = [
    {
    "order": "send",
    "type": tradeType,
    "tradeable": tradeable,
    "unit": unit,
    "dir": tradeDir,
    "qty": qty,
    "price": price,
    },
    {
    "order": "cancel",
    "uid": orderID,
    "tradeable": tradeable,
    "unit": unit,
    },    
]

batch = {
    "id": uid,
    "orders": orders,
        } 

result = cfPrivate.place_batchOrder( uid, batch )
