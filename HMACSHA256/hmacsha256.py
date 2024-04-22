from datetime import datetime,timedelta
import uuid
import base64
import hmac
import hashlib
import os

from Functions.Converter import DatetimeToTimestamp


def getSignature(timestamp, nonce):
    payload = str(timestamp) + '&' + nonce
    payload_bytes = payload.encode('utf-8')
    hash_byte = hmac.new(os.getenv('ADMIN_KEY_SECRETE').encode('ascii'), payload_bytes, hashlib.sha256).digest()
    hash_string = base64.b64encode(hash_byte)

    return hash_string


def setHeaders():
    now = datetime.now()
    timestamp = DatetimeToTimestamp(now)
    # print(f"timestamp: {timestamp}")

    # nonce = secrets.token_hex(16)  # (16바이트) 16진수 secure random number 생성
    nonce = str(uuid.uuid4())
    # print("nonce: " + nonce)

    # signature 생성
    signature = getSignature(timestamp, nonce)
    # print("signature: " + signature.decode('ascii'))

    headers = {
        'timestamp': str(timestamp),
        'nonce': nonce,
        'accessKey': os.getenv('ADMIN_KEY_ACCESS'),
        'signature': signature,

    }

    return headers


def getSignature_v1(timestamp, nonce):
    payload = str(timestamp) + '&' + nonce
    payload_bytes = payload.encode('utf-8')
    hash_byte = hmac.new(os.getenv('ADMIN_KEY_SECRETE_v1').encode('ascii'), payload_bytes, hashlib.sha256).digest()
    hash_string = base64.b64encode(hash_byte)

    return hash_string

def setHeaders_v1():
    now = datetime.now()+ timedelta(hours=9)
    timestamp = DatetimeToTimestamp(now)

    # nonce = secrets.token_hex(16)  # (16바이트) 16진수 secure random number 생성
    nonce = str(uuid.uuid4())
    # print("nonce: " + nonce)

    # signature 생성
    signature = getSignature_v1(timestamp, nonce)
    # print("signature: " + signature.decode('ascii'))

    headers = {
        'timestamp': str(timestamp),
        'nonce': nonce,
        'accessKey': os.getenv('ADMIN_KEY_ACCESS_v1'),
        'signature': signature,

    }

    return headers