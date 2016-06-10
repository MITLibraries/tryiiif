import base64


def b64safe(url):
    return base64.urlsafe_b64encode(
        bytearray(url, 'utf-8')).decode('utf-8')
