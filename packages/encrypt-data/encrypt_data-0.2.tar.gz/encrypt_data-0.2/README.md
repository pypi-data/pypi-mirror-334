# This code will help you give the encrypted data by using the Hybrid Encryption.
# The only things it require is Public_key & Data that needs to be encrypted.

# Structure of the File
encrypt_data/
|__ encrypt_data/
|    |__ __init__.py
|   |__ main.py
|__setup.py
|__README.md

# Way to implement it.
from encrypt_data import Encrypt

public_key = "-----BEGIN RSA PUBLIC-----END RSA PUBLIC KEY-----\n"
encrypt = Encrypt(public_key)
encryption_data = {"name": "john"}
data_encrypted = encrypt.encrypt_data(data_to_be_encrypted=encryption_data)

# This file has been developed to make an encryption process a bit easier.
# We can use this for bulky data as well as the symmetric encryption is being used.
# And also the data is at utmost secure as the asymmetric encryption is also being used.