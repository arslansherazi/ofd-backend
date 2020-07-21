from cryptography.fernet import Fernet

from security.security_credentials import SECRET_KEY

params = '''{
"email": "arslan_sherazi@hotmail.com",
"is_email_verification_code": 1,
"encryption_disable_key": "fgresdc456tgde%rf##&gfd123swedDfrt"
}'''


def encrypt_data(data):
    cipher_suite = Fernet(SECRET_KEY.encode())
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data.decode()


def decrypt_data(encrypted_data):
    cipher_suite = Fernet(SECRET_KEY.encode())
    decrypted_data = cipher_suite.decrypt(encrypted_data.encode())
    return decrypted_data.decode()


if __name__ == '__main__':
    encrypted_params = encrypt_data(params)
    print(encrypted_params)
    print(decrypt_data(encrypted_params))
