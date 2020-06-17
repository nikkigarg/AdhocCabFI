""" 
import secrets
with open('user-data.txt') as f:
    words = [word.strip() for word in f]
    print(words)
    password = ' '.join(secrets.choice(words) for i in range(4))
    print(password)
    print('https://mydomain.com/reset=' + secrets.token_urlsafe(password))
 
 https://nitratine.net/blog/post/encryption-and-decryption-in-python/#installing-cryptography
 """

import json 

from cryptography.fernet import Fernet
message = json.dumps({"usename":"nikita","email":"nikita@gmail.com"}).encode()
print(message)

key = Fernet.generate_key()
file = open('key.key', 'wb')
file.write(key) # The key is type bytes still
file.close()

file = open('key.key', 'rb')
key = file.read() # The key will be type bytes
f = Fernet(key)
file.close()
encrypted = f.encrypt(message)
print(encrypted)
decrypted = f.decrypt(encrypted)
x = decrypted.decode()
x = json.loads(x)
print('https://mydomain.com/reset='+str(encrypted))