# Built on Python 3.4.3 64 bits

import time
import base64
import hashlib
import hmac
import json
import urllib.request as urllib2
import ssl

class cfApiMethods( object ):
    # your apiPublicKey and apiPrivateKey are accessible in your Account view under Settings
    def __init__( self, api_address, apiPublicKey = "", apiPrivateKey = "", timeout = 10, checkCertificate = True ):
        self.api_address = api_address
        self.apiPublicKey = apiPublicKey
        self.apiPrivateKey = apiPrivateKey
        self.timeout = timeout
        self.nonce = 0
        self.checkCertificate = checkCertificate

    # returns all open contracts
    def get_contracts( self ):
        apiPath = "/api/contracts"
        response = self.make_request( "POST", apiPath, {} )
        return response

    # returns ticker information for a contract
    def get_ticker(self, tradeable, unit ):
        apiPath = "/api/ticker"
        postData = "tradeable=%s&unit=%s" % ( tradeable,unit )
        response = self.make_request( "POST", apiPath, {}, postData = postData )
        return response

    # returns the order book for a contract
    def get_orderBook( self, tradeable, unit ):
        apiPath = "/api/cumulativebidask"
        postData = "tradeable=%s&unit=%s" % ( tradeable, unit )
        response = self.make_request( "POST", apiPath, {}, postData = postData )
        return response

    # returns the CF-BPI (real time bitcon price index)
    def get_cfbpi( self ):
        apiPath = "/api/cfbpi"
        response = self.make_request( "POST", apiPath, {} )
        return response

    # returns the annualized 60 minute volatility of the CF-BPI
    def get_volatility( self ):
        apiPath = "/api/volatility"
        response = self.make_request( "POST", apiPath, {} )
        return response

    # returns all account balances
    def get_balance( self ):
        apiPath = "/api/balance"
        response = self.make_request( "POST", apiPath, {} )
        return response

    # returns all open orders
    def get_openOrders( self ):
        apiPath = "/api/openOrders"
        response = self.make_request( "POST", apiPath, {} )
        return response

    # returns last trades
    def get_trades( self, numTrades ):
        apiPath = "/api/trades"
        postData = "number=%s" % ( numTrades )
        response = self.make_request( "POST", apiPath, {}, postData = postData )
        return response

    # places an order
    def place_order( self, tradeType, tradeable, unit, tradeDir, qty, price ):
        apiPath = "/api/placeOrder"
        postData = "type=%s&tradeable=%s&unit=%s&dir=%s&qty=%s&price=%s" % ( tradeType, tradeable, unit, tradeDir, qty, price )
        response = self.make_request( "POST", apiPath, {}, postData = postData )
        return response

    # cancels an order
    def cancel_order( self, uid, tradeable, unit ):
        apiPath = "/api/cancelOrder"
        postData = "uid=%s&tradeable=%s&unit=%s" % ( uid, tradeable, unit )
        response = self.make_request( "POST", apiPath, {}, postData = postData )
        return response

    # places or cancels orders in batch
    def place_batchOrder( self, uid, jsonOrders ):
        apiPath = "/api/batchOrders"
        postData = "uid=%s&json=%s" % ( uid, jsonOrders )
        body = { "uid": uid, "json": jsonOrders }
        response = self.make_request( "POST", apiPath, body, postData = postData )
        return response

    # make an HTTP request
    def make_request( self, verb, apiPath, body_dict, postData = "" ):
        url = self.api_address + apiPath
        nonce = str( self.get_timestamp() ) + str( self.get_nonce() ).zfill( 4 )
        
        signer = cfApiSigner()
        signature = signer.sign_message( self.apiPrivateKey, apiPath, nonce, postData, "" )
        auth_headers = { "APIKey": self.apiPublicKey, "Nonce": nonce, "Authent": signature }
        
        r = urllib2.Request( url, str.encode( postData ), auth_headers )

        if self.checkCertificate == False:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            response = urllib2.urlopen( r, context = ctx )
        else:
            response = urllib2.urlopen( r )
            
        str_response = response.read().decode( "utf-8" )
        return json.loads( str_response )

    # create a nonce
    def get_nonce( self ):
        self.nonce += 1
        return self.nonce

    # create a timestamp in milliseconds
    def get_timestamp( self ):
        return int( time.time() * 1000 )

class cfApiSigner( object ):
    def sign_message( self, apiPrivateKey, apiPath, nonce, postData, body ):
        # step 1: concatenate postData, nonce + apiPath                
        message = postData + body + nonce + apiPath

        # step 2: hash the result of step 1 with SHA256
        sha256_hash = hashlib.sha256()
        sha256_hash.update( message.encode( 'utf8' ) )
        hash_digest = sha256_hash.digest()
        
        # step 3: base64 decode apiPrivateKey
        secretDecoded = base64.b64decode( apiPrivateKey )
        
        # step 4: use result of step 3 to has the result of step 2 with HMAC-SHA512
        hmac_digest = hmac.new( secretDecoded, hash_digest, hashlib.sha512 ).digest()
        
        # step 5: base54 encode the result of step 4
        return base64.b64encode( hmac_digest )
