import base64

from Crypto.Cipher import AES
from Crypto.Util.py3compat import bchr, bord

from security.security_credentials import (ENCRYPTION_KEY, ENCRYPTION_MODE,
                                           ENCRYPTION_SALT)

params = '''{
"username": "arslansherazi",
"password": "123456",
"user_type": 1
}'''


class AESCipher(object):
    block_size = AES.block_size

    @classmethod
    def encrypt(cls, data):
        data = cls.pad(data)
        cipher = AES.new(key=ENCRYPTION_KEY, mode=ENCRYPTION_MODE, IV=ENCRYPTION_SALT)
        encrypted_data = cipher.encrypt(data)
        encrypted_data = base64.b64encode(encrypted_data)
        encrypted_data = encrypted_data.decode(errors='ignore')
        return encrypted_data

    @classmethod
    def decrypt(cls, encrypted_data):
        encrypted_data = base64.b64decode(encrypted_data)
        cipher = AES.new(key=ENCRYPTION_KEY, mode=ENCRYPTION_MODE, IV=ENCRYPTION_SALT)
        data = cipher.decrypt(encrypted_data)
        data = cls.unpad(data)
        data = data.decode(errors='ignore')
        return data

    @classmethod
    def pad(cls, data):
        number_of_bytes_to_pad = cls.block_size - len(data) % cls.block_size
        padding = bchr(number_of_bytes_to_pad) * number_of_bytes_to_pad
        return data + padding

    @classmethod
    def unpad(cls, data):
        padding_len = bord(data[-1])
        return data[:-padding_len]


if __name__ == '__main__':
    # encrypted_data = 'fv+iszl/ORvEdK/ub2Pku0zXD/ZSjf3GumKdN3ihysPQjuiLTNrA+5WAiZAZk8uk+6l3BzDnnbYCtZtos6/hqgGoRMpq6szwdbxOeJHQ9ITc8Uf+VeQ50wdDau7OZOfEHHZCWsJIC6/+egr5vku679LmNkww8Qo1SwIlwGqVHlzY0oxkx2UBPRJvOEnQUBR1UzdcwRnn05hZozevTGRAJIbVeflQJ/B/JmUthv2fgNHlFPyXA1UfrjIfEB8eiYWoeH+sXEQ8rgnlrsUdTHj1Q/KhEyhjG/kBrn2TUoAJRYK4F3Gy7jTa6Ho2OyZoyHdSYvWgucfEYdVd8rM87n6rrwF7tRSY61ftx9oOcGTJRmDVKR94UmEGgDLMQ6oyh0gAVIq3slG5ya5Cc2IIviohT+gxbfebyQrea5Fbr1WmNFYKOW9omcQf9X6o7rxWVXsODy/ml7FeIpaVActTIDN3OhaBwznMpr27J6RE644Wk6yBPk70S98bsG7mSGD9BTcGRAbryR31t6GEy5lgBPjtF4mkmaoHMmmdEvatnYdWT8UCqqxpdSC5X9w3OiUJcIVvwEoAWsShbjEVIYpZU1dewxpupvv+RRXA+Vx0zr0fbZBNxc8D1N7RefRVbeR4e1x6k0GiUJ1HD18HzfBeLnKld3dMXyPX3dg8GZtIya+wSVKA6GFr+KOE4ZZWCU2AxkKJi8GKYt62OnY+ekSNCVn4TNvUPHvzXd2MQPGjiFWPNqlmKQhEEzfm8lR20pyTpOFKLuC45eiUj1u+BXm1OANBMg=='
    # decrypted_data = AESCipher.decrypt(encrypted_data)
    # print(decrypted_data)
    encrypted_params = AESCipher.encrypt(params.encode())
    print(encrypted_params)
    print(AESCipher.decrypt(encrypted_params))
