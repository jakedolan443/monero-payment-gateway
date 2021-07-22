import monero.wallet
from monero.backends.jsonrpc import JSONRPCWallet
import requests.exceptions
import time
import qrcode


class Wallet(monero.wallet.Wallet):
    def __init__(self):
        try:
            monero.wallet.Wallet.__init__(self, JSONRPCWallet(port=28088))          # requires monerod and rpc-wallet, see README
        except requests.exceptions.ConnectionError:
            print("Wallet failed to initialize, trying again in 60 seconds.")
            time.sleep(60)
            self.__init__()
    
    def check_wallets(self, userhash, price=0, hashtable={}):               # check if the purchase is completed
        bal = float(self._unserialize(hashtable[userhash]).balance(unlocked=True))          # get unlocked balance of the wallet - balance becomes unlocked after 10 confirmations 
        bal_due = price
        if bal >= bal_due:  
            return True
        else:
            return False
    
    def generate_qrcode(self, userhash, address):
        img = qrcode.make(address, box_size=4)
        img.save("static/barcodes/{}.png".format(userhash))        
            
    def generate_new_wallet(self, userhash):
        wallet = self._serialize(self.new_account())
        self.generate_qrcode(userhash, wallet)
        return wallet
    
    def _serialize(self, wallet):        # allows for use in json files
        return wallet.address().__repr__()
    
    def _unserialize(self, wallet_address):      # returns a wallet object back from a json formatted object
        for wallet in self.accounts:
            if wallet_address == wallet.address().__repr__():
                return wallet
