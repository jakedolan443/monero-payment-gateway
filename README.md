# monero-payment-gateway

A simple proof-of-concept payment gateway for the cryptocurrency Monero, using a `monero-python` and `flask` backend.

This web server uses a userhash, stored as a cookie, to distinguish payments - this means payments are **somewhat** anonymous, adhearing to monero's main principles. This is different to most services where, instead of having anonymity, you sign up with an email and complete KYC etc.

The user is presented with a payment page with a unique wallet, generated for their unique userhash. This wallet belongs to an account of a single monero-wallet (this makes it easy for admins to handle, instead of several individual accounts, meaning all can be transferred quickly).

![image](https://raw.githubusercontent.com/jakedolan443/monero-payment-gateway/main/payment.png)

Upon payment, the web server will return a payment complete page to the userhash

![image](https://raw.githubusercontent.com/jakedolan443/monero-payment-gateway/main/payment_complete.png)

# How it works

The server uses flask to handle requests. 

On request, the user is given a userhash and redirected to the payment page, where a corresponding wallet address & barcode are generated and saved in a dictionary. 

On request, if an existing userhash is given by the user, its existence will be checked in the dictionary. If it exists, the same wallet address & barcode will be served to the user. This allows payments to be distinguishable and remain consistent per user.

If the wallet address already exists, the wallet object is checked using `monero-python`. If the balance of the wallet is above what is due, the user is delivered a "payment complete" page. This could be expanded to include an `access:1` entry in the dictionary or for use in a larger json file. Or, for concurrent usage, an SQL database. For use of a json file, wallet objects have been serialized to allow wallet addresses to be placed into json files without error - these are then unserialized into wallet objects when the balance is found. This also saves memory.

Due to this project being a "proof-of-concept" I did not choose to include any of these additions, this is merely to show how monero payments can be implemented using cookies.

Another obstacle in using a database/json file would be clearing cache, as there is currently no implementation for removing addreses that are no longer used. This could be done using python's `time` module, where after 24 hours (86400 seconds) a wallet address is marked for removal, which could be executed with a simple crontab.

# Setup 

This program was created & tested on Debian 10 (Buster); see your own distro/OS details for installation.

To interact with the monero wallet, the server uses the `monero-rpc-wallet` binded on a localhost port.

The `monero-rpc-wallet` is not included by default in debian's repositories, but is included in the whonix repository:

```
echo "deb https://deb.whonix.org buster main contrib non-free" > /etc/apt/sources.list.d/whonix.list
apt update -y
apt-get install monero-gui
```

This will install the `monero-wallet-rpc` command among other tools.

First, a wallet file must be created using `monero-wallet-cli`

To start the wallet daemon:
```
monerod
```
To start the RPC wallet:
```
monero-wallet-rpc --wallet-file <wallet-file> --password "" --rpc-bind-port 28088 --disable-rpc-login
```
If you do not have your own node, you can use a remote node (note this is not advised on production servers):
```
monero-wallet-rpc --wallet-file <wallet-file> --password "" --rpc-bind-port 28088 --disable-rpc-login --daemon-host node.supportxmr.com
```
Now, we can setup the web server.
```
git clone https://github.com/jakedolan443/monero-payment-gateway
cd monero-payment-gateway
pip3 install -r requirements.txt
```
# Usage
Run 
```
python3 main.py
```
Now, navigate to `127.0.0.1:5000` in your web browser.
A different host/port can be specified in `main.py`

# Donate
XMR
```
85wYZS2eFM3FqEU3yMeuMmh4PXC7vgC2AZS27ow6bU7QhYQYEbQBzd4WbcSLgs43yeZ1uAHRkGcn1Q6jRyNHcL881JoAyVG
```
