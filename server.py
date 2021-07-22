import random
from flask import Flask, request
import wallet


class Server(Flask):
    def __init__(self):
        Flask.__init__(self, __name__)
        self.wallet = wallet.Wallet()
        self.hashtable = {}
        
    def generate_userhash(self):   # create a fixed length string, stored as a cookie
        string = ""
        for i in range(32):    
            string += random.choice(list("1234567890"))      # real userhashes would be a lot more sophisticated, using digits only could be vulnerable to brute force attacks
        return string
        
    def get_userhash(self):
        userhash = request.cookies.get('userhash')
        if userhash in list(self.hashtable.keys()):
            return userhash # the userhash exists, return it
        else:
            return False # the userhash does not exist, generate a new one
        
    def add_to_hashtable(self, wallet, userhash):
        self.hashtable[userhash] = wallet
        
    def get_payment_gateway(self, userhash):
        return self.hashtable[userhash]
        
