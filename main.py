"""
TO DO:
- Find payment id automatically
- Make monitor and integrate with Slack
- Make this look all professional and shit with classes and logging instead some shitty printing
"""
import requests
import bs4 as bs
import simplejson as json
# importing * is bad practice, i know, go away
from decimal import *
import datetime
from urllib.parse import quote
import time

r = requests.session()
host = 'https://www.boxlunch.com/'


# if you're not using logging, this is the dumb shit you do instead
def get_timestamp():
    t = str(datetime.datetime.now())
    return t

config = open('config.json')
configdump = json.load(config)

loginemail = configdump['loginemail']
loginemaildontatme = quote(loginemail)
loginpass = configdump['loginpass']
# make sure card is default on account
paymentinfo = configdump['paymentinfo']
# Add product url and product id - product url not used at the moment
producturl = configdump['earlylink']
productid = configdump['productid']
quantity = configdump['quantity']

atcurl = 'https://www.boxlunch.com/on/demandware.store/Sites-boxlunch-Site/default/Product-CLPAdd2Cart?cgid=undefined&pid={}&Quantity=1&format=ajax'.format(productid)

headersmain = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,fr;q=0.8,es;q=0.7',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
}
headersmobileguest = {
'Host': 'cloudservices.predictspring.com',
'PredictSpring-InstallationID': 'bb40bc24-defe-4a08-a4ff-1aed95038565',
'Accept': 'application/json',
'PredictSpring-Region': 'US',
'PredictSpring-API-Key': 'afgNO1L6P2IwRegfmJFZI575',
'PredictSpring-Locale': 'en_US',
'PredictSpring-DeviceName': 'FunkoFucked',
'PredictSpring-MerchantID': 'BOXLUNCH672907',
'User-Agent': 'BoxLunch/3798 CFNetwork/901.1 Darwin/17.6.0',
'Content-Type': 'application/json'
}

# def productscrape(url):
# product = r.get(producturl, headers = headersmain)
# soup = bs.BeautifulSoup(product.text, 'lxml')
# productname = soup.find('h1', {'itemprop': 'name'})
# print(productname)clear
# soon (TM)

def login(email, password):
    loginurl = 'https://cloudservices.predictspring.com/search/v1/customer/login'

    payload = {
        "credentials":{
            "password": password,
            "userId": email,
            "userIdType":"EMAIL"
            },
            "includeCart": "true",
            "includeProfile": "true"
    }
    login = r.post(loginurl, json = payload, headers = headersmobileguest)
    print('[' + get_timestamp() + '] Follow me on Twitter - @TaquitoSlayer')
    print('[' + get_timestamp() + '] Do not forget to tell your momma that FUNKO FUCKED TOOK STOCK')
    print('[' + get_timestamp() + '] LOGGED IN WITH {}'.format(email))
    return login.text

# imagine being shit at code and using 1 entire function to checkout - im a bio major, fuck off :)
def main():
    # login and grab saved addy and other info for checkout
    login_return = login(loginemail, loginpass)
    try:
        jsondump = json.loads(login_return)
        sessionid = jsondump['sessionId']
        profile = jsondump['profile']
        customerid = profile['customerId']
        addresslist = jsondump['addressList']
    except:
        print('[' + get_timestamp() + '] Login error found! - printing response:')
        print(login_return)

    # once logged in, different header needed
    headersmobilecustomer = {
        'PredictSpring-SessionId': sessionid,
        'PredictSpring-Attribution': '%7B%22email%22%3A%22{}%22%2C%22customerGroups%22%3A%5B%22BoxLunch_5Star%22%2C%22Everyone%22%2C%22Non-Employees%22%2C%22Registered%22%5D%7D'.format(loginemaildontatme),
        'PredictSpring-CustomerGroups': 'BoxLunch_5Star|Everyone|Non-Employees|Registered',
        'PredictSpring-Region': 'CA',
        'PredictSpring-API-Key': 'afgNO1L6P2IwRegfmJFZI575',
        'PredictSpring-MerchantId': 'BOXLUNCH672907',
        'PredictSpring-Locale': 'en_CA',
        'Content-Type': 'application/json; charset=utf-8',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 8.1.0; Pixel 2 XL Build/OPM2.171019.029) FUNKOFUCKEDTOOKSTOCK',
        'Host': 'cloudservices.predictspring.com',
        'Accept-Encoding': 'gzip',
    }

    addtocarturl = 'https://cloudservices.predictspring.com/search/v1/customer/{}/cart/product/update'.format(customerid)
    carturl = 'https://cloudservices.predictspring.com/search/v1/customer/{}/cart'.format(customerid)
    payload = {
        "adjustedQuantity":0,
        "cartItemList":[],
        "isGift": 'false',
        "newQuantity": quantity,
        "oneTimePromotionCodes":[],
        "productId": productid,
        "promotionCodes":[],
        "session": sessionid}
        
    add = r.post(addtocarturl, json = payload, headers = headersmobilecustomer)
    print('[' + get_timestamp() + '] PRODUCT ADDED TO CART')
    # Most info needed for placing order comes from add.text
    # why does json in python convert decimal values when not asked to?
    jsondump = json.loads(add.text, use_decimal=True)
    cartitemlist = jsondump['cartItemList']
    price = jsondump['subTotal']
    price = json.dumps(price, use_decimal=True)

    # On app, selecting cart makes an initial request for info - It's most likely redundant.
    payload_orderpullup = {
        "cartItemList": cartitemlist,
        "customerGroups":["BoxLunch_5Star","Everyone", "Non-Employees", "Registered"],
        "customerId": customerid,
        "rewardList":[],
        "customerEmail": loginemail,
        "giftCardList":[],
        "installationId":"fb04e0df-13f8-493f-b3cd-f3de91a13d54",
        "isGift":'false',
        "oneTimePromotionCodes":[],
        "productList":[],
        "promotionCodes":[],
        "shippingAddress": addresslist[0]
    }
    orderpullup = r.post(addtocarturl, json = payload_orderpullup, headers = headersmobilecustomer)
    jsondump = json.loads(orderpullup.text)
    sessionid = jsondump['session']

    # For whatever reason, demandware-mobileapi likes to make 2 request of pretty much the exact things in the payload, except for 1-3 new key and value added
    # When submitting this, it creates an order which when made, essentially the product is yours, you just need to pay.
    for cartitemlists in cartitemlist:
        cartitemlists['variantGroupId'] = productid
        cartitemlists['adjustedQuantity'] = '0'
        cartitemlists['oldQuantity'] = '0'
        cartitemlists['price'] = price

    payload_orderinit = {
        "cartItemList": cartitemlist,
        "customerGroups":["BoxLunch_5Star","Everyone", "Non-Employees", "Registered"],
        "customerId": customerid,
        "rewardList":[],
        "customerEmail": loginemail,
        "giftCardList":[],
        "installationId":"fb04e0df-13f8-493f-b3cd-f3de91a13d54",
        "isGift":'false',
        "oneTimePromotionCodes":[],
        "productList":[],
        "promotionCodes":[],
        "shippingAddress": addresslist[0]
    }
    add_orderinit = r.post(carturl, json = payload_orderinit, headers = headersmobilecustomer)
    # final order - get hit with these shitty variable names that don't follow pep8
    jsondump = json.loads(add_orderinit.text, use_decimal=True)
    shippingmethod = jsondump['shippingMethodList']
    shippingmethodid = shippingmethod[0]['shippingMethodId']
    shippingprice = shippingmethod[0]['price']
    shippingtax = shippingmethod[0]['tax']
    # gay ass decimal shit
    getcontext().prec = 47
    grandtotal = Decimal(shippingprice) + Decimal(price) + Decimal(shippingtax)
    print('[' + get_timestamp() + '] GRAND TOTAL: ', grandtotal)

    payload_orderfinal = {
        "billingAddress": addresslist[0],
        "cartId": "this",
        "customerEmail": loginemail,
        "customerId": customerid,
        "rewardList": [],
        "giftCardList": [],
        "grandTotal": str(grandtotal),
        "installationId": "fb04e0df-13f8-493f-b3cd-f3de91a13d54",
        "isGift": 'false',
        "oneTimePromotionCodes": [],
        "paymentData": {
            "paymentCard": paymentinfo,
            "paymentType": "StoredCard"
        },
        "productList": cartitemlist,
        "promotionCodes": [],
        "shippingAddress": addresslist[0],
        "shippingMethodId": shippingmethodid,
        "storeId": ""
    }
    # i heard project destroyer cant even push payment through properly :P
    final = 'https://cloudservices.predictspring.com/search/v1/customer/{}/cart/this/submit'.format(customerid)
    finalcheckout = r.post(final, json = payload_orderfinal, headers = headersmobilecustomer)
    print('[' + get_timestamp() + '] ' + finalcheckout.text)


# let's buttfuck at 213132321312213 requests/second and if it times out TOO FUCKING BAD WE GUNNA KEEP FUCKING IT TILL BOXLUNCH'S CAREER IS LISA ANN
while True:
    # could make this a seperate function but it's already done and i got lazy - it's basically a monitor in 5-10 lines of code
    checkifavail = r.get(atcurl, headers = headersmain)
    soup = bs.BeautifulSoup(checkifavail.text, 'lxml')
    inventory = soup.find('input', {'name': 'hasInventory'}).get('value')
    if inventory == 'false':
        print('[' + get_timestamp() + '] NOT IN STOCK, MONITORING...')
        # where were you when i didnt add proper exception handling for connection handling which almost happens all the time ;)
        time.sleep(1.5)
    elif inventory == 'true':
        print('[' + get_timestamp() + '] STOCK FOUND')
        print('[' + get_timestamp() + '] CHECKING OUT NOW')
        main()
        break
