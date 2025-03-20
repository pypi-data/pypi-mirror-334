from ._jwt import _sign,_verify

__version__ = "1.0.0"
__author__ = "钟阳"

def creatr_sign(aud=None,sub=None,iss='system', key=None):
    if aud is None:
        return False
    if sub is None:
        return False
    if key is None:
        return False
    return _sign(aud,sub,iss, key)

def verify_sign(token=None, key=None):
    if token is None:
        return False
    if key is None:
        return False
    return _verify(token, key)