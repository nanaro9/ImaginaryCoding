#encryption/hashing test file
from cryptography.fernet import Fernet
import hashlib

text = "Test"

hashText = hash(text)
print(hashText)

#UID vieta bus lietotaja ID un tad parole kaut kada
password = Fernet.generate_key()
password2 = b'password'
print(password2)
passkey = "UID_Password"
hashObj = hashlib.sha256()
hashObj.update(passkey.encode())
hashPass = hashObj.hexdigest()

print(hashPass)
print(hashPass.encode())