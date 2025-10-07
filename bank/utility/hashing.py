from cryptography.fernet import Fernet
import hashlib
import base64
def generate_key(password):
    key = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode( key)

def encrypt(message, key):
    cipher_suite = Fernet(generate_key(key) )
    encrypted_message = cipher_suite.encrypt(  message.encode())
    return encrypted_message
def decrypt(encrypted_message, key):
    cipher_suite = Fernet(generate_key(key))
    decrypted_message = cipher_suite.decrypt(encrypted_message).decode()
    return decrypted_message

