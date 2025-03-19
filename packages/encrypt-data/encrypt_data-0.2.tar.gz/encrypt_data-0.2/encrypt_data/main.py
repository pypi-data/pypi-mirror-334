from cryptography.fernet import Fernet
import rsa
import json

class Encrypt:
    def __init__(self, public_key=''):
        self.__symmetric_key = Fernet.generate_key() # Generation of random symmetric key
        self.__cypher = Fernet(self.__symmetric_key) # Used to encrypt the text
        self.__public_key = rsa.PublicKey.load_pkcs1(public_key)
        self.__symmetric_key_encryption = rsa.encrypt(self.__symmetric_key, self.__public_key) # Encrypting the symmetric key

    def encrypt_data(self, data_to_be_encrypted=''):
        response = {}
        try:
            print('Inside a main encrypt data function.')
            if data_to_be_encrypted:
                if isinstance(data_to_be_encrypted, dict):
                    data_encryption = self.__cypher.encrypt(json.dumps(data_to_be_encrypted).encode('utf-8'))
                else:
                    data_encryption = self.__cypher.encrypt(data_to_be_encrypted.encode('utf-8'))
                response['status'] = True
                response['detail'] = 'Data Encrypted Successfully.'
                response['encrypted_key'] = self.__symmetric_key_encryption
                response['encrypted_data'] = data_encryption
            else:
                response['status'] = False
                response['detail'] = 'Data not provided for Encryption.'
        except Exception as e:
            print(f"Exception caused in {self.encrypt_data.__name__} function: {e}")
            response['status'] = False
            response['detail'] = f"Exception caused in {self.encrypt_data.__name__} function: {e}"
        finally:
            return response