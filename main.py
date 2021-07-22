import flask
import wallet
import random
from server import Server


app = Server()
payment_amount = 0.005 # amount of XMR for payment

@app.route("/")
def access_gateway():
    userhash = app.get_userhash()        # get the user's cookie
    if userhash:             # if the userhash exists
        if app.wallet.check_wallets(userhash, price=payment_amount, hashtable=app.hashtable):        # if payment is successful
            return app.send_static_file('payment_complete.html')  
        else:      # still waiting for a payment
            wallet = app.get_payment_gateway(userhash)  # return the existing wallet
            return flask.render_template('payment.html', data=[payment_amount, wallet, "static/barcodes/{}.png".format(userhash)])
    else:                    # if the userhash does not exist
        response = flask.make_response(flask.redirect("/"))      # save a new hash as a browser cookie
        userhash = app.generate_userhash()
        response.set_cookie('userhash', userhash, secure=True)
        payment_gateway = app.wallet.generate_new_wallet(userhash)  # generate a new wallet and add to hashtable
        app.add_to_hashtable(payment_gateway, userhash) 
        return response # refresh the page via redirection, now that the user has a valid userhash

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')


