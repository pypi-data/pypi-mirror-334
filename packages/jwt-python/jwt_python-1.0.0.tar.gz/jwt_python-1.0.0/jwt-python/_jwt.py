import hmac
import hashlib
import base64
import json
import time


# 生成签名
def _generate(message, secret_key):
    message_bytes = message.encode('utf-8')
    secret_key_bytes = secret_key.encode('utf-8')
    signature = hmac.new(secret_key_bytes, message_bytes, hashlib.sha256).digest()
    return base64.urlsafe_b64encode(signature).decode('utf-8').rstrip("=")

# 验证签名
def _verify_sign(message, signature, secret_key):
    new_signature = _generate(message, secret_key)
    return hmac.compare_digest(new_signature, signature)

def _sign(aud=None,sub=None,iss='system', secret_key=None):
    iat = int(time.time())
    exp = iat + 86400
    Header = {'alg': 'HS256', "type": 'JWT'}
    Payload = {
        'aud': aud,
        'exp': exp,
        'iat': iat,
        'iss': iss,
        'sub': sub,
        'nbf': iat}
    Header = json.dumps(Header)
    Header = str(Header)
    Header = Header.encode('utf-8')
    Header = base64.b64encode(Header)
    Payload = json.dumps(Payload)
    Payload = str(Payload)
    Payload = Payload.encode('utf-8')
    Payload = base64.b64encode(Payload)
    HP = Header.decode() + '.' + Payload.decode()
    Signature = _generate(HP, secret_key)
    Token = HP + '.' + Signature
    return Token

def _verify(token=None, secret_key=None):
    token = token.split(' ')
    if len(token) == 2:
        token = token[1]
        token = token.split('.')
        if len(token) == 3:
            if (_verify_sign(token[0] + '.' + token[1], token[2], secret_key)):
                Payload = token[1]
                Payload = base64.b64decode(Payload)
                Payload = Payload.decode('utf-8')
                Payload = json.loads(Payload)
                if (Payload['exp'] > int(time.time())):
                    return Payload
                return False
            return False
        return False
    return False