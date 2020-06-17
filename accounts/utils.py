import base64
import json
import os

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from datetime import datetime, timedelta


def generate_nk_key(instance):
    password = instance.password.encode()
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(password))

    file = open('key.key', 'wb')
    file.write(key)  # The key is type bytes still
    file.close()


def encrypt_nk_url(instance):
    expiry_time = datetime.now() + timedelta(days=2)
    message = json.dumps(
        {"username": instance.username, "email": instance.email,
         "expiry_time": expiry_time.strftime("%b %d %Y %H %M %S %p")}).encode()
    file = open('key.key', 'rb')
    key = file.read()  # The key will be type bytes
    f = Fernet(key)
    file.close()
    encrypted = f.encrypt(message)
    # print(encrypted)
    # decrypted = f.decrypt(encrypted)
    # x = decrypted.decode()
    # x = json.loads(x)
    # print('http://localhost:8000/users/activate/' + encrypted.decode())
    return 'http://localhost:8000/users/activate/' + encrypted.decode()


def get_activation_url(instance):
    generate_nk_key(instance)
    url = encrypt_nk_url(instance)
    print(url)
    return url
