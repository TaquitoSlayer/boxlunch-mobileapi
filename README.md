# BoxLunch.com Monitor and Checkout - Mobile API
![FunkoFuckedTookStock](https://i.imgur.com/cZHg4w1.png)

I'm seeing more and more people enter the Funko POP! collection scene, and I've realized that these web devs need to step up their game to make it fair for the collectors. Sike, I resell these joints. However, it's way too easy to get these right now, and what better way to manipulate the market by making it easier to supplement demand.

Introducing the first public 'Funko' bot that can easily be edited to work for Hot Topic as well (soon(tm)).

Follow me on [Twitter](https://twitter.com/taquitoslayer)

Feel free to pay for my tuition while you're at it by sending me some BTC - 178zRN3YVdiTRivhHoJcbJRe7rnGSLRePY

## Limitations to the Mobile API
* They have a bug on their app that even though you're using your own account, it'll still charge you $5 for shipping if you're in the US as opposed to the $1. Call their customer service, they'll credit you back $4.
* You need to find the payment udid respective to the credit card you're using yourself since you can't scrape the payment udid with the mobile API (I could add this later if you have the IQ of a rock).
* The item in question cannot have a discount applied. I'll update this to fix that if the demand is there, but for the most part, the products you're trying to get with this aren't discounted to begin with.
* If you have an alternative shipping address, you are currently shit out of luck and need to make sure that you only have 1 address. If you really want to add the second address on your Boxlunch account as the shipping/billing, edit the [0] to [1] where you can use it as a method of index navigation (if you have 3 addresses on the account, [0] is the default one, [1] the second one, [2] the third and so on.
```
"billingAddress": addresslist[0]
```
```
"shippingAddress": addresslist[0]
```
Find the above lines in main.py and edit them.

### With that said, let's get started.
### How to install and use
1. Make sure you install [Python3](https://www.python.org/getit/) and [pip](https://pip.pypa.io/en/stable/installing/) followed by running the following in the same directory as main.py
```bash
pip3 install -r requirements.txt
```
2. Edit config.json with info needed
> paymentID is a uuid generated randomly once card is saved to account. To get it, simply go to https://www.boxlunch.com/wallet on your desktop after logging into your account, then find "dwfrm_paymentinstruments_creditcards" in page source where you can also find card name (e.g. Mastercard = Master Card)
![FunkoFuckedTookStock](https://i.imgur.com/3eaH660.png)
3. Run script
```bash
python3 main.py
```
> If you have problems with any of the above, you need to google your errors. There are many things that can be wrong, and if all else fails, drop a follow on my twitter and DM me and I'll try and help. I'm nice if you're nice.

## Future features:
* Scrape uuid manually along with credit card name
* Switch to desktop for checkout. This is possible however they are planning on adding captcha in the foreseeable future granted they use demandware so for now, let's abuse the mobile API instead.
