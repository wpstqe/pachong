import base64
import pyotp
str= 'TSBH2O2QU3MNPCP2'
info = base64.b32encode(str)
print(info)
data = pyotp.TOTP('KRJUESBSJ4ZFCVJTJVHFAQ2QGI======')
print(data)
print(data.now())